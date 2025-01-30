from typing import Dict, Any, List, TYPE_CHECKING
import sys
import os
import json

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

if TYPE_CHECKING:
    from models.model_interfaces import BaseModel, FinalStageModel
    from utils.token_counter import TokenTracker
    import PIL.Image

class ModelManager:
    def __init__(self):
        # Shared context window to store all data
        self.context_window: Dict[str, Any] = {}
        
        # Token tracker (lazy loaded)
        self._token_tracker = None
        
        # Private model storage
        self._llm1 = None
        self._llm2 = None
        self._llm3 = None
        self._llm4 = None

    @property
    def llm1(self) -> 'BaseModel':
        """Lazy load LLM1"""
        if self._llm1 is None:
            from models import LLM1Model
            self._llm1 = LLM1Model()
        return self._llm1

    @property
    def llm2(self) -> 'BaseModel':
        """Lazy load LLM2"""
        if self._llm2 is None:
            from models import LLM2Model
            self._llm2 = LLM2Model()
        return self._llm2

    @property
    def llm3(self) -> 'BaseModel':
        """Lazy load LLM3"""
        if self._llm3 is None:
            from models import LLM3Model
            self._llm3 = LLM3Model()
        return self._llm3

    @property
    def llm4(self) -> 'FinalStageModel':
        """Lazy load LLM4"""
        if self._llm4 is None:
            from models import LLM4Model
            self._llm4 = LLM4Model()
        return self._llm4

    @property
    def model_sequence(self) -> 'List[tuple]':
        """Get model sequence, creating models only when needed"""
        return [
            (self.llm1, "LLM1"),
            (self.llm2, "LLM2"),
            (self.llm3, "LLM3")
        ]

    def _verify_stage_data(self, stage: str, required_keys: List[str]):
        """Helper method to verify required data is present in context window"""
        missing_keys = [key for key in required_keys if key not in self.context_window]
        if missing_keys:
            print("\nContext Window State:")
            self._debug_context("Verification Error")
            raise Exception(f"{stage} incomplete. Missing data: {missing_keys}")
        
        # Verify content is not empty
        empty_keys = [key for key in required_keys if isinstance(self.context_window.get(key), str) 
                     and not self.context_window[key].strip()]
        if empty_keys:
            raise Exception(f"{stage} incomplete. Empty content for: {empty_keys}")
        
        print(f"\n{stage} verification passed - All required data present and non-empty")

    def _debug_context(self, stage: str):
        """Debug helper to verify context window state"""
        print(f"\nContext Window State after {stage}:")
        for key, value in self.context_window.items():
            # Import PIL.Image only when needed for isinstance check
            if 'PIL' in str(type(value)):
                import PIL.Image
                if isinstance(value, PIL.Image.Image):
                    print(f"- {key}: <PIL.Image.Image object>")
                    continue
            # Print first 100 chars of value if it's a string
            preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            print(f"- {key}: {preview}")

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

    def process_image(self, image: 'PIL.Image.Image', token_tracker: 'TokenTracker' = None) -> 'Dict[str, Any]':
        """
        Process an image through all stages using the shared context window.
        """
        try:
            # Use provided token tracker or lazy load default one
            if token_tracker is not None:
                self.token_tracker = token_tracker
            
            # Store image in context window for transcription stages only
            self.context_window["image"] = image

            print("\n=== Starting Image Processing Pipeline ===")
            
            print("\n=== Stage 1: Initial Image Encoding and Transcription ===")
            self._execute_stage_1(image)
            self._debug_context("Stage 1")
            
            print("\n=== Stage 2: Secondary Image Encoding and Transcription ===")
            self._execute_stage_2()
            self._debug_context("Stage 2")
            
            print("\n=== Stage 3: Comparative Analysis and Recommendation ===")
            self._execute_stage_3()
            self._debug_context("Stage 3")
            
            print("\n=== Stage 4: Comprehensive Review ===")
            self._execute_stage_4()
            self._debug_context("Stage 4")
            
            print("\n=== Starting Final Stages ===")
            self._execute_final_stages()
            self._debug_context("Final Stages")
            
            # Final verification of all stages
            self._verify_all_stages()
            
            print("\n=== Image Processing Complete ===")
            return self.context_window
            
        except Exception as e:
            print("\nError occurred during image processing.")
            print("\nContext Window State at Error:")
            self._debug_context("Error State")
            print("\nFull error details:")
            # Re-raise the original exception to preserve the stack trace
            raise

    def _verify_all_stages(self):
        """Verify all required data from all stages is present"""
        stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Final Stages"]
        for stage in stages:
            required_keys = self._get_required_keys(stage)
            if required_keys:  # Only verify if there are required keys for the stage
                self._verify_stage_data(stage, required_keys)

    def _get_model_config(self, model_key: str):
        """Lazy load model config only when needed"""
        from config.config import get_model_init_params
        return get_model_init_params(int(model_key[-1]))

    def _get_configured_models(self) -> List[tuple]:
        """Get list of configured models."""
        configured_models = []
        for model, model_key in self.model_sequence:
            config = self._get_model_config(model_key)
            if config and config.get('provider') and config.get('name'):
                configured_models.append((model, model_key))
        return configured_models

    def _verify_api_keys(self):
        """Verify required API keys are present for configured models."""
        required_keys = set()
        
        # Check which providers we need based on configured models
        for model_key in ["LLM1", "LLM2", "LLM3", "LLM4"]:
            config = self._get_model_config(model_key)
            if config and config.get('provider') and config.get('name'):  # Check if config exists and model is configured
                provider = config['provider']
                # Get model-specific API key var
                from config.config import get_env_var_name
                api_key_var = get_env_var_name(provider, int(model_key[-1]))
                required_keys.add(api_key_var)
        
        # If no models configured, raise error
        if not required_keys:
            print("\nNo models configured. Please configure at least one model in your .env file.")
            print("\nRequired configuration for each model:")
            print("1. Set the provider: LLM{N}_PROVIDER (e.g., LLM1_PROVIDER=google)")
            print("2. Set the model: LLM{N}_MODEL (e.g., LLM1_MODEL=gemini-2.0-flash-exp)")
            print("3. Set the API key for the chosen provider")
            print("\nExample configurations:")
            print("\nFor LLM1 (Gemini Flash):")
            print("LLM1_PROVIDER=google")
            print("LLM1_MODEL=gemini-2.0-flash-exp")
            print("GEMINI_FLASH_EXP_API_KEY=your-key-here")
            print("\nFor LLM2 (Gemini Pro):")
            print("LLM2_PROVIDER=google")
            print("LLM2_MODEL=gemini-1.5-pro")
            print("GEMINI_PRO_API_KEY=your-key-here")
            print("\nFor LLM3 (Claude):")
            print("LLM3_PROVIDER=anthropic")
            print("LLM3_MODEL=claude-3-5-sonnet-20241022")
            print("CLAUDE35_SONNET_API_KEY=your-key-here")
            print("\nFor LLM4 (Gemini Exp):")
            print("LLM4_PROVIDER=google")
            print("LLM4_MODEL=gemini-exp-1206")
            print("GEMINI_EXP1206_API_KEY=your-key-here")
            raise Exception("No models configured. Please set LLM{N}_PROVIDER and LLM{N}_MODEL in .env")
        
        # Check if keys are present
        missing_keys = []
        for key in required_keys:
            if not os.getenv(key):
                missing_keys.append(key)
        
        if missing_keys:
            print("\nMissing Required API Keys:")
            for key in missing_keys:
                print(f"\n{key}:")
                if 'OPENAI' in key:
                    print("1. Get your API key from: https://platform.openai.com/api-keys")
                elif 'CLAUDE' in key or 'ANTHROPIC' in key:
                    print("1. Get your API key from: https://console.anthropic.com/account/keys")
                elif 'GEMINI' in key:
                    print("1. Get your API key from: https://makersuite.google.com/app/apikey")
                print(f"2. Add to your .env file: {key}=your-api-key-here")
            
            raise Exception("Missing required API keys. Please add them to your .env file.")

    def _execute_stage_1(self, image: 'PIL.Image.Image'):
        """
        Stage 1: Have each model generate transcription
        """
        # Verify API keys before starting
        self._verify_api_keys()
        
        # Have each configured model generate transcription
        configured_models = self._get_configured_models()
        for model, model_key in configured_models:
            config = self._get_model_config(model_key)
            print(f"\nProcessing Stage 1 with model {model_key}...")
            print(f"- Provider: {config['provider']}")
            print(f"- Generating initial transcription...")
            
            # Generate transcription using the shared encoded image
            transcription = model.generate_transcription(image, self.token_tracker)
            
            # Store transcription in context window
            key = f"{model_key}'s Stage 1 transcription"
            self.context_window[key] = transcription
            print(f"- Transcription stored in context window under key: {key}")
        
        # Verify Stage 1 data for configured models
        required_keys = self._get_required_keys("Stage 1")
        self._verify_stage_data("Stage 1", required_keys)

    def _get_required_keys(self, stage: str) -> List[str]:
        """Get required keys based on configured models."""
        configured_models = self._get_configured_models()
        model_nums = [int(model_key[-1]) for _, model_key in configured_models]
        
        if stage == "Stage 1":
            return [f"LLM{i}'s Stage 1 transcription" for i in model_nums]
        elif stage == "Stage 2":
            return [f"LLM{i}'s Stage 2 transcription" for i in model_nums]
        elif stage == "Stage 3":
            return [f"LLM{i}'s Stage 3 Analysis and Recommendation" for i in model_nums]
        elif stage == "Stage 4":
            return [f"LLM{i}'s Stage 4 Comprehensive Review" for i in model_nums]
        elif stage == "Final Stages":
            return [
                "Stage 5 Final Transcription",
                "Stage 6 Punctuated Final Transcription",
                "Stage 7 English Translation",
                "Stage 8 Historical Commentary"
            ]
        return []

    def _execute_stage_2(self):
        """
        Stage 2: Second pass transcriptions
        """
        configured_models = self._get_configured_models()
        for model, model_key in configured_models:
            config = self._get_model_config(model_key)
            print(f"\nProcessing Stage 2 with model {model_key}...")
            print(f"- Provider: {config['provider']}")
            print(f"- Generating secondary transcription...")
            
            # Generate transcription using the shared encoded image
            transcription = model.generate_transcription(
                self.context_window["image"],
                self.token_tracker
            )
            
            # Store transcription in context window
            key = f"{model_key}'s Stage 2 transcription"
            self.context_window[key] = transcription
            print(f"- Transcription stored in context window under key: {key}")
        
        # Verify Stage 2 data for configured models
        required_keys = self._get_required_keys("Stage 2")
        self._verify_stage_data("Stage 2", required_keys)

    def _execute_stage_3(self):
        """
        Stage 3: Each model analyzes all previous data and makes recommendations
        """
        # Get configured models
        configured_models = self._get_configured_models()
        
        # Verify required data from previous stages
        required_keys = []
        for _, model_key in configured_models:
            required_keys.extend([
                f"{model_key}'s Stage 1 transcription",
                f"{model_key}'s Stage 2 transcription"
            ])
        self._verify_stage_data("Previous Stages", required_keys)

        for model, model_key in configured_models:
            config = self._get_model_config(model_key)
            print(f"\nProcessing Stage 3 with model {model_key}...")
            print(f"- Provider: {config['provider']}")
            print(f"- Analyzing previous transcriptions...")
            
            # Create context with only this model's transcriptions
            model_context = {
                f"{model_key}'s Stage 1 transcription": self.context_window[f"{model_key}'s Stage 1 transcription"],
                f"{model_key}'s Stage 2 transcription": self.context_window[f"{model_key}'s Stage 2 transcription"]
            }
            
            # Model analyzes only its own Stage 1 vs Stage 2 transcriptions
            analysis = model.analyze_context(model_context, self.token_tracker)
            
            # Store analysis in context window
            key = f"{model_key}'s Stage 3 Analysis and Recommendation"
            self.context_window[key] = analysis
            print(f"- Analysis stored in context window under key: {key}")
        
        # Verify Stage 3 data for configured models
        required_keys = self._get_required_keys("Stage 3")
        self._verify_stage_data("Stage 3", required_keys)

    def _execute_stage_4(self):
        """
        Stage 4: Each model performs a comprehensive review of all previous data
        """
        # Get configured models
        configured_models = self._get_configured_models()
        
        # Verify required data from previous stages
        required_keys = []
        for _, model_key in configured_models:
            required_keys.extend([
                f"{model_key}'s Stage 1 transcription",
                f"{model_key}'s Stage 2 transcription",
                f"{model_key}'s Stage 3 Analysis and Recommendation"
            ])
        self._verify_stage_data("Previous Stages", required_keys)

        for model, model_key in configured_models:
            config = self._get_model_config(model_key)
            print(f"\nProcessing Stage 4 with model {model_key}...")
            print(f"- Provider: {config['provider']}")
            print(f"- Performing comprehensive review...")
            
            # Model reviews all previous data and generates final recommendations
            review = model.comprehensive_review(self.context_window, self.token_tracker)
            
            # Store review in context window
            key = f"{model_key}'s Stage 4 Comprehensive Review"
            self.context_window[key] = review
            print(f"- Review stored in context window under key: {key}")
        
        # Verify Stage 4 data for configured models
        required_keys = self._get_required_keys("Stage 4")
        self._verify_stage_data("Stage 4", required_keys)

    def _execute_final_stages(self):
        """
        Stages 5-8: Final processing by LLM4
        """
        # Verify required data from previous stages for configured models
        required_keys = self._get_required_keys("Stage 4")
        self._verify_stage_data("Previous Stages", required_keys)
        
        # Remove image from context window since it's not needed for final stages
        if "image" in self.context_window:
            del self.context_window["image"]
        
        # Stage 5: Final Transcription
        print("\n=== Stage 5: Generating Final Authoritative Transcription ===")
        final_transcription = self.llm4.generate_final_transcription(
            self.context_window,
            self.token_tracker
        )
        self.context_window["Stage 5 Final Transcription"] = final_transcription
        print("- Final transcription stored in context window")
        self._verify_stage_data("Stage 5", ["Stage 5 Final Transcription"])
        
        # Stage 6: Punctuation
        print("\n=== Stage 6: Adding Chinese Punctuation ===")
        punctuated = self.llm4.add_punctuation(
            final_transcription,
            self.token_tracker
        )
        self.context_window["Stage 6 Punctuated Final Transcription"] = punctuated
        print("- Punctuated transcription stored in context window")
        self._verify_stage_data("Stage 6", ["Stage 6 Punctuated Final Transcription"])
        
        # Stage 7: Translation
        print("\n=== Stage 7: Translating to English ===")
        translation = self.llm4.translate_to_english(
            punctuated,
            self.token_tracker
        )
        self.context_window["Stage 7 English Translation"] = translation
        print("- Translation stored in context window")
        self._verify_stage_data("Stage 7", ["Stage 7 English Translation"])
        
        # Stage 8: Commentary
        print("\n=== Stage 8: Generating Historical Commentary ===")
        commentary = self.llm4.generate_commentary(
            translation,
            self.token_tracker
        )
        self.context_window["Stage 8 Historical Commentary"] = commentary
        print("- Commentary stored in context window")
        self._verify_stage_data("Stage 8", ["Stage 8 Historical Commentary"])
        
        # Verify all final stages
        required_keys = [
            "Stage 5 Final Transcription",
            "Stage 6 Punctuated Final Transcription",
            "Stage 7 English Translation",
            "Stage 8 Historical Commentary"
        ]
        self._verify_stage_data("Final Stages", required_keys)
