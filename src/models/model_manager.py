"""
Model Manager for coordinating all LLM interactions.
"""
from typing import Dict, Any, List, TYPE_CHECKING, Optional
import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

if TYPE_CHECKING:
    from models.model_interfaces import TranscriptionModel, ReviewModel, FinalStageModel
    from utils.token_counter import TokenTracker

from models.model_factory import ModelFactory
from config.config import get_model_init_params
from utils.token_counter import count_tokens

class ModelManager:
    """Manager class for coordinating model interactions across stages."""
    
    def __init__(self):
        # Shared context window to store all data
        self.context_window: Dict[str, Any] = {}
        
        # Token tracker (lazy loaded)
        self._token_tracker = None
        
        # Track active models for cleanup
        self._active_models = []
        
        # Processing metadata
        self.start_time = None
        self.output_dir = None
        self.timestamp = None

    def _initialize_run(self, image_path: str):
        """Initialize run-specific variables."""
        self.start_time = time.time()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        self.output_dir = os.path.join(current_dir, 'output', f"run_{self.timestamp}")
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_processing_time(self) -> float:
        """Get current processing time."""
        return time.time() - self.start_time

    def _save_stage_output(self, stage_num: int, content: str, next_stage_data: Dict[str, str] = None):
        """Save stage output to a markdown file."""
        if not self.output_dir or not self.timestamp:
            raise RuntimeError("Output directory not initialized")
            
        filename = f"Stage{stage_num}_{self.timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        # Add header
        header = f"# Stage {stage_num} Output\n\n"
        header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += f"Processing Time: {self._get_processing_time():.2f} seconds\n\n"
        
        content = header + content
        
        if next_stage_data:
            content += "\n## Data Passed to Next Stage\n\n"
            total_tokens = 0
            for key, data in next_stage_data.items():
                token_count = count_tokens(data)
                total_tokens += token_count
                content += f"### {key}\n"
                content += f"Token count: {token_count:,} tokens\n"
                content += f"```\n{data}\n```\n\n"
            content += f"\nTotal tokens being passed to next stage: {total_tokens:,} tokens\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"- Stage {stage_num} output saved to: {filepath}")

    @property
    def token_tracker(self):
        """Lazy load token tracker"""
        if self._token_tracker is None:
            from utils.token_counter import TokenTracker
            self._token_tracker = TokenTracker()
        return self._token_tracker

    @token_tracker.setter
    def token_tracker(self, tracker):
        """Allow setting external token tracker"""
        self._token_tracker = tracker

    def _get_model_info(self, stage: int, model_num: int) -> str:
        """Get formatted model info string."""
        config = self._get_model_config(stage, model_num)
        return f"Stage {stage} Model {model_num} - {config['provider'].title()} {config['name']}"

    def _get_model_config(self, stage: int, model_num: int) -> Dict[str, Any]:
        """Get model configuration for a specific stage and model number."""
        return get_model_init_params(stage, model_num)

    def _get_stage_dependencies(self, stage: int, model_num: int) -> List[str]:
        """Get required keys for a stage based on its dependencies."""
        if stage == 3:
            # Stage 3: Each model needs transcriptions from corresponding model numbers
            stage1_config = get_model_init_params(1, model_num)
            stage2_config = get_model_init_params(2, model_num)
            return [
                f"Stage 1 Model {model_num} - {stage1_config['provider'].title()} {stage1_config['name']} Transcription",
                f"Stage 2 Model {model_num} - {stage2_config['provider'].title()} {stage2_config['name']} Transcription"
            ]
        elif stage == 4:
            # Stage 4: Each model needs all Stage 3 reviews
            return [
                f"Stage 3 Model 1 - {get_model_init_params(3, 1)['provider'].title()} {get_model_init_params(3, 1)['name']} Review",
                f"Stage 3 Model 2 - {get_model_init_params(3, 2)['provider'].title()} {get_model_init_params(3, 2)['name']} Review",
                f"Stage 3 Model 3 - {get_model_init_params(3, 3)['provider'].title()} {get_model_init_params(3, 3)['name']} Review"
            ]
        elif stage == 5:
            # Stage 5: Needs all Stage 4 reviews
            return [
                f"Stage 4 Model 1 - {get_model_init_params(4, 1)['provider'].title()} {get_model_init_params(4, 1)['name']} Review",
                f"Stage 4 Model 2 - {get_model_init_params(4, 2)['provider'].title()} {get_model_init_params(4, 2)['name']} Review",
                f"Stage 4 Model 3 - {get_model_init_params(4, 3)['provider'].title()} {get_model_init_params(4, 3)['name']} Review"
            ]
        elif stage == 6:
            # Stage 6: Needs Stage 5 final transcription
            stage5_config = get_model_init_params(5, 1)
            return [f"Stage 5 Model 1 - {stage5_config['provider'].title()} {stage5_config['name']} Final Transcription"]
        elif stage == 7:
            # Stage 7: Needs Stage 6 punctuated transcription
            stage6_config = get_model_init_params(6, 1)
            return [f"Stage 6 Model 1 - {stage6_config['provider'].title()} {stage6_config['name']} Punctuated Transcription"]
        elif stage == 8:
            # Stage 8: Needs both Stage 6 punctuated text and Stage 7 translation
            stage6_config = get_model_init_params(6, 1)
            stage7_config = get_model_init_params(7, 1)
            return [
                f"Stage 6 Model 1 - {stage6_config['provider'].title()} {stage6_config['name']} Punctuated Transcription",
                f"Stage 7 Model 1 - {stage7_config['provider'].title()} {stage7_config['name']} Translation"
            ]
        else:
            return []

    def _verify_stage_data(self, stage: int, model_num: int) -> None:
        """
        Verify required data is present in context window for a stage.
        
        Args:
            stage: Stage number
            model_num: Model number
            
        Raises:
            ValueError: If required data is missing or invalid
        """
        # Get required keys for this stage
        required_keys = self._get_stage_dependencies(stage, model_num)
        if not required_keys:
            return
            
        # Check for missing keys
        missing_keys = [key for key in required_keys if key not in self.context_window]
        if missing_keys:
            print("\nContext Window State:")
            self._debug_context("Verification Error")
            raise ValueError(f"Stage {stage} incomplete. Missing data: {missing_keys}")
        
        # Verify content is not empty
        empty_keys = [key for key in required_keys if isinstance(self.context_window.get(key), str) 
                     and not self.context_window[key].strip()]
        if empty_keys:
            raise ValueError(f"Stage {stage} incomplete. Empty content for: {empty_keys}")
        
        print(f"\nStage {stage} verification passed - All required data present and non-empty")

    def _debug_context(self, stage: str):
        """Debug helper to verify context window state"""
        print(f"\nContext Window State after {stage}:")
        for key, value in self.context_window.items():
            if key == "image":
                print(f"- {key}: <base64 encoded image>")
                continue
            # Print first 100 chars of value if it's a string
            preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            print(f"- {key}: {preview}")

    def process_image(self, image_base64: str, token_tracker: Optional['TokenTracker'] = None) -> Dict[str, Any]:
        """
        Process an image through all stages using the shared context window.
        
        Args:
            image_base64: Base64 encoded image string
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            Dict[str, Any]: Context window containing all stage results
            
        Raises:
            ValueError: If stage validation fails or required data is missing
            RuntimeError: If model creation or execution fails
            Exception: For any other processing errors
        """
        try:
            # Use provided token tracker or lazy load default one
            if token_tracker is not None:
                self.token_tracker = token_tracker
            
            # Validate image data
            if not image_base64:
                raise ValueError("Image data cannot be empty")
            if not isinstance(image_base64, str):
                raise ValueError("Image data must be a base64 string")
            
            # Initialize run metadata
            self._initialize_run(image_base64)
            
            # Store image in context window for transcription stages only
            self.context_window["image"] = image_base64

            print("\n=== Starting Image Processing Pipeline ===")
            
            # Stage 1: Initial Transcription (3 models in parallel)
            print("\n=== Stage 1: Initial Transcription ===")
            self._execute_transcription_stage(1, image_base64)
            self._debug_context("Stage 1")
            
            # Stage 2: Secondary Transcription (3 models in parallel)
            print("\n=== Stage 2: Secondary Transcription ===")
            self._execute_transcription_stage(2, image_base64)
            self._debug_context("Stage 2")
            
            # Stage 3: Initial Review (3 models in parallel)
            print("\n=== Stage 3: Initial Review ===")
            self._execute_review_stage(3)
            self._debug_context("Stage 3")
            
            # Stage 4: Comprehensive Review (3 models in parallel)
            print("\n=== Stage 4: Comprehensive Review ===")
            self._execute_review_stage(4)
            self._debug_context("Stage 4")
            
            # Final Stages (5-8)
            print("\n=== Starting Final Stages ===")
            self._execute_final_stages()
            self._debug_context("Final Stages")
            
            print("\n=== Image Processing Complete ===")
            return self.context_window
            
        except Exception as e:
            print("\nError occurred during image processing.")
            print("\nContext Window State at Error:")
            self._debug_context("Error State")
            print("\nFull error details:")
            raise
        finally:
            # Cleanup
            if "image" in self.context_window:
                del self.context_window["image"]
            self._active_models.clear()

    def _execute_transcription_stage(self, stage: int, image_base64: str):
        """
        Execute a transcription stage with multiple models in parallel.
        
        Args:
            stage: Stage number (must be 1 or 2)
            image_base64: Base64 encoded image string
            
        Raises:
            ValueError: If stage is not 1 or 2
            RuntimeError: If model creation or execution fails
        """
        if stage not in [1, 2]:
            raise ValueError(f"Invalid transcription stage: {stage}")
            
        stage_content = ""
        stage_next = {}
        success_count = 0
        errors = []
        
        for model_num in range(1, 4):  # 3 models per stage
            model_info = None  # Initialize outside try block
            try:
                model = ModelFactory.create_model(stage, model_num)
                self._active_models.append(model)
                model_info = self._get_model_info(stage, model_num)
                print(f"\nProcessing Stage {stage} Transcription with {model_info}...")
                
                transcription = model.generate_transcription(image_base64, self.token_tracker)
                if not transcription:
                    raise ValueError("Empty transcription result")
                    
                key = f"{model_info} Transcription"
                self.context_window[key] = transcription
                stage_content += f"## {model_info}\n" + transcription + "\n\n"
                stage_next[key] = transcription
                print("- Transcription completed and stored")
                success_count += 1
                
            except Exception as e:
                error_msg = f"Error with {model_info or f'Stage {stage} Model {model_num}'}: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
                # Save output before raising error
                if stage_content:
                    self._save_stage_output(stage, stage_content, stage_next)
                raise RuntimeError(f"Failed to complete Stage {stage} Model {model_num}: {str(e)}") from e
        
        # Save stage output
        self._save_stage_output(stage, stage_content, stage_next)
        
        if success_count == 0:
            raise RuntimeError(
                f"All models failed in transcription stage {stage}. Errors:\n" +
                "\n".join(errors)
            )

    def _execute_review_stage(self, stage: int):
        """
        Execute a review stage with multiple models in parallel.
        
        Args:
            stage: Stage number (must be 3 or 4)
            
        Raises:
            ValueError: If stage is not 3 or 4 or if required data is missing
            RuntimeError: If model creation or execution fails
        """
        if stage not in [3, 4]:
            raise ValueError(f"Invalid review stage: {stage}")
            
        stage_content = ""
        stage_next = {}
        success_count = 0
        errors = []
        
        for model_num in range(1, 4):  # 3 models per stage
            model_info = None  # Initialize outside try block
            try:
                # Verify required data is present
                self._verify_stage_data(stage, model_num)
                
                model = ModelFactory.create_model(stage, model_num)
                self._active_models.append(model)
                model_info = self._get_model_info(stage, model_num)
                print(f"\nProcessing Stage {stage} Review with {model_info}...")
                
                if stage == 3:
                    review = model.analyze_context(self.context_window, self.token_tracker)
                    print("- Analysis completed")
                else:  # stage 4
                    review = model.comprehensive_review(self.context_window, self.token_tracker)
                    print("- Comprehensive review completed")
                
                if not review:
                    raise ValueError("Empty review result")
                    
                key = f"{model_info} Review"
                self.context_window[key] = review
                stage_content += f"## {model_info}\n" + review + "\n\n"
                stage_next[key] = review
                print("- Results stored in context window")
                success_count += 1
                
            except Exception as e:
                error_msg = f"Error with {model_info or f'Stage {stage} Model {model_num}'}: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
                # Save output before raising error
                if stage_content:
                    self._save_stage_output(stage, stage_content, stage_next)
                raise RuntimeError(f"Failed to complete Stage {stage} Model {model_num}: {str(e)}") from e
        
        # Save stage output
        self._save_stage_output(stage, stage_content, stage_next)
        
        if success_count == 0:
            raise RuntimeError(
                f"All models failed in review stage {stage}. Errors:\n" +
                "\n".join(errors)
            )

    def _execute_final_stages(self):
        """
        Execute final stages (5-8) with the selected model.
        
        Raises:
            ValueError: If required data is missing for any stage
            RuntimeError: If model creation or execution fails
        """
        # Remove image from context window since it's not needed for final stages
        if "image" in self.context_window:
            del self.context_window["image"]
        
        try:
            # Stage 5: Final Transcription
            print("\n=== Stage 5: Generating Final Authoritative Transcription ===")
            self._verify_stage_data(5, 1)
            model = ModelFactory.create_model(5, 1)  # Use first model for final stages
            self._active_models.append(model)
            model_info = self._get_model_info(5, 1)
            print(f"Processing with {model_info}...")
            final_transcription = model.generate_final_transcription(self.context_window, self.token_tracker)
            if not final_transcription:
                raise ValueError("Empty final transcription result")
            key = f"{model_info} Final Transcription"
            self.context_window[key] = final_transcription
            stage5_content = "## Final Authoritative Transcription\n```\n" + final_transcription + "\n```\n\n"
            stage5_next = {key: final_transcription}
            self._save_stage_output(5, stage5_content, stage5_next)
            print("- Final transcription completed and stored")
            
            # Stage 6: Punctuation
            print("\n=== Stage 6: Adding Chinese Punctuation ===")
            self._verify_stage_data(6, 1)
            model = ModelFactory.create_model(6, 1)
            self._active_models.append(model)
            model_info = self._get_model_info(6, 1)
            print(f"Processing with {model_info}...")
            punctuated = model.add_punctuation(final_transcription, self.token_tracker)
            if not punctuated:
                raise ValueError("Empty punctuation result")
            key = f"{model_info} Punctuated Transcription"
            self.context_window[key] = punctuated
            stage6_content = "## Chinese Text with Punctuation\n" + punctuated + "\n\n"
            stage6_next = {key: punctuated}
            self._save_stage_output(6, stage6_content, stage6_next)
            print("- Punctuation completed and stored")
            
            # Stage 7: Translation
            print("\n=== Stage 7: Translating to English ===")
            self._verify_stage_data(7, 1)
            model = ModelFactory.create_model(7, 1)
            self._active_models.append(model)
            model_info = self._get_model_info(7, 1)
            print(f"Processing with {model_info}...")
            translation = model.translate_to_english(punctuated, self.token_tracker)
            if not translation:
                raise ValueError("Empty translation result")
            key = f"{model_info} Translation"
            self.context_window[key] = translation
            stage7_content = "## English Translation\n" + translation + "\n\n"
            stage7_next = {key: translation}
            self._save_stage_output(7, stage7_content, stage7_next)
            print("- Translation completed and stored")
            
            # Stage 8: Commentary
            print("\n=== Stage 8: Generating Historical Commentary ===")
            self._verify_stage_data(8, 1)
            model = ModelFactory.create_model(8, 1)
            self._active_models.append(model)
            model_info = self._get_model_info(8, 1)
            print(f"Processing with {model_info}...")
            # Get both punctuated Chinese text and English translation for commentary
            stage6_key = next((k for k in self.context_window if "Stage 6" in k and "Punctuated Transcription" in k), None)
            if not stage6_key:
                raise ValueError("Missing Stage 6 punctuated transcription")
            punctuated_text = self.context_window[stage6_key]
            
            commentary = model.generate_commentary(punctuated_text, translation, self.token_tracker)
            if not commentary:
                raise ValueError("Empty commentary result")
            key = f"{model_info} Commentary"
            self.context_window[key] = commentary
            stage8_content = "## Historical Commentary\n" + commentary + "\n\n"
            stage8_content += "\n## Final Stage\nNo data is passed to next stage as this is the final stage."
            self._save_stage_output(8, stage8_content)
            print("- Commentary completed and stored")
            
        except Exception as e:
            print(f"Error in final stages: {str(e)}")
            raise RuntimeError("Failed to complete final stages") from e
