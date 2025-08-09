import numpy as np
from constants import ROWS, COLUMNS, PLAYER_1, PLAYER_2, EMPTY, AI_DEPTH


class AIEngine:
    def __init__(self):
        """Initialize the AI engine."""
        self.ai_player = PLAYER_2
        self.human_player = PLAYER_1
    
    def score_position(self, board, player):
        """
        Evaluate a board position for the given player.
        
        Args:
            board: The current board state
            player: The player to evaluate for
            
        Returns:
            int: Score for the position (positive favors the player)
        """
        score = 0
        
        # Check for wins
        if self.check_win(board, player):
            return 1000000  # Very high score for win
        if self.check_win(board, 3 - player):  # Opponent
            return -1000000  # Very low score for opponent win
        
        # Score center column control
        center_col = COLUMNS // 2
        center_score = 0
        for row in range(ROWS):
            if board[row][center_col] == player:
                center_score += 3
            elif board[row][center_col] == 3 - player:
                center_score -= 3
        score += center_score
        
        # Score horizontal windows
        score += self.evaluate_windows(board, player, 'horizontal')
        
        # Score vertical windows
        score += self.evaluate_windows(board, player, 'vertical')
        
        # Score diagonal windows
        score += self.evaluate_windows(board, player, 'diagonal')
        
        return score
    
    def evaluate_windows(self, board, player, direction):
        """
        Evaluate all 4-piece windows in the specified direction.
        
        Args:
            board: The board state
            player: The player to evaluate for
            direction: 'horizontal', 'vertical', or 'diagonal'
            
        Returns:
            int: Score for this direction
        """
        score = 0
        opponent = 3 - player
        
        if direction == 'horizontal':
            for row in range(ROWS):
                for col in range(COLUMNS - 3):
                    window = [board[row][col], board[row][col + 1], 
                             board[row][col + 2], board[row][col + 3]]
                    score += self.evaluate_window(window, player, opponent)
        
        elif direction == 'vertical':
            for row in range(ROWS - 3):
                for col in range(COLUMNS):
                    window = [board[row][col], board[row + 1][col], 
                             board[row + 2][col], board[row + 3][col]]
                    score += self.evaluate_window(window, player, opponent)
        
        elif direction == 'diagonal':
            # Positive diagonal
            for row in range(ROWS - 3):
                for col in range(COLUMNS - 3):
                    window = [board[row][col], board[row + 1][col + 1], 
                             board[row + 2][col + 2], board[row + 3][col + 3]]
                    score += self.evaluate_window(window, player, opponent)
            
            # Negative diagonal
            for row in range(3, ROWS):
                for col in range(COLUMNS - 3):
                    window = [board[row][col], board[row - 1][col + 1], 
                             board[row - 2][col + 2], board[row - 3][col + 3]]
                    score += self.evaluate_window(window, player, opponent)
        
        return score
    
    def evaluate_window(self, window, player, opponent):
        """
        Evaluate a 4-piece window.
        
        Args:
            window: List of 4 pieces
            player: The player to evaluate for
            opponent: The opponent player
            
        Returns:
            int: Score for this window
        """
        player_count = window.count(player)
        opponent_count = window.count(opponent)
        empty_count = window.count(EMPTY)
        
        if opponent_count == 0:
            if player_count == 4:
                return 100  # Win
            elif player_count == 3:
                return 5  # Strong threat
            elif player_count == 2:
                return 2  # Potential threat
            elif player_count == 1:
                return 1  # Minor advantage
        
        return 0  # No advantage or blocked
    
    def check_win(self, board, player):
        """
        Check if the given player has won.
        
        Args:
            board: The board state
            player: The player to check
            
        Returns:
            bool: True if the player has won
        """
        # Check horizontal
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if (board[row][col] == player and
                    board[row][col + 1] == player and
                    board[row][col + 2] == player and
                    board[row][col + 3] == player):
                    return True
        
        # Check vertical
        for row in range(ROWS - 3):
            for col in range(COLUMNS):
                if (board[row][col] == player and
                    board[row + 1][col] == player and
                    board[row + 2][col] == player and
                    board[row + 3][col] == player):
                    return True
        
        # Check diagonal (positive slope)
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if (board[row][col] == player and
                    board[row + 1][col + 1] == player and
                    board[row + 2][col + 2] == player and
                    board[row + 3][col + 3] == player):
                    return True
        
        # Check diagonal (negative slope)
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if (board[row][col] == player and
                    board[row - 1][col + 1] == player and
                    board[row - 2][col + 2] == player and
                    board[row - 3][col + 3] == player):
                    return True
        
        return False
    
    def get_valid_locations(self, board):
        """
        Get all valid column locations for moves.
        
        Args:
            board: The board state
            
        Returns:
            list: List of valid column indices
        """
        valid_locations = []
        for col in range(COLUMNS):
            if board[0][col] == EMPTY:
                valid_locations.append(col)
        return valid_locations
    
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: The board state
            depth: Current depth in the search tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: True if maximizing player's turn
            
        Returns:
            tuple: (score, column) for the best move
        """
        valid_locations = self.get_valid_locations(board)
        
        # Terminal conditions
        if self.check_win(board, self.ai_player):
            return (1000000, None)
        elif self.check_win(board, self.human_player):
            return (-1000000, None)
        elif len(valid_locations) == 0:
            return (0, None)
        elif depth == 0:
            return (self.score_position(board, self.ai_player), None)
        
        if maximizing_player:
            value = float('-inf')
            column = valid_locations[0]
            
            for col in valid_locations:
                # Make a copy of the board and make the move
                temp_board = board.copy()
                self.drop_piece(temp_board, col, self.ai_player)
                
                new_score, _ = self.minimax(temp_board, depth - 1, alpha, beta, False)
                
                if new_score > value:
                    value = new_score
                    column = col
                
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            
            return (value, column)
        
        else:
            value = float('inf')
            column = valid_locations[0]
            
            for col in valid_locations:
                # Make a copy of the board and make the move
                temp_board = board.copy()
                self.drop_piece(temp_board, col, self.human_player)
                
                new_score, _ = self.minimax(temp_board, depth - 1, alpha, beta, True)
                
                if new_score < value:
                    value = new_score
                    column = col
                
                beta = min(beta, value)
                if alpha >= beta:
                    break
            
            return (value, column)
    
    def drop_piece(self, board, column, player):
        """
        Drop a piece in the specified column.
        
        Args:
            board: The board to modify
            column: The column to drop the piece in
            player: The player making the move
        """
        for row in range(ROWS - 1, -1, -1):
            if board[row][column] == EMPTY:
                board[row][column] = player
                break
    
    def get_best_move(self, board):
        """
        Get the best move for the AI player.
        
        Args:
            board: The current board state
            
        Returns:
            int: The best column to move in
        """
        _, column = self.minimax(board, AI_DEPTH, float('-inf'), float('inf'), True)
        return column
