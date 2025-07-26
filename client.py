# client.py
import pygame
from network import Network

pygame.font.init()

# --- UI Configuration ---
WIDTH = 600
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 150, 0)

# --- Fonts ---
MAIN_FONT = pygame.font.SysFont("helvetica", 160, bold=True)
INFO_FONT = pygame.font.SysFont("helvetica", 30, bold=True)
STATUS_FONT = pygame.font.SysFont("helvetica", 50, bold=True)
BUTTON_FONT = pygame.font.SysFont("helvetica", 40, bold=True)


class Button:
    """A simple button class for the 'Play Again' feature."""

    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GREEN
        self.text = text
        self.text_color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, border_radius=10)
        text_surf = BUTTON_FONT.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        win.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def draw_grid(win):
    """Draws the 3x3 Tic-Tac-Toe grid."""
    win.fill(WHITE)
    # Draw vertical lines
    pygame.draw.line(win, BLACK, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(win, BLACK, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 5)
    # Draw horizontal lines
    pygame.draw.line(win, BLACK, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), 5)
    pygame.draw.line(win, BLACK, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), 5)


def draw_pieces(win, board):
    """Draws the X's and O's on the board."""
    for row in range(3):
        for col in range(3):
            piece = board[row][col]
            if piece == 'X':
                text = MAIN_FONT.render('X', 1, BLUE)
                win.blit(text, (col * (WIDTH // 3) + 40, row * (HEIGHT // 3) + 10))
            elif piece == 'O':
                text = MAIN_FONT.render('O', 1, RED)
                win.blit(text, (col * (WIDTH // 3) + 30, row * (HEIGHT // 3) + 10))


def draw_status(win, game, player_symbol, score):
    """Draws the game status, including turns and the score."""
    # Draw Score
    score_text = f"Wins: {score['wins']} | Losses: {score['losses']} | Ties: {score['ties']}"
    score_surf = INFO_FONT.render(score_text, 1, BLACK)
    win.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 10))

    # Draw Turn/Winner Info
    if game.winner:
        if game.winner == "Tie":
            message = "It's a Tie!"
        else:
            message = f"Player {game.winner} Wins!"
    else:
        message = f"Your turn, Player {player_symbol}" if game.turn == player_symbol else f"Player {game.turn}'s Turn"

    status_text = STATUS_FONT.render(message, 1, BLACK)
    win.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, 50))


def redraw_window(win, game, player_symbol, score, play_again_button):
    """Main drawing function, now includes score and button."""
    draw_grid(win)
    draw_pieces(win, game.board)

    if not game.connected():
        text = STATUS_FONT.render("Waiting for Opponent...", 1, RED)
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    else:
        draw_status(win, game, player_symbol, score)
        if game.winner:
            play_again_button.draw(win)

    pygame.display.update()


def get_mouse_pos(pos):
    """Converts pixel coordinates to board coordinates (row, col)."""
    x, y = pos
    row = y // (HEIGHT // 3)
    col = x // (WIDTH // 3)
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()

    player_id_str = n.get_player_id()
    if player_id_str is None:
        print("Could not connect to the server. Is server.py running?")
        return

    player_id = int(player_id_str)
    player_symbol = "X" if player_id == 0 else "O"
    print(f"You are player '{player_symbol}'")

    score = {"wins": 0, "losses": 0, "ties": 0}
    score_updated = False
    play_again_button = Button(WIDTH // 2 - 125, HEIGHT // 2 + 50, 250, 80, "Play Again")

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except Exception as e:
            run = False
            print(f"Connection lost: {e}")
            break

        if game.winner and not score_updated:
            if game.winner == player_symbol:
                score["wins"] += 1
            elif game.winner == "Tie":
                score["ties"] += 1
            else:
                score["losses"] += 1
            score_updated = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if game.winner and play_again_button.is_clicked(pos):
                    n.send("reset")
                    score_updated = False
                elif game.connected() and game.winner is None and game.turn == player_symbol:
                    row, col = get_mouse_pos(pos)
                    n.send(f"{row},{col}")

        redraw_window(win, game, player_symbol, score, play_again_button)


if __name__ == "__main__":
    main()
