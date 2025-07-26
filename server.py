import socket
from _thread import *
import pickle
from game import Game  # Import the new Tic-Tac-Toe Game class

# --- Server Configuration ---
# IMPORTANT: Change this to your computer's local IPv4 address.
server_ip = "192.168.1.43"
port = 5555

# --- Server Setup ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))
    exit()
s.listen()
print("Waiting for a connection, Server Started")

# --- Game Management ---
games = {}
id_count = 0


def threaded_client(conn, player_id, game_id):
    """
    Handles communication with a single client for a Tic-Tac-Toe game.
    """
    global id_count
    # Send player ID ('0' for X, '1' for O) to the client
    conn.send(str.encode(str(player_id)))

    while True:
        try:
            data = conn.recv(4096).decode()
            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get":
                        # Data is a move like "row,col"
                        row, col = map(int, data.split(','))
                        player_symbol = "X" if player_id == 0 else "O"

                        # Only allow a player to move on their turn
                        if game.turn == player_symbol:
                            game.make_move(row, col)

                    # Send the updated game state back to the client
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print(f"Lost connection from player {player_id} in game {game_id}")
    try:
        del games[game_id]
        print("Closing Game", game_id)
    except:
        pass
    id_count -= 1
    conn.close()


# --- Main Server Loop ---
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    id_count += 1
    player = 0  # Player 0 is 'X'
    game_id = (id_count - 1) // 2

    if id_count % 2 == 1:
        # First player creates a new game
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        # Second player joins, the game is ready
        games[game_id].ready = True
        player = 1  # Player 1 is 'O'

    start_new_thread(threaded_client, (conn, player, game_id))
