class Game:
    """
    Manages the state of a single Tic-Tac-Toe game.
    """

    def __init__(self, id):
        self.id = id
        self.ready = False
        # The board is a 3x3 grid. ' ' represents an empty square.
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.turn = "X"  # Player 'X' always starts
        self.winner = None  # Can be 'X', 'O', or 'Tie'
        self.moves = 0

    def make_move(self, row, col):
        """
        Places a piece on the board if the move is valid.
        Returns True if the move was successful, False otherwise.
        """
        if self.board[row][col] == ' ':
            self.board[row][col] = self.turn
            self.moves += 1
            self.check_winner()
            # Switch turns
            self.turn = "O" if self.turn == "X" else "X"
            return True
        return False

    def check_winner(self):
        """
        Checks for a winner or a tie condition.
        Updates self.winner if the game has ended.
        """
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                self.winner = self.board[i][0]
                return
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                self.winner = self.board[0][i]
                return

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.winner = self.board[0][0]
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.winner = self.board[0][2]
            return

        # Check for a tie
        if self.moves == 9 and self.winner is None:
            self.winner = "Tie"

    def get_board(self):
        """Returns the current board state."""
        return self.board

    def connected(self):
        """Checks if both players are connected."""
        return self.ready

    def reset(self):
        """Resets the game to its initial state."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.turn = "X"
        self.winner = None
        self.moves = 0
