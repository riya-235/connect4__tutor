import pygame
from constants import *


class GameView:
    def __init__(self, screen):
        """
        Initialize the game view with the screen and fonts.
        
        Args:
            screen: The pygame screen object
        """
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.tutor_font = pygame.font.Font(None, TUTOR_FONT_SIZE)
    
    def draw_board(self, board):
        """
        Draw the Connect 4 board and pieces.
        
        Args:
            board: The current board state from GameModel
        """
        # Draw the blue background
        self.screen.fill(BLUE)
        
        # Draw the board grid
        for col in range(COLUMNS):
            for row in range(ROWS):
                pygame.draw.rect(self.screen, BLACK, 
                               (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE), 1)
                
                # Draw the pieces
                center_x = int(col * SQUARE_SIZE + SQUARE_SIZE / 2)
                center_y = int((row + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)
                
                if board[row][col] == PLAYER_1:
                    pygame.draw.circle(self.screen, RED, (center_x, center_y), PIECE_RADIUS)
                elif board[row][col] == PLAYER_2:
                    pygame.draw.circle(self.screen, YELLOW, (center_x, center_y), PIECE_RADIUS)
                else:
                    pygame.draw.circle(self.screen, BLACK, (center_x, center_y), PIECE_RADIUS)
        
        # Draw column numbers
        for col in range(COLUMNS):
            text = self.font.render(str(col), True, WHITE)
            text_rect = text.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, SQUARE_SIZE // 2))
            self.screen.blit(text, text_rect)
    
    def draw_tutor_panel(self, tutor_response, user_input, text_input_active=False):
        """
        Draw the tutor panel with text input and response area.
        
        Args:
            tutor_response (str): The tutor's response to display
            user_input (str): The current user input text
            text_input_active (bool): Whether text input is currently active
        """
        # Draw tutor panel background
        panel_y = (ROWS + 1) * SQUARE_SIZE
        pygame.draw.rect(self.screen, LIGHT_BLUE, 
                        (0, panel_y, SCREEN_WIDTH, SCREEN_HEIGHT - panel_y))
        
        # Draw input box with different border color when active
        input_box_rect = pygame.Rect(10, panel_y + 10, SCREEN_WIDTH - 20, 40)
        pygame.draw.rect(self.screen, WHITE, input_box_rect)
        border_color = RED if text_input_active else BLACK
        pygame.draw.rect(self.screen, border_color, input_box_rect, 3)
        
        # Draw input text
        if user_input:
            input_text = self.tutor_font.render(f"Ask tutor: {user_input}", True, BLACK)
            self.screen.blit(input_text, (15, panel_y + 15))
        else:
            if text_input_active:
                placeholder_text = self.tutor_font.render("Type your question here...", True, BLACK)
            else:
                placeholder_text = self.tutor_font.render("Click here and type your question, then press Enter", True, GRAY)
            self.screen.blit(placeholder_text, (15, panel_y + 15))
        
        # Draw tutor response
        print(f"Drawing tutor response: '{tutor_response}'")
        if tutor_response and tutor_response.strip():
            # Split response into lines for better display
            words = tutor_response.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if self.tutor_font.size(test_line)[0] < SCREEN_WIDTH - 20:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Display lines
            for i, line in enumerate(lines[:8]):  # Limit to 8 lines
                response_text = self.tutor_font.render(line, True, BLACK)
                self.screen.blit(response_text, (10, panel_y + 60 + i * 25))
    
    def draw_game_status(self, current_player, game_over, winner):
        """
        Draw the current game status.
        
        Args:
            current_player (int): The current player (1 or 2)
            game_over (bool): Whether the game is over
            winner (int): The winner (None if no winner)
        """
        status_y = (ROWS + 1) * SQUARE_SIZE + 250
        
        if game_over:
            if winner:
                status_text = f"Player {winner} wins!"
            else:
                status_text = "It's a draw!"
        else:
            status_text = f"Player {current_player}'s turn"
        
        status_surface = self.font.render(status_text, True, WHITE)
        status_rect = status_surface.get_rect(center=(SCREEN_WIDTH // 2, status_y))
        self.screen.blit(status_surface, status_rect)
    
    def draw_instructions(self):
        """Draw basic game instructions."""
        instructions = [
            "Click on a column to place your piece",
            "Press 'r' to reset the game",
            "Type questions for the AI tutor"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.tutor_font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 80 + i * 20))
