# 21BCE0310 - Hitwicket Task Submission

This project is a two-player online chess-like game with custom rules. The game is played on a 5x5 grid, where each player controls a team of five characters. The game supports real-time gameplay using Flask-SocketIO for WebSocket-based communication between the players.

## Table of Contents
1. [Project Description](#project-description)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Running the Game](#running-the-game)
6. [Gameplay Instructions](#gameplay-instructions)
7. [File Structure](#file-structure)
8. [Known Issues](#known-issues)
9. [Future Improvements](#future-improvements)
10. [Screenshot](#screenshot)

## Project Description

This is a multiplayer online game inspired by chess, but with a custom set of rules. The game is designed to be played by two players on a 5x5 grid. Each player has five characters, which include Pawns, Hero1, and Hero2. The objective of the game is to eliminate all of the opponent's characters.

The game supports real-time communication between the players using WebSockets, allowing both players to see the game board and make their moves in sync.

## Features

- **Real-Time Multiplayer**: Two players can play against each other in real time using WebSockets.
- **Custom Rules**: The game uses custom rules for character movements, different from standard chess.
- **Simple User Interface**: A basic web interface to visualize the game board and interact with the pieces.
- **Cross-Platform**: The game runs on any platform that supports Python and Flask.

## Technologies Used

- **Backend**: Flask, Flask-SocketIO, Python
- **Frontend**: HTML, JavaScript, Socket.IO
- **WebSockets**: For real-time communication between the server and clients
- **Flask-CORS**: To handle Cross-Origin Resource Sharing (CORS) for WebSocket connections

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Node.js (optional, for advanced WebSocket debugging)

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/revant-kumar/P-Revant-Kumar-21BCE0310.git
   cd P-Revant-Kumar-21BCE0310
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the Required Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` file, manually install the necessary packages:
   ```bash
   pip install flask flask-socketio flask-cors eventlet
   ```

4. **Run the Game Server**:
   ```bash
   python app.py
   ```

   The server will start on `http://localhost:5000`.

## Running the Game

1. **Access the Game**:
   Open a browser and navigate to `http://localhost:5000`. If you're running the game on a remote server, replace `localhost` with the server's IP address.

2. **Playing as Two Players**:
   - Open two browser windows or tabs.
   - Each player will be automatically assigned a player ID (`A` or `B`) when they connect.
   - The current player's turn is displayed at the top of the game board.
   - After each move, the game state will update in real-time for both players.

## Gameplay Instructions

1. **Character Types**:
   - **Pawn**: Moves one block in any direction (L, R, F, B).
   - **Hero1**: Moves two blocks straight in any direction (L, R, F, B). Can kill any opponent's character in its path.
   - **Hero2**: Moves two blocks diagonally in any direction (FL, FR, BL, BR). Can kill any opponent's character in its path.

2. **Objective**:
   The game ends when one player eliminates all of their opponent's characters.

3. **Controls**:
   - Click on a character to select it.
   - The possible move directions will appear at the bottom of the screen.
   - Click on a direction to move the character.

4. **Turn-based Gameplay**:
   Players alternate turns, and the game board updates in real time for both players.

## File Structure

```
P-Revant-Kumar-21BCE0310/
│
├── app.py                    # Main Flask application with SocketIO integration
├── templates/
│   └── index.html            # Frontend HTML file for the game
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Known Issues

- **WebSocket Connection Issues**: The WebSocket connection may remain pending due to firewall or network restrictions. Ensure that the required ports are open and no firewalls are blocking WebSocket traffic.
- **Game State Not Updating Automatically**: The game board may not update automatically in real time in some cases. This can be due to WebSocket disconnections or delayed responses.
  
## Future Improvements

- **Enhanced User Interface**: Improve the visual design and add animations for better user experience.
- **AI Opponent**: Implement a basic AI opponent for single-player mode.
- **Mobile Support**: Optimize the game for mobile devices to allow for better accessibility.
- **Game Replay**: Add functionality to replay the game after it ends, without restarting the server.

## Screenshot
![image](https://github.com/user-attachments/assets/45e734aa-b834-4b98-99b2-2228b3fe0587)

