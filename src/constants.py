# Game Board Constants
ROWS = 6
COLUMNS = 7
SQUARE_SIZE = 100
PIECE_RADIUS = int(SQUARE_SIZE / 2 - 5)

# Screen Dimensions
SCREEN_WIDTH = COLUMNS * SQUARE_SIZE
SCREEN_HEIGHT = (ROWS + 1) * SQUARE_SIZE + 300  # Extra space for tutor panel and status

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)

# Player Constants
PLAYER_1 = 1
PLAYER_2 = 2
EMPTY = 0

# AI Constants
AI_DEPTH = 4  # Depth for minimax algorithm

# Font Settings
FONT_SIZE = 36
TUTOR_FONT_SIZE = 24
