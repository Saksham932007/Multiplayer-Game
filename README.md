# Real-Time Multiplayer Tic-Tac-Toe
  <!-- You can replace this with a screenshot of your game! -->

A classic game of Tic-Tac-Toe built with Python and Pygame, featuring a client-server architecture for real-time, two-player gameplay over a local network.

## Features

- **Real-Time Multiplayer:** Play against another person on the same local network.
- **Graphical Interface:** A clean and intuitive UI built with Pygame.
- **Persistent Scoring:** The client keeps track of wins, losses, and ties for the duration of the session.
- **"Play Again" Functionality:** Seamlessly start a new match after a game concludes without restarting the application.
- **Separation of Concerns:** The project is logically structured into a game engine, a server, a client, and a networking module.

## How to Run

Follow these steps to get the game running between two computers on the same network.

### Prerequisites

- **Python 3:** Make sure Python 3 is installed on your system.
- **Pygame:** Install the Pygame library by running the following command in your terminal:

pip install pygame


### 1. Download the Code

Clone this repository or download the source code files (`server.py`, `client.py`, `game.py`, `network.py`) into a single folder on your computer.

### 2. Configure the Server IP Address

This is the most important step for enabling network play.

- **Find the Server's Local IP:** On the computer that will act as the server, find its local IPv4 address.
- **On Windows:** Open Command Prompt (`cmd`) and type `ipconfig`.
- **On macOS/Linux:** Open a terminal and type `ifconfig` or `ip addr`.
- The address will likely look like `192.168.x.x` or `10.0.x.x`.

- **Update the Code:** Open `server.py` and `network.py` in a text editor and change the IP address variable to the one you just found.

- In `server.py`:
  ```python
  server_ip = "YOUR_LOCAL_IP_ADDRESS_HERE" 
  ```
- In `network.py`:
  ```python
  self.server = "YOUR_LOCAL_IP_ADDRESS_HERE"
  ```
**Note:** The IP address must be identical in both files.

### 3. Run the Server

On the server computer, open a terminal, navigate to the project folder, and run:


python server.py


You should see the message: `Waiting for a connection, Server Started`. Leave this terminal running.

### 4. Run the Clients

- On the first player's computer (this can be the same computer as the server), open a **new** terminal, navigate to the project folder, and run:

python client.py

- A game window will open, showing "Waiting for Opponent...".

- On the second player's computer, do the same: open a terminal, navigate to the project folder, and run:

python client.py

- Once the second client connects, the game will start on both screens!

## File Structure

- **`server.py`**: Handles all incoming connections, manages game sessions, and relays moves between the two players.
- **`client.py`**: The main application for the players. It renders the game board, handles user input, and communicates with the server.
- **`game.py`**: Contains the core game logic in the `Game` class. It manages the board state, checks for wins/ties, and enforces the rules.
- **`network.py`**: A simple networking class that abstracts away the socket communication, making it easy for the client to send and receive game data.

## Technologies Used

- **Python 3**
- **Pygame** for the graphical interface and user input.
- **Socket** for low-level networking and communication between the client and server.
- **Pickle** for serializing and deserializing game objects to send over the network.
