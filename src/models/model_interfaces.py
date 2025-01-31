"""
Base interfaces for LLM model implementations.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from utils.token_counter import TokenTracker

class BaseModel(ABC):
    """Base class for all LLM models."""
    
    MIN_STAGE = 1
    MAX_STAGE = 8
    MAX_MODEL_NUM = 3
    
    def __init__(self, provider: str, model_name: str, stage: int, model_num: int):
        """
        Initialize model with provider and model name.
        
        Args:
            provider: Name of the model provider (e.g., 'google', 'openai')
            model_name: Name of the specific model
            stage: Stage number (1-8)
            model_num: Model number within the stage (1-3)
            
        Raises:
            ValueError: If stage or model_num is invalid
        """
        if not isinstance(stage, int) or stage < self.MIN_STAGE or stage > self.MAX_STAGE:
            raise ValueError(f"Invalid stage number. Must be between {self.MIN_STAGE} and {self.MAX_STAGE}")
            
        if not isinstance(model_num, int) or model_num < 1 or model_num > self.MAX_MODEL_NUM:
            raise ValueError(f"Invalid model number. Must be between 1 and {self.MAX_MODEL_NUM}")
            
        if not provider or not isinstance(provider, str):
            raise ValueError("Provider must be a non-empty string")
            
        if not model_name or not isinstance(model_name, str):
            raise ValueError("Model name must be a non-empty string")
        
        self.provider = provider
        self.model_name = model_name
        self.stage = stage
        self.model_num = model_num

class TranscriptionModel(BaseModel):
    """Base class for models that can transcribe Chinese text from images."""
    
    @abstractmethod
    def generate_transcription(self, image_base64: str, token_tracker: TokenTracker = None) -> str:
        """
        Generate transcription from base64 encoded image.
        
        Args:
            image_base64: Base64 encoded image string
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            str: Generated transcription
            
        Raises:
            ValueError: If stage is not a transcription stage (1-2)
        """
        if self.stage > 2:
            raise ValueError(f"Stage {self.stage} is not a transcription stage. Only stages 1-2 can transcribe.")
        return ""  # Base implementation for inheritance

class ReviewModel(TranscriptionModel):
    """Base class for models that can review and analyze transcriptions."""
    
    @abstractmethod
    def analyze_context(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """
        Compare and analyze Stage 1 and Stage 2 transcriptions for this model's number.
        
        Each Stage 3 model analyzes the transcriptions from Stage 1 and Stage 2
        that were produced by the model with the same model number. For example,
        Stage 3 Model 1 analyzes Stage 1 Model 1 and Stage 2 Model 1 transcriptions.
        
        Args:
            context: Context window containing Stage 1 and 2 transcriptions
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            str: Analysis, recommendations, and suggested transcription
            
        Raises:
            ValueError: If stage is not stage 3
        """
        if self.stage != 3:
            raise ValueError("analyze_context is only valid for stage 3")
        return ""  # Base implementation for inheritance
    
    @abstractmethod
    def comprehensive_review(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """
        Review all Stage 3 analyses and recommend a transcription.
        
        Each Stage 4 model reviews all Stage 3 analyses to understand different
        perspectives and recommendations. Based on this comprehensive review,
        each model provides its own recommendation for the final transcription.
        
        Args:
            context: Context window containing all Stage 3 reviews
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            str: Comprehensive review with transcription recommendation
            
        Raises:
            ValueError: If stage is not stage 4
        """
        if self.stage != 4:
            raise ValueError("comprehensive_review is only valid for stage 4")
        return ""  # Base implementation for inheritance

class FinalStageModel(ReviewModel):
    """Base class for models that handle final processing stages."""
    
    @abstractmethod
    def generate_final_transcription(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """
        Generate final authoritative transcription based on Stage 4 reviews.
        
        This method synthesizes the reviews and recommendations from Stage 4 to create
        a single, authoritative transcription. It considers consensus points,
        justified corrections, and recommendations from the expert reviews.
        
        Args:
            context: Context window containing Stage 4 reviews and recommendations
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            str: Final authoritative transcription
            
        Raises:
            ValueError: If stage is not stage 5
        """
        if self.stage != 5:
            raise ValueError("generate_final_transcription is only valid for stage 5")
        return ""  # Base implementation for inheritance
    
    @abstractmethod
    def add_punctuation(self, text: str, token_tracker: TokenTracker = None) -> str:
        """
        Add appropriate Chinese punctuation to text.
        
        Args:
            text: Chinese text without punctuation
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            str: Text with punctuation added
            
        Raises:
            ValueError: If stage is not stage 6
        """
        if self.stage != 6:
            raise ValueError("add_punctuation is only valid for stage 6")
        return ""  # Base implementation for inheritance
    
    @abstractmethod
    def translate_to_english(self, text: str, token_tracker: TokenTracker = None) -> str:
        """
        Translate Chinese text to English.
        
        Args:
            text: Chinese text to translate
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            str: English translation
            
        Raises:
            ValueError: If stage is not stage 7
        """
        if self.stage != 7:
            raise ValueError("translate_to_english is only valid for stage 7")
        return ""  # Base implementation for inheritance
    
    @abstractmethod
    def generate_commentary(self, text: str, token_tracker: TokenTracker = None) -> str:
        """
        Generate historical commentary on the text.
        
        Args:
            text: Text to generate commentary for
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            str: Historical commentary
            
        Raises:
            ValueError: If stage is not stage 8
        """
        if self.stage != 8:
            raise ValueError("generate_commentary is only valid for stage 8")
        return ""  # Base implementation for inheritance
