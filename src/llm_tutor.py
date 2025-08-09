import os
import google.generativeai as genai
from dotenv import load_dotenv


class LLMTutor:
    def __init__(self):
        """Initialize the LLM tutor with Gemini API configuration."""
        load_dotenv()
        
        # Configure the Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key or api_key == "YOUR_API_KEY":
            print("Warning: Please set your Google Gemini API key in the .env file")
            self.model = None
            self.chat = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.chat = self.model.start_chat(history=[])
    
    def get_tutoring_response(self, board_state_text, relevant_strategy, user_query):
        """
        Get a tutoring response from the Gemini API.
        
        Args:
            board_state_text (str): Text representation of the current board
            relevant_strategy (str): Relevant strategy content from knowledge base
            user_query (str): The user's question
            
        Returns:
            str: The tutor's response
        """
        if not self.chat:
            # Provide a simple fallback response for testing
            if "center" in user_query.lower() or "middle" in user_query.lower():
                return "Consider placing your piece in the center column (column 3) - it gives you the most opportunities to create winning combinations!"
            elif "threat" in user_query.lower() or "block" in user_query.lower():
                return "Look for any three-in-a-row patterns that your opponent could complete. Blocking these threats is crucial!"
            else:
                return "Try to control the center and look for opportunities to create multiple threats simultaneously!"
        
        # Construct the Socratic prompt
        prompt = f"""
You are a helpful Connect 4 tutor using the Socratic method. Your goal is to guide the student to discover the answer themselves rather than giving direct answers.

Current board state:
{board_state_text}

Relevant strategy information:
{relevant_strategy}

Student's question: {user_query}

Instructions:
1. Analyze the board state and the student's question
2. Consider the relevant strategy information provided
3. Instead of giving a direct answer, ask a guiding question that will help the student think through the problem
4. Your response should be encouraging and educational
5. Keep your response concise (2-3 sentences maximum)
6. Focus on helping the student develop strategic thinking skills

Remember: You are a tutor, not a coach. Guide the student to discover the answer through thoughtful questioning.
"""
        
        try:
            print(f"Sending prompt to Gemini API...")
            response = self.chat.send_message(prompt)
            print(f"Received response from API")
            
            # Ensure we get a string response
            if hasattr(response, 'text'):
                return str(response.text)
            else:
                return str(response)
                
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            # Return a safe fallback response instead of crashing
            return "I'm having trouble connecting to the AI tutor right now. Try asking about center control or threat analysis strategies!"
    
    def load_knowledge_base(self):
        """
        Load the knowledge base content.
        
        Returns:
            dict: Dictionary with strategy names as keys and content as values
        """
        knowledge_base = {}
        
        try:
            # Try different possible paths for the knowledge base files
            possible_paths = [
                'src/knowledge_base/center_control.md',
                'knowledge_base/center_control.md',
                '../knowledge_base/center_control.md'
            ]
            
            center_control_content = None
            for path in possible_paths:
                try:
                    with open(path, 'r') as f:
                        center_control_content = f.read()
                        print(f"Successfully loaded center control from: {path}")
                        break
                except FileNotFoundError:
                    continue
            
            if center_control_content:
                knowledge_base['center_control'] = center_control_content
            else:
                knowledge_base['center_control'] = 'Controlling the center column is important in Connect 4.'
            
            # Try different possible paths for threat analysis
            possible_paths = [
                'src/knowledge_base/threat_analysis.md',
                'knowledge_base/threat_analysis.md',
                '../knowledge_base/threat_analysis.md'
            ]
            
            threat_analysis_content = None
            for path in possible_paths:
                try:
                    with open(path, 'r') as f:
                        threat_analysis_content = f.read()
                        print(f"Successfully loaded threat analysis from: {path}")
                        break
                except FileNotFoundError:
                    continue
            
            if threat_analysis_content:
                knowledge_base['threat_analysis'] = threat_analysis_content
            else:
                knowledge_base['threat_analysis'] = 'Threats are potential winning combinations that need to be blocked.'
                
        except Exception as e:
            print(f"Warning: Could not load knowledge base files: {e}")
            knowledge_base = {
                'center_control': 'Controlling the center column is important in Connect 4.',
                'threat_analysis': 'Threats are potential winning combinations that need to be blocked.'
            }
        
        return knowledge_base
    
    def find_relevant_strategy(self, user_input, knowledge_base):
        """
        Find the most relevant strategy based on user input.
        
        Args:
            user_input (str): The user's question
            knowledge_base (dict): The loaded knowledge base
            
        Returns:
            str: The most relevant strategy content
        """
        user_input_lower = user_input.lower()
        
        # Simple keyword matching
        if any(word in user_input_lower for word in ['center', 'middle', 'column 3', 'column 4']):
            return knowledge_base.get('center_control', 'Center control is important.')
        
        elif any(word in user_input_lower for word in ['threat', 'block', 'defend', 'three', 'winning']):
            return knowledge_base.get('threat_analysis', 'Threat analysis is crucial.')
        
        else:
            # Default to center control if no specific keywords found
            return knowledge_base.get('center_control', 'Center control is important.')
