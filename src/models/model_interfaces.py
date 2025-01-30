from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import PIL.Image
import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from utils.token_counter import TokenTracker  # Updated import path

class BaseModel(ABC):
    """Base interface for LLM models that handle transcription and analysis."""
    
    @abstractmethod
    def generate_transcription(self, image: PIL.Image.Image, token_tracker: TokenTracker = None) -> str:
        """Generate transcription from PIL Image."""
        pass

    @abstractmethod
    def analyze_context(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """Analyze context window data and generate recommendations."""
        pass

    @abstractmethod
    def comprehensive_review(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """Stage 4: Review all transcripts and Stage 3 analyses."""
        pass

    def count_tokens(self, text: str) -> Tuple[int, int]:
        """
        Count input and output tokens for the given text.
        Should be implemented by each provider's specific tokenizer.
        Returns (input_tokens, output_tokens)
        """
        # Default implementation - override in provider-specific models
        # Rough estimation: 1 token ≈ 4 characters
        return (len(text) // 4, len(text) // 4)

class FinalStageModel(ABC):
    """Interface for LLM4 that handles final stages."""
    
    @abstractmethod
    def generate_final_transcription(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """Stage 5: Generate final authoritative transcription based on Stage 4 analyses."""
        pass

    @abstractmethod
    def add_punctuation(self, text: str, token_tracker: TokenTracker = None) -> str:
        """Stage 6: Add appropriate Chinese punctuation to the text."""
        pass

    @abstractmethod
    def translate_to_english(self, text: str, token_tracker: TokenTracker = None) -> str:
        """Stage 7: Translate Chinese text to English."""
        pass

    @abstractmethod
    def generate_commentary(self, text: str, token_tracker: TokenTracker = None) -> str:
        """Stage 8: Generate historical commentary on the English translation."""
        pass

    def count_tokens(self, text: str) -> Tuple[int, int]:
        """
        Count input and output tokens for the given text.
        Should be implemented by each provider's specific tokenizer.
        Returns (input_tokens, output_tokens)
        """
        # Default implementation - override in provider-specific models
        # Rough estimation: 1 token ≈ 4 characters
        return (len(text) // 4, len(text) // 4)
