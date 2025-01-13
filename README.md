
# Real-Time WebSocket Server with FastAPI: User Management and Challenges
sample from postman
![Server Image 1](https://github.com/user-attachments/assets/e75baddf-a7da-4c59-adad-00ed0b337b37)
![Server Image 2](https://github.com/user-attachments/assets/de0af26e-dd29-45c4-b3e5-34e9257089ae)

## Overview

This project implements a **real-time WebSocket server** using FastAPI. It allows multiple users to connect, interact, and initiate challenges dynamically. The foundation of the server is built to manage user sessions and handle real-time communication, paving the way for building multiplayer applications.

### Key Features
- **User Management**: 
  - Handles real-time user connections and disconnections.
  - Broadcasts the active user list to all connected clients.
- **Challenge Functionality**:
  - Allows users to send and accept challenges.
  - Facilitates dynamic interactions between users.
- **Scalability**:
  - Lightweight and efficient WebSocket communication using FastAPI.

---

## Getting Started

### Prerequisites
- **Python 3.8 or above**
- FastAPI and Uvicorn installed:
  ```bash
  pip install fastapi uvicorn
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Real-Time-WebSocket-Server.git
   cd Real-Time-WebSocket-Server
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server
Start the server using Uvicorn:
```bash
uvicorn main:app --reload
```
The server will be accessible at `http://127.0.0.1:8000`.

---

## API Endpoints

### WebSocket Endpoint
- **`/ws`**: Handles WebSocket connections for real-time communication.

#### Sample WebSocket Messages
1. **Join the Server**:
   ```json
   {
       "type": "join",
       "username": "shiv"
   }
   ```
2. **Send a Challenge**:
   ```json
   {
       "type": "challenge",
       "challenged": 12345
   }
   ```
3. **Accept a Challenge**:
   ```json
   {
       "type": "accept_challenge",
       "challenge_id": 1
   }
   ```
4. **Leave the Server**:
   ```json
   {
       "type": "leave"
   }
   ```

---

## Future Enhancements
- [ ] Implement Tic-Tac-Toe game mechanics.
- [ ] Add persistent score tracking and leaderboard.
- [ ] Integrate a front-end client for better user interaction.

---

## Screenshots

### user1
![Server Image 1](https://github.com/user-attachments/assets/e75baddf-a7da-4c59-adad-00ed0b337b37)

### user2
![Server Image 2](https://github.com/user-attachments/assets/de0af26e-dd29-45c4-b3e5-34e9257089ae)

---

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

---
