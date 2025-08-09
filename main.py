#!/usr/bin/env python3
"""
Connect 4 AI Tutor - Main Entry Point

A comprehensive Connect 4 game with AI opponent and tutoring system.
Built using MVC architecture with Pygame for the GUI and Google Gemini API for tutoring.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game_controller import GameController


def main():
    """Main function to start the Connect 4 AI Tutor game."""
    print("Starting Connect 4 AI Tutor...")
    print("Features:")
    print("- Play Connect 4 against an AI opponent")
    print("- Get strategic hints from an AI tutor")
    print("- Learn Connect 4 strategies through Socratic questioning")
    print("\nInstructions:")
    print("- Click on a column to place your piece")
    print("- Type questions for the AI tutor and press Enter")
    print("- Press 'r' to reset the game")
    print("- Close the window to quit")
    print("\nNote: Set your Google Gemini API key in the .env file for full tutor functionality.")
    
    try:
        # Create and run the game controller
        controller = GameController()
        controller.run_game()
    except Exception as e:
        print(f"Error starting the game: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
