import os
from typing import Dict, Any, Tuple
import PIL.Image
from dotenv import load_dotenv
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from models.model_interfaces import FinalStageModel  # Updated import path
from config.config import get_model_init_params  # Updated import path
from models.model_factory import ModelFactory  # Updated import path
from prompts.stage_prompts import (  # Updated import path
    format_prompt,
    Stage5,
    Stage6,
    Stage7,
    Stage8
)
from utils.token_counter import TokenTracker  # Updated import path

class LLM4Model(FinalStageModel):
    def __init__(self):
        # Get model config but don't initialize provider yet
        self.model_config = get_model_init_params(4)
        self._provider = None

    @property
    def provider(self):
        """Lazy load provider only when needed"""
        if self._provider is None:
            self._provider = ModelFactory.create_model(4)
        return self._provider

    def generate_transcription(self, image, token_tracker=None):
        """Not used by LLM4"""
        raise NotImplementedError("LLM4 does not handle transcription")

    def analyze_context(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """Not used by LLM4"""
        raise NotImplementedError("LLM4 does not handle analysis")

    def generate_final_transcription(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """
        Stage 5: Generate final authoritative transcription based on Stage 4 analyses.
        """
        try:
            # Extract just the final recommendations from each Stage 4 review
            stage4_analyses = {}
            for model_num in [1, 2, 3]:
                review = context.get(f"LLM{model_num}'s Stage 4 Comprehensive Review", "")
                # Extract just the Final Character Recommendations section
                if "Final Character Recommendations" in review:
                    recommendations = review.split("Final Character Recommendations")[1]
                    if "Confidence Assessment" in recommendations:
                        recommendations = recommendations.split("Confidence Assessment")[0]
                    stage4_analyses[f'llm{model_num}'] = recommendations.strip()
                else:
                    stage4_analyses[f'llm{model_num}'] = review
            
            system = format_prompt(
                Stage5.SYSTEM,
                model_name="LLM4"
            )

            prompt = format_prompt(
                Stage5.PROMPT,
                stage4_analyses=stage4_analyses
            )

            # Count tokens before API call
            if token_tracker:
                input_tokens, _ = self.count_tokens(system + prompt)
            
            result = self.provider.generate_content(prompt, system=system)
            
            # Track token usage if token_tracker provided
            if token_tracker:
                _, output_tokens = self.count_tokens(result)
                token_tracker.add_usage(
                    stage="Stage 5: Final Transcription",
                    model="LLM4",
                    model_name=self.model_config['name'],
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )
            
            return result
            
        except Exception as e:
            raise Exception(f"Error generating final transcription: {str(e)}")

    def add_punctuation(self, text: str, token_tracker: TokenTracker = None) -> str:
        """
        Stage 6: Add appropriate Chinese punctuation to the text.
        """
        try:
            system = format_prompt(
                Stage6.SYSTEM,
                model_name="LLM4"
            )

            prompt = format_prompt(
                Stage6.PROMPT,
                text=text
            )

            # Count tokens before API call
            if token_tracker:
                input_tokens, _ = self.count_tokens(system + prompt)
            
            result = self.provider.generate_content(prompt, system=system)
            
            # Track token usage if token_tracker provided
            if token_tracker:
                _, output_tokens = self.count_tokens(result)
                token_tracker.add_usage(
                    stage="Stage 6: Punctuation",
                    model="LLM4",
                    model_name=self.model_config['name'],
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )
            
            return result
            
        except Exception as e:
            raise Exception(f"Error adding punctuation: {str(e)}")

    def translate_to_english(self, text: str, token_tracker: TokenTracker = None) -> str:
        """
        Stage 7: Translate Chinese text to English.
        """
        try:
            system = format_prompt(
                Stage7.SYSTEM,
                model_name="LLM4"
            )

            prompt = format_prompt(
                Stage7.PROMPT,
                text=text
            )

            # Count tokens before API call
            if token_tracker:
                input_tokens, _ = self.count_tokens(system + prompt)
            
            result = self.provider.generate_content(prompt, system=system)
            
            # Track token usage if token_tracker provided
            if token_tracker:
                _, output_tokens = self.count_tokens(result)
                token_tracker.add_usage(
                    stage="Stage 7: Translation",
                    model="LLM4",
                    model_name=self.model_config['name'],
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )
            
            return result
            
        except Exception as e:
            raise Exception(f"Error during translation: {str(e)}")

    def generate_commentary(self, text: str, token_tracker: TokenTracker = None) -> str:
        """
        Stage 8: Generate historical commentary on the English translation.
        """
        try:
            system = format_prompt(
                Stage8.SYSTEM,
                model_name="LLM4"
            )

            prompt = format_prompt(
                Stage8.PROMPT,
                text=text
            )

            # Count tokens before API call
            if token_tracker:
                input_tokens, _ = self.count_tokens(system + prompt)
            
            result = self.provider.generate_content(prompt, system=system)
            
            # Track token usage if token_tracker provided
            if token_tracker:
                _, output_tokens = self.count_tokens(result)
                token_tracker.add_usage(
                    stage="Stage 8: Historical Commentary",
                    model="LLM4",
                    model_name=self.model_config['name'],
                    input_tokens=input_tokens,
                    output_tokens=output_tokens
                )
            
            return result
            
        except Exception as e:
            raise Exception(f"Error generating commentary: {str(e)}")
