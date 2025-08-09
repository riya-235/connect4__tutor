import numpy as np
from constants import ROWS, COLUMNS, PLAYER_1, PLAYER_2, EMPTY


class GameModel:
    def __init__(self):
        """Initialize the game model with a 6x7 board and set current player to 1."""
        self.board = np.zeros((ROWS, COLUMNS), dtype=int)
        self.current_player = PLAYER_1
        self.game_over = False
        self.winner = None
    
    def make_move(self, column, player):
        """
        Place a piece in the specified column for the given player.
        
        Args:
            column (int): The column to place the piece (0-6)
            player (int): The player making the move (1 or 2)
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        if not self.is_valid_location(column):
            return False
        
        # Find the lowest empty row in the column
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][column] == EMPTY:
                self.board[row][column] = player
                return True
        return False
    
    def is_valid_location(self, column):
        """
        Check if a column is not full and is within bounds.
        
        Args:
            column (int): The column to check
            
        Returns:
            bool: True if the column is valid for a move
        """
        if column < 0 or column >= COLUMNS:
            return False
        return self.board[0][column] == EMPTY
    
    def check_win(self, player):
        """
        Check for a win by the specified player.
        
        Args:
            player (int): The player to check for a win
            
        Returns:
            bool: True if the player has won
        """
        # Check horizontal
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if (self.board[row][col] == player and
                    self.board[row][col + 1] == player and
                    self.board[row][col + 2] == player and
                    self.board[row][col + 3] == player):
                    return True
        
        # Check vertical
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if (self.board[row][col] == player and
                    self.board[row + 1][col] == player and
                    self.board[row + 2][col] == player and
                    self.board[row + 3][col] == player):
                    return True
        
        # Check diagonal (positive slope)
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if (self.board[row][col] == player and
                    self.board[row + 1][col + 1] == player and
                    self.board[row + 2][col + 2] == player and
                    self.board[row + 3][col + 3] == player):
                    return True
        
        # Check diagonal (negative slope)
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if (self.board[row][col] == player and
                    self.board[row - 1][col + 1] == player and
                    self.board[row - 2][col + 2] == player and
                    self.board[row - 3][col + 3] == player):
                    return True
        
        return False
    
    def is_draw(self):
        """
        Check if the game is a draw (board is full).
        
        Returns:
            bool: True if the game is a draw
        """
        return np.all(self.board[0] != EMPTY)
    
    def get_board_state(self):
        """
        Get the current board state as a 2D array.
        
        Returns:
            numpy.ndarray: The current board state
        """
        return self.board.copy()
    
    def switch_player(self):
        """Switch the current player."""
        self.current_player = PLAYER_2 if self.current_player == PLAYER_1 else PLAYER_1
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = np.zeros((ROWS, COLUMNS), dtype=int)
        self.current_player = PLAYER_1
        self.game_over = False
        self.winner = None
    
    def get_board_text(self):
        """
        Convert the board to a text representation for the tutor.
        
        Returns:
            str: Text representation of the board
        """
        text = "Current Board State:\n"
        for row in range(ROWS):
            text += "|"
            for col in range(COLUMNS):
                if self.board[row][col] == EMPTY:
                    text += " "
                elif self.board[row][col] == PLAYER_1:
                    text += "X"
                else:
                    text += "O"
                text += "|"
            text += "\n"
        text += "+" + "-" * (COLUMNS * 2 - 1) + "+\n"
        text += " 0 1 2 3 4 5 6\n"
        return text
