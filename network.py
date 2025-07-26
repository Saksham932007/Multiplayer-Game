import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # IMPORTANT: Change this to the server's IPv4 address.
        self.server = "######server"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_id = self.connect()

    def get_player_id(self):
        """Returns the player's ID (0 or 1)."""
        return self.player_id

    def connect(self):
        """Connects to the server and returns the player ID."""
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Connection Error: {e}")
            return None

    def send(self, data):
        """
        Sends data to the server and returns the response (the game state).
        Uses pickle to handle sending/receiving the game object.
        """
        try:
            self.client.send(str.encode(data))
            # Increase buffer size for the larger game object
            return pickle.loads(self.client.recv(4096 * 2))
        except socket.error as e:
            print(e)
            return None
