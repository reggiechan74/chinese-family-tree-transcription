import os
from typing import Dict, Any, Tuple
import PIL.Image
from dotenv import load_dotenv
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from models.model_interfaces import BaseModel  # Updated import path
from config.config import get_model_init_params  # Updated import path
from models.model_factory import ModelFactory  # Updated import path
from prompts.stage_prompts import (  # Updated import path
    format_prompt,
    Stage1,
    Stage3,
    Stage4
)
from utils.token_counter import TokenTracker  # Updated import path

class LLM1Model(BaseModel):
    def __init__(self):
        # Get model config but don't initialize provider yet
        self.model_config = get_model_init_params(1)
        self._provider = None

    @property
    def provider(self):
        """Lazy load provider only when needed"""
        if self._provider is None:
            self._provider = ModelFactory.create_model(1)
        return self._provider

    def generate_transcription(self, image: PIL.Image.Image, token_tracker: TokenTracker = None) -> str:
        """
        Generate transcription from PIL Image.
        """
        try:
            system = format_prompt(
                Stage1.SYSTEM,
                model_name="LLM1"
            )

            prompt = format_prompt(Stage1.PROMPT)

            # Count input tokens
            if token_tracker:
                input_tokens, _ = self.count_tokens(system + prompt)
                
            # Extract PIL image from encoded image dict if needed
            pil_image = image.get('pil') if isinstance(image, dict) else image
            
            # Use the provider's generate_content method with system prompt
            result = self.provider.generate_content(prompt, image=pil_image, system=system)
            
            # Track token usage if token_tracker provided
            if token_tracker:
                _, output_tokens = self.count_tokens(result)
                token_tracker.add_usage(
                    stage="Stage 1: Initial Transcription",
                    model="LLM1",
                    model_name=self.model_config['name'],
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )

            return result

        except Exception as e:
            # Re-raise the provider's error to preserve the stack trace
            raise

    def analyze_context(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """
        Analyze context window data and generate recommendations.
        """
        try:
            # Get only this model's transcriptions
            stage1_transcription = context.get("LLM1's Stage 1 transcription", "")
            stage2_transcription = context.get("LLM1's Stage 2 transcription", "")
            
            system = format_prompt(
                Stage3.SYSTEM,
                model_name="LLM1"
            )

            prompt = format_prompt(
                Stage3.PROMPT,
                stage1_transcription=stage1_transcription,
                stage2_transcription=stage2_transcription
            )

            # Count input tokens
            if token_tracker:
                input_tokens, _ = self.count_tokens(system + prompt)

            # Use the provider's generate_content method with system prompt
            result = self.provider.generate_content(prompt, system=system)
            
            # Track token usage if token_tracker provided
            if token_tracker:
                _, output_tokens = self.count_tokens(result)
                token_tracker.add_usage(
                    stage="Stage 3: Initial Analysis",
                    model="LLM1",
                    model_name=self.model_config['name'],
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )

            return result
            
        except Exception as e:
            # Re-raise the provider's error to preserve the stack trace
            raise

    def comprehensive_review(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """
        Stage 4: Review all transcripts and Stage 3 analyses.
        """
        try:
            stage1_transcriptions = {
                'llm1': context.get("LLM1's Stage 1 transcription", ""),
                'llm2': context.get("LLM2's Stage 1 transcription", ""),
                'llm3': context.get("LLM3's Stage 1 transcription", "")
            }
            
            stage2_transcriptions = {
                'llm1': context.get("LLM1's Stage 2 transcription", ""),
                'llm2': context.get("LLM2's Stage 2 transcription", ""),
                'llm3': context.get("LLM3's Stage 2 transcription", "")
            }
            
            stage3_analyses = {
                'llm1': context.get("LLM1's Stage 3 Analysis and Recommendation", ""),
                'llm2': context.get("LLM2's Stage 3 Analysis and Recommendation", ""),
                'llm3': context.get("LLM3's Stage 3 Analysis and Recommendation", "")
            }
            
            system = format_prompt(
                Stage4.SYSTEM,
                model_name="LLM1"
            )

            prompt = format_prompt(
                Stage4.PROMPT,
                stage1_transcriptions=stage1_transcriptions,
                stage2_transcriptions=stage2_transcriptions,
                stage3_analyses=stage3_analyses
            )

            # Count input tokens
            if token_tracker:
                input_tokens, _ = self.count_tokens(system + prompt)

            # Use the provider's generate_content method with system prompt
            result = self.provider.generate_content(prompt, system=system)
            
            # Track token usage if token_tracker provided
            if token_tracker:
                _, output_tokens = self.count_tokens(result)
                token_tracker.add_usage(
                    stage="Stage 4: Comprehensive Review",
                    model="LLM1",
                    model_name=self.model_config['name'],
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )

            return result
            
        except Exception as e:
            # Re-raise the provider's error to preserve the stack trace
            raise
