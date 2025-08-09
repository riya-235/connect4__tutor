# Connect 4 AI Tutor

A comprehensive Connect 4 game with an AI opponent and Socratic tutoring system, built using clean MVC architecture with Pygame and Google Gemini API.

## Features

- **Fully Playable Connect 4 Game**: Classic 6x7 board with graphical interface
- **AI Opponent**: Challenging computer opponent using Minimax algorithm with alpha-beta pruning
- **Socratic AI Tutor**: Intelligent tutoring system using Google Gemini API with RAG capabilities
- **Clean Architecture**: Built using Model-View-Controller (MVC) pattern for maintainability

## Project Structure

```
connect4_tutor/
├── .env                          # Environment variables (API key)
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── README.md                    # This file
├── src/                         # Source code directory
│   ├── __init__.py
│   ├── constants.py             # Game constants and configuration
│   ├── game_model.py            # Game logic (Model)
│   ├── game_view.py             # UI rendering (View)
│   ├── game_controller.py       # Event handling (Controller)
│   ├── ai_engine.py             # AI opponent with Minimax
│   ├── llm_tutor.py             # Gemini API tutor integration
│   └── knowledge_base/          # RAG knowledge base
│       ├── center_control.md    # Center control strategy
│       └── threat_analysis.md   # Threat analysis strategy
└── assets/                      # Game assets
    └── fonts/                   # Font files
```

## Installation

1. **Clone or download the project**
2. **Create and activate virtual environment**:
   ```bash
   # Create virtual environment
   python3 -m venv connect4_tutor_env
   
   # Activate virtual environment
   source connect4_tutor_env/bin/activate  # On Linux/Mac
   # OR
   connect4_tutor_env\Scripts\activate     # On Windows
   
   # Alternative: Use the provided activation script
   ./activate_env.sh
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key** (optional for full tutor functionality):
   - Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Edit the `.env` file and replace `YOUR_API_KEY` with your actual API key

## Usage

### Running the Game

```bash
# Make sure virtual environment is activated
source connect4_tutor_env/bin/activate  # Linux/Mac
# OR
connect4_tutor_env\Scripts\activate     # Windows

# Run the game
python main.py
```

### Game Controls

- **Mouse Click**: Place your piece in a column
- **Type + Enter**: Ask the AI tutor a question
- **R Key**: Reset the game
- **Close Window**: Quit the game

### Tutor Usage

The AI tutor uses the Socratic method to help you learn Connect 4 strategies:

1. **Type a question** in the input box (e.g., "What should I do next?")
2. **Press Enter** to get a guiding response
3. **The tutor will ask questions** to help you think through the strategy yourself

### Example Questions

- "What's the best move here?"
- "How can I control the center?"
- "What threats should I look for?"
- "Why did the AI make that move?"

## Architecture

### MVC Pattern

- **Model** (`game_model.py`): Game logic, board state, win detection
- **View** (`game_view.py`): Pygame rendering, UI components
- **Controller** (`game_controller.py`): Event handling, game flow coordination

### AI Components

- **AI Engine**: Minimax algorithm with alpha-beta pruning
- **Heuristic Function**: Evaluates board positions considering center control and threats
- **Search Depth**: Configurable depth for AI difficulty

### Tutor System

- **RAG Integration**: Retrieval-Augmented Generation using knowledge base
- **Socratic Method**: Guides learning through questions rather than direct answers
- **Context Awareness**: Analyzes current board state and relevant strategies

## Configuration

### Game Constants (`src/constants.py`)

- Board dimensions (6x7)
- Screen size and colors
- AI search depth
- Font sizes

### AI Difficulty

Adjust the AI difficulty by modifying `AI_DEPTH` in `constants.py`:
- Lower values (2-3): Easier AI
- Higher values (4-5): More challenging AI

## Dependencies

- `pygame`: Game graphics and input handling
- `numpy`: Array operations for board management
- `python-dotenv`: Environment variable management
- `google-generativeai`: Google Gemini API integration

## Troubleshooting

### Common Issues

1. **"No module named 'pygame'"**
   - Install dependencies: `pip install -r requirements.txt`

2. **Tutor not responding**
   - Check your API key in the `.env` file
   - Ensure internet connection for API calls

3. **Game not starting**
   - Make sure you're running from the project root directory
   - Check Python version (3.7+ required)

### API Key Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file:
   ```
   GOOGLE_API_KEY="your_actual_api_key_here"
   ```

## Development

### Adding New Strategies

1. Create a new markdown file in `src/knowledge_base/`
2. Add keyword matching in `llm_tutor.py` `find_relevant_strategy()` method
3. Update the knowledge base loading in `llm_tutor.py`

### Extending the AI

- Modify heuristic function in `ai_engine.py` `score_position()`
- Adjust search depth in `constants.py`
- Add new evaluation criteria for different strategies

### UI Customization

- Modify colors and dimensions in `constants.py`
- Update rendering methods in `game_view.py`
- Add new UI elements in the controller

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

**Enjoy learning Connect 4 with your AI tutor!** 🎮🧠 