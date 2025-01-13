from fasthtml.common import *

# Initialize FastHTML application
app, rt = fast_app()

# FastHTML page rendering the WebSocket interface
@rt('/')
def home():
    return Titled("WebSocket Active Users",
        Div(
            Div(
                Label("Enter your username:", For="username"),
                Input(id="username", type="text", placeholder="Your username"),
                Button("Join", onclick="connectWebSocket()"),
                id="username-form",
            ),
            Div(
                H2("Your Name"),
                H3(id = "current_user_name_only"),
                P("wants to connect to you :",id = "connection_request"),
                H2("Active Users:"),
                Ul(id="user-list"),
                Button("Leave", onclick="leaveWebSocket()"),
                id="active-users",
                cls="hidden"
            ),
            Script(
                f"""
                let websocket;
                let username;

                function connectWebSocket() {{
                    username = document.getElementById("username").value;
                    if (!username) {{
                        alert("Please enter a username!");
                        return;
                    }}
                    websocket = new WebSocket(`ws://10.7.116.100:8000/ws`); // FastAPI WebSocket URL

                    websocket.onopen = () => {{
                        websocket.send(JSON.stringify({{ type: "join", username }}));
                        document.getElementById("username-form").classList.add("hidden");
                        document.getElementById("current_user_name_only").innerHTML = username;
                        document.getElementById("active-users").classList.remove("hidden");
                        
                    }};

                    websocket.onmessage = (event) => {{
                        const data = JSON.parse(event.data);
                        console.log(data);
                        if (data.type === "active_users") {{
                            updateActiveUsers(data.users,username);
                        }}
                        if (data.type === "connection_request"){{
                            document.getElementById("connection_request").innerHTML += username;}}
                    }};

                    websocket.onclose = () => {{
                        alert("Disconnected from server.");
                        resetUI();
                    }};
                }}

                function leaveWebSocket() {{
                    websocket.send(JSON.stringify({{ type: "leave" }}));
                    websocket.close();
                    resetUI();
                }}

                function resetUI() {{
                    document.getElementById("username").value = "";
                    document.getElementById("username-form").classList.remove("hidden");
                    document.getElementById("active-users").classList.add("hidden");
                    updateActiveUsers([]);
                }}

                function updateActiveUsers(users) {{
                    const userList = document.getElementById("user-list");
                    userList.innerHTML = ""; // Clear the current list
                    users.forEach((user) => {{
                        if (user === username) return; // Skip the current user wich is user itself.
                        const li = document.createElement("li");
                        const button = document.createElement("button");
                        button.textContent = user;
                        button.onclick = () => {{
                            websocket.send(JSON.stringify({{ type: "connect_request", target_user: user }}));
                        }};
                        li.appendChild(button);
                        userList.appendChild(li);
                    }});
                }}
                """
            ),
            Style(
                """
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                #active-users {
                    margin-top: 20px;
                }
                .hidden {
                    display: none;
                }
                """
            )
        )
    )

# Run the FastHTML application
serve()
