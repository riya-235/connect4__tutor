import pygame
from pygame.locals import *
from game_model import GameModel
from game_view import GameView
from ai_engine import AIEngine
from llm_tutor import LLMTutor
from constants import *


class GameController:
    def __init__(self):
        """Initialize the game controller with all components."""
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Connect 4 AI Tutor")
        
        # Print screen dimensions for debugging
        print(f"Screen dimensions: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print(f"Board dimensions: {COLUMNS} columns x {ROWS} rows")
        print(f"Square size: {SQUARE_SIZE}")
        
        # Initialize MVC components
        self.game_model = GameModel()
        self.game_view = GameView(self.screen)
        
        # Initialize AI and Tutor
        self.ai_engine = AIEngine()
        self.llm_tutor = LLMTutor()
        
        # Initialize tutor-related variables
        self.user_input = ""
        self.tutor_response = ""
        self.knowledge_base = self.llm_tutor.load_knowledge_base()
        
        # Game state
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Text input state
        self.text_input_active = False
    
    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            
            elif event.type == MOUSEBUTTONDOWN:
                # Check if click is in the tutor panel area
                panel_y = (ROWS + 1) * SQUARE_SIZE
                if event.pos[1] > panel_y:
                    # Click in tutor panel - activate text input
                    self.text_input_active = True
                    print("Text input activated")
                elif not self.game_model.game_over:
                    # Handle mouse clicks for game moves
                    pos_x = event.pos[0]
                    column = int(pos_x // SQUARE_SIZE)
                    
                    # Only allow human player (Player 1) to make moves
                    if self.game_model.current_player == PLAYER_1:
                        if self.game_model.make_move(column, PLAYER_1):
                            # Check for win or draw
                            if self.game_model.check_win(PLAYER_1):
                                self.game_model.game_over = True
                                self.game_model.winner = PLAYER_1
                            elif self.game_model.is_draw():
                                self.game_model.game_over = True
                            else:
                                self.game_model.switch_player()
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Deactivate text input
                    self.text_input_active = False
                    print("Text input deactivated")
                
                elif event.key == K_RETURN and self.user_input.strip():
                    # Trigger the tutor
                    self.trigger_tutor()
                    self.text_input_active = False
                
                elif event.key == K_BACKSPACE:
                    # Handle backspace
                    self.user_input = self.user_input[:-1]
                
                elif event.key == K_r and not self.text_input_active:
                    # Reset the game (only when not typing)
                    self.game_model.reset_game()
                    self.user_input = ""
                    self.tutor_response = ""
                
                elif event.unicode.isprintable() and self.text_input_active:
                    # Handle printable characters only when text input is active
                    self.user_input += event.unicode
                    print(f"Added character: {event.unicode}, current input: {self.user_input}")
    
    def trigger_tutor(self):
        """Trigger the AI tutor with the current board state and user input."""
        if not self.user_input.strip():
            return
        
        try:
            print(f"Triggering tutor with input: {self.user_input}")
            
            # Get board state as text
            board_text = self.game_model.get_board_text()
            print(f"Board text: {board_text}")
            
            # Find relevant strategy
            relevant_strategy = self.llm_tutor.find_relevant_strategy(
                self.user_input, self.knowledge_base
            )
            print(f"Relevant strategy: {relevant_strategy[:100]}...")
            
            # Get tutor response
            self.tutor_response = self.llm_tutor.get_tutoring_response(
                board_text, relevant_strategy, self.user_input
            )
            print(f"Tutor response: {self.tutor_response[:100]}...")
            print(f"Tutor response length: {len(self.tutor_response)}")
            print(f"Tutor response type: {type(self.tutor_response)}")
            
            # Clear user input
            self.user_input = ""
            
        except Exception as e:
            print(f"Error in trigger_tutor: {e}")
            import traceback
            traceback.print_exc()
            self.tutor_response = "I'm having trouble processing your question right now. Please try again!"
            self.user_input = ""
    
    def ai_move(self):
        """Make AI move if it's the AI's turn."""
        if (not self.game_model.game_over and 
            self.game_model.current_player == PLAYER_2):
            
            # Get the best move from AI
            best_column = self.ai_engine.get_best_move(self.game_model.get_board_state())
            
            # Make the move
            if self.game_model.make_move(best_column, PLAYER_2):
                # Check for win or draw
                if self.game_model.check_win(PLAYER_2):
                    self.game_model.game_over = True
                    self.game_model.winner = PLAYER_2
                elif self.game_model.is_draw():
                    self.game_model.game_over = True
                else:
                    self.game_model.switch_player()
    
    def update_display(self):
        """Update the game display."""
        # Get current board state
        board = self.game_model.get_board_state()
        
        # Draw the board
        self.game_view.draw_board(board)
        
        # Draw tutor panel
        self.game_view.draw_tutor_panel(self.tutor_response, self.user_input, self.text_input_active)
        
        # Draw game status
        self.game_view.draw_game_status(
            self.game_model.current_player,
            self.game_model.game_over,
            self.game_model.winner
        )
        
        # Draw instructions
        self.game_view.draw_instructions()
        
        # Update the display
        pygame.display.flip()
    
    def run_game(self):
        """Main game loop."""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update display
            self.update_display()
            
            # Make AI move if it's AI's turn (only once per turn)
            if (not self.game_model.game_over and 
                self.game_model.current_player == PLAYER_2):
                # Add a small delay to make AI moves visible
                pygame.time.wait(500)  # 500ms delay
                self.ai_move()
            
            # Control frame rate
            self.clock.tick(60)
        
        # Clean up
        pygame.quit()
