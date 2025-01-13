from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class User:
    def __init__(self, websocket_id: int, username: str, websocket: WebSocket):
        self.websocket_id = websocket_id
        self.username = username
        self.websocket = websocket
        self.status = "Active"
        self.score = 0

    async def send_message(self, message: dict):
        """Send a JSON message to the user's WebSocket."""
        try:
            await self.websocket.send_json(message)
        except Exception as e:
            print(f"Error sending message to {self.username}: {e}")
            raise e


class Challenge:
    def __init__(self, user1_id: int, user2_id: int):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.start = False
        while self.start:
            print("Starting challenge!!!!!")


# Data Structures
active_users = {}  # {websocket_id: User}
active_challenges = {}  # {challenge_id: Challenge}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    await websocket.accept()
    websocket_id = id(websocket)
    user = None

    try:
        while True:
            data = await websocket.receive_json()

            if data["type"] == "join":
                username = data["username"]
                user = User(websocket_id, username, websocket)
                active_users[websocket_id] = user
                await broadcast_active_users()

            elif data["type"] == "leave" and websocket_id in active_users:
                await handle_disconnect(websocket_id)

            elif data["type"] == "challenge":
                print(type(websocket_id),type(data["challenged"]))
                await handle_challenge(data, websocket_id)

            elif data["type"] == "accept_challenge":
                await handle_accept_challenge(data)

            elif data["type"] == "decline_challenge":
                await handle_decline_challenge(data)

    except WebSocketDisconnect:
        print(f"WebSocket {websocket_id} disconnected.")
        await handle_disconnect(websocket_id)
    except Exception as e:
        print(f"Error in WebSocket {websocket_id}: {e}")

    finally:
        await handle_disconnect(websocket_id)


async def handle_disconnect(websocket_id: int):
    """Handle user disconnection."""
    if websocket_id in active_users:
        del active_users[websocket_id]

    # Clean up challenges involving the disconnected user
    challenges_to_remove = [
        cid for cid, challenge in active_challenges.items()
        if challenge.user1_id == websocket_id or challenge.user2_id == websocket_id
    ]
    for cid in challenges_to_remove:
        del active_challenges[cid]

    await broadcast_active_users()


async def handle_challenge(data: dict, websocket_id: int):
    """Handle a challenge request."""
    challenged_id = int(data.get("challenged"))
    if challenged_id in active_users:
        print("TRUE")
        challenged_user = active_users[challenged_id]
        challenger_user = active_users[websocket_id]
        challenge_id = id(challenger_user)
        print(challenge_id,challenger_user,challenged_user)
        active_challenges[challenge_id] = Challenge(websocket_id, challenged_id)
        await challenged_user.send_message({
            "type": "challenge",
            "challenge_id": challenge_id,
            "challenger": challenger_user.username,
        })
    else:
        await active_users[websocket_id].send_message({
            "type": "error",
            "message": "Challenged user not found.",
        })


async def handle_accept_challenge(data: dict):
    """Handle challenge acceptance."""
    challenge_id = int(data.get("challenge_id"))
    if challenge_id in active_challenges:
        challenge = active_challenges[challenge_id]
        user1 = active_users.get(challenge.user1_id)
        user2 = active_users.get(challenge.user2_id)

        if user1 and user2:
            await user1.send_message({
                "type": "challenge_accepted",
                "opponent": user2.username,
            })
            await user2.send_message({
                "type": "challenge_accepted",
                "opponent": user1.username,
            })
            challenge.start = True

        # Remove the challenge after acceptance
        del active_challenges[challenge_id]


async def handle_decline_challenge(data: dict):
    """Handle challenge decline."""
    challenge_id = data.get("challenge_id")
    if challenge_id in active_challenges:
        challenge = active_challenges[challenge_id]
        challenger_user = active_users.get(challenge.user1_id)
        declining_user = active_users.get(challenge.user2_id)

        if challenger_user and declining_user:
            await challenger_user.send_message({
                "type": "challenge_declined",
                "opponent": declining_user.username,
            })

        # Remove the challenge after decline
        del active_challenges[challenge_id]


async def broadcast_active_users():
    """Broadcast the list of active users to all connected clients."""
    user_list = [{"websocket_id": uid, "username": user.username} for uid, user in active_users.items()]
    for user in list(active_users.values()):
        try:
            await user.send_message({"type": "active_users", "users": user_list})
        except Exception:
            print(f"Failed to broadcast to {user.username}")
            await handle_disconnect(user.websocket_id)


@app.get("/")
async def root():
    return {"message": "WebSocket server is running. Connect to '/ws' with a WebSocket client."}
