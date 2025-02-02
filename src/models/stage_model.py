"""
Stage-based Model Implementation
"""
import os
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import tiktoken

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from models.model_interfaces import FinalStageModel
from utils.token_counter import TokenTracker
from prompts.stage_prompts import Stage1, Stage2, Stage3, Stage4, Stage5, Stage6, Stage7, Stage8
from config.config import get_model_init_params

class StageModel(FinalStageModel):
    """
    Implementation of stage-based model.
    
    This class implements all stage-specific functionality:
    - Stages 1-2: Transcription (inherited from TranscriptionModel via FinalStageModel)
    - Stages 3-4: Review (inherited from ReviewModel via FinalStageModel)
    - Stages 5-8: Final processing (inherited from FinalStageModel)
    """
    
    # Token counting encoders
    ENCODERS = {
        'google': 'cl100k_base',  # Same as GPT-4
        'openai': 'cl100k_base',
        'groq': 'cl100k_base',
        'anthropic': 'cl100k_base',
        'openrouter': 'cl100k_base',
        'together': 'cl100k_base'  # Using same as others since it's Llama based
    }

    # Models that don't support system messages
    NO_SYSTEM_MESSAGE_MODELS = ['o1-mini', 'o3-mini']
    
    def __init__(self, provider: str, model_name: str, stage: int, model_num: int):
        """Initialize model with provider and model name."""
        super().__init__(provider, model_name, stage, model_num)
        self._client = None
        self._encoder = None
        self._initialize_client()
        self._initialize_encoder()
        
    def _initialize_client(self):
        """Initialize the appropriate API client based on provider."""
        if self.provider == 'google':
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self._client = genai.GenerativeModel(self.model_name)
            
        elif self.provider == 'openai':
            from openai import OpenAI
            self._client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
        elif self.provider == 'groq':
            from groq import Groq
            self._client = Groq(api_key=os.getenv('GROQ_API_KEY'))
            
        elif self.provider == 'anthropic':
            from anthropic import Anthropic
            self._client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            
        elif self.provider == 'openrouter':
            from openai import OpenAI
            self._client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv('OPENROUTER_API_KEY')
            )
            
        elif self.provider == 'together':
            from together import Together
            self._client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
            
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
            
    def _initialize_encoder(self):
        """Initialize the token counting encoder."""
        encoder_name = self.ENCODERS.get(self.provider)
        if not encoder_name:
            raise ValueError(f"No encoder defined for provider: {self.provider}")
        self._encoder = tiktoken.get_encoding(encoder_name)
        
    def _count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        return len(self._encoder.encode(text))
    
    def _extract_transcription_chars(self, text: str) -> int:
        """Extract and count characters from Chinese transcription sections."""
        # For stages 1-2, the entire output is the transcription
        if self.stage <= 2:
            return len(text)
            
        # For stage 3-4, look for sections marked as "Recommended Transcription" or similar
        if self.stage in [3, 4]:
            import re
            transcription = ""
            patterns = [
                r"建议的转录：\s*([^#\n]+)",  # Chinese
                r"Recommended Transcription:\s*([^#\n]+)",  # English
                r"转录：\s*([^#\n]+)",  # Shorter Chinese
                r"Transcription:\s*([^#\n]+)"  # Shorter English
            ]
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    transcription = matches[0]
                    break
            return len(transcription.strip())
            
        # For stage 5-6, the entire output is the transcription
        if self.stage in [5, 6]:
            return len(text)
            
        # For stages 7-8, don't count characters as they don't produce Chinese transcriptions
        return 0
            
    def _generate_content(self, prompt: str, image: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate content using the appropriate provider's API.
        
        Args:
            prompt: The prompt text
            image: Optional base64 encoded image
            
        Returns:
            Dict containing response content and usage info
        """
        try:
            if self.provider == 'google':
                if image:
                    response = self._client.generate_content([prompt, {"mime_type": "image/jpeg", "data": image}])
                else:
                    response = self._client.generate_content(prompt)
                content = response.text
                return {
                    'content': content,
                    'usage': {
                        'input_tokens': self._count_tokens(prompt) + (1000 if image else 0),  # Estimate image tokens
                        'output_tokens': self._count_tokens(content)
                    }
                }
                
            elif self.provider == 'openai':
                messages = []
                # Only add system message for models that support it
                if self.model_name not in self.NO_SYSTEM_MESSAGE_MODELS:
                    messages.append({"role": "system", "content": "You are a helpful assistant."})
                
                if image:
                    messages.append({
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}
                        ]
                    })
                else:
                    messages.append({"role": "user", "content": prompt})
                
                response = self._client.chat.completions.create(
                    model=self.model_name,
                    messages=messages
                )
                return {
                    'content': response.choices[0].message.content,
                    'usage': {
                        'input_tokens': response.usage.prompt_tokens,
                        'output_tokens': response.usage.completion_tokens
                    }
                }
                
            elif self.provider == 'groq':
                if image:
                    # For vision tasks, use vision-specific format
                    response = self._client.chat.completions.create(
                        model=self.model_name,  # Use configured model name
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{image}",
                                        },
                                    },
                                ],
                            }
                        ]
                    )
                else:
                    # For non-vision tasks, use standard format
                    response = self._client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                content = response.choices[0].message.content
                return {
                    'content': content,
                    'usage': {
                        'input_tokens': self._count_tokens(prompt) + (1000 if image else 0),  # Estimate image tokens
                        'output_tokens': self._count_tokens(content)
                    }
                }
                
            elif self.provider == 'anthropic':
                if image:
                    max_tokens = 4096 if 'claude-3-opus' in self.model_name else 8192
                    response = self._client.messages.create(
                        model=self.model_name,
                        max_tokens=max_tokens,
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image}}
                            ]
                        }]
                    )
                else:
                    max_tokens = 4096 if 'claude-3-opus' in self.model_name else 8192
                    response = self._client.messages.create(
                        model=self.model_name,
                        max_tokens=max_tokens,
                        messages=[{
                            "role": "user",
                            "content": prompt
                        }]
                    )
                content = response.content[0].text
                return {
                    'content': content,
                    'usage': {
                        'input_tokens': self._count_tokens(prompt),
                        'output_tokens': self._count_tokens(content)
                    }
                }
                
            elif self.provider == 'openrouter':
                if image:
                    response = self._client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}
                            ]}
                        ],
                        extra_headers={
                            "HTTP-Referer": "https://github.com/reggiechan74/chinese-family-tree-transcription",
                            "X-Title": "Chinese Family Tree Transcription"
                        }
                    )
                else:
                    response = self._client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        extra_headers={
                            "HTTP-Referer": "https://github.com/reggiechan74/chinese-family-tree-transcription",
                            "X-Title": "Chinese Family Tree Transcription"
                        }
                    )
                return {
                    'content': response.choices[0].message.content,
                    'usage': {
                        'input_tokens': response.usage.prompt_tokens,
                        'output_tokens': response.usage.completion_tokens
                    }
                }
                
            elif self.provider == 'together':
                response = self._client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                content = response.choices[0].message.content
                return {
                    'content': content,
                    'usage': {
                        'input_tokens': self._count_tokens(prompt),
                        'output_tokens': self._count_tokens(content)
                    }
                }
                
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
                
        except Exception as e:
            error_msg = str(e)
            if self.provider == 'google' and '500' in error_msg:
                error_msg = (
                    f"Error with {self.provider} {self.model_name}: Context window length exceeded. "
                    f"This model cannot handle the amount of text being processed. "
                    f"Consider using a model with a larger context window like gemini-2.0-flash-exp or gemini-1.5-pro. "
                    f"Original error: {error_msg}"
                )
            else:
                error_msg = f"Error generating content with {self.provider} {self.model_name}: {error_msg}"
            print(error_msg)
            raise RuntimeError(error_msg)
    
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
        # Call parent validation
        super().generate_transcription(image_base64, token_tracker)
        
        # Get appropriate prompt based on stage
        if self.stage == 1:
            prompt = Stage1.get_prompt()
        elif self.stage == 2:
            prompt = Stage2.get_prompt()
        else:
            raise ValueError(f"Invalid stage {self.stage} for transcription")
        
        # Call provider's API with the prompt and image
        result = self._generate_content(prompt, image_base64)
        
        # Track token usage if tracker provided
        if token_tracker:
            content = result['content'].strip()
            token_tracker.add_usage(
                stage=f"Stage {self.stage}",
                model=f"Stage {self.stage} Model {self.model_num} - {self.provider.title()} {self.model_name}",
                model_name=self.model_name,
                input_tokens=result['usage']['input_tokens'],
                output_tokens=result['usage']['output_tokens'],
                char_count=self._extract_transcription_chars(content)
            )
        
        return result['content'].strip()

    def analyze_context(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """
        Compare and analyze Stage 1 and Stage 2 transcriptions for this model number.
        
        Each Stage 3 model analyzes the transcriptions from Stage 1 and Stage 2
        that were produced by the model with the same model number. For example,
        Stage 3 Model 1 analyzes Stage 1 Model 1 and Stage 2 Model 1 transcriptions,
        even though the Stage 3 model may be a different provider/model.
        
        Args:
            context: Context window containing Stage 1 and 2 transcriptions
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            str: Analysis, recommendations, and suggested transcription
            
        Raises:
            ValueError: If stage is not stage 3
        """
        # Call parent validation
        super().analyze_context(context, token_tracker)
        
        # Get transcriptions from Stage 1 and 2 for this model number
        transcriptions = {}
        for stage in [1, 2]:
            stage_config = get_model_init_params(stage, self.model_num)
            key = f"Stage {stage} Model {self.model_num} - {stage_config['provider'].title()} {stage_config['name']} Transcription"
            if key in context:
                transcriptions[key] = context[key]
        
        # Get prompt from Stage3
        prompt = Stage3.get_prompt(transcriptions)
        
        # Call provider's API
        result = self._generate_content(prompt)
        
        # Track token usage if tracker provided
        if token_tracker:
            token_tracker.add_usage(
                stage=f"Stage {self.stage}",
                model=f"Stage {self.stage} Model {self.model_num} - {self.provider.title()} {self.model_name}",
                model_name=self.model_name,
                input_tokens=result['usage']['input_tokens'],
                output_tokens=result['usage']['output_tokens'],
                char_count=self._extract_transcription_chars(result['content'].strip())
            )
        
        return result['content'].strip()
        
    def comprehensive_review(self, context: Dict[str, Any], token_tracker: TokenTracker = None) -> str:
        """
        Review all Stage 3 analyses and recommend a transcript.
        
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
        # Call parent validation
        super().comprehensive_review(context, token_tracker)
        
        # Get all Stage 3 reviews using actual Stage 3 model configs
        stage3_reviews = {}
        for model_num in range(1, 4):
            stage3_config = get_model_init_params(3, model_num)
            key = f"Stage 3 Model {model_num} - {stage3_config['provider'].title()} {stage3_config['name']} Review"
            if key in context:
                stage3_reviews[key] = context[key]
        
        # Get prompt from Stage4
        prompt = Stage4.get_prompt(stage3_reviews)
        
        # Call provider's API
        result = self._generate_content(prompt)
        
        # Track token usage if tracker provided
        if token_tracker:
            token_tracker.add_usage(
                stage=f"Stage {self.stage}",
                model=f"Stage {self.stage} Model {self.model_num} - {self.provider.title()} {self.model_name}",
                model_name=self.model_name,
                input_tokens=result['usage']['input_tokens'],
                output_tokens=result['usage']['output_tokens'],
                char_count=self._extract_transcription_chars(result['content'].strip())
            )
        
        return result['content'].strip()
        
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
        # Call parent validation
        super().generate_final_transcription(context, token_tracker)
        
        # Get stage 4 reviews using actual Stage 4 model configs
        stage4_reviews = {}
        for model_num in range(1, 4):
            stage4_config = get_model_init_params(4, model_num)
            key = f"Stage 4 Model {model_num} - {stage4_config['provider'].title()} {stage4_config['name']} Review"
            if key in context:
                stage4_reviews[key] = context[key]
        
        # Get prompt from Stage5
        prompt = Stage5.get_prompt(stage4_reviews)
        
        # Call provider's API
        result = self._generate_content(prompt)
        
        # Track token usage if tracker provided
        if token_tracker:
            token_tracker.add_usage(
                stage=f"Stage {self.stage}",
                model=f"Stage {self.stage} Model {self.model_num} - {self.provider.title()} {self.model_name}",
                model_name=self.model_name,
                input_tokens=result['usage']['input_tokens'],
                output_tokens=result['usage']['output_tokens'],
                char_count=self._extract_transcription_chars(result['content'].strip())
            )
        
        return result['content'].strip()
        
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
        # Call parent validation
        super().add_punctuation(text, token_tracker)
        
        # Get prompt from Stage6
        prompt = Stage6.get_prompt(text)
        
        # Call provider's API
        result = self._generate_content(prompt)
        
        # Track token usage if tracker provided
        if token_tracker:
            token_tracker.add_usage(
                stage=f"Stage {self.stage}",
                model=f"Stage {self.stage} Model {self.model_num} - {self.provider.title()} {self.model_name}",
                model_name=self.model_name,
                input_tokens=result['usage']['input_tokens'],
                output_tokens=result['usage']['output_tokens'],
                char_count=self._extract_transcription_chars(result['content'].strip())
            )
        
        return result['content'].strip()
        
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
        # Call parent validation
        super().translate_to_english(text, token_tracker)
        
        # Get prompt from Stage7
        prompt = Stage7.get_prompt(text)
        
        # Call provider's API
        result = self._generate_content(prompt)
        
        # Track token usage if tracker provided
        if token_tracker:
            token_tracker.add_usage(
                stage=f"Stage {self.stage}",
                model=f"Stage {self.stage} Model {self.model_num} - {self.provider.title()} {self.model_name}",
                model_name=self.model_name,
                input_tokens=result['usage']['input_tokens'],
                output_tokens=result['usage']['output_tokens'],
                char_count=self._extract_transcription_chars(result['content'].strip())
            )
        
        return result['content'].strip()
        
    def generate_commentary(self, chinese_text: str, english_text: str, token_tracker: TokenTracker = None) -> str:
        """
        Generate historical commentary on the text.
        
        Args:
            chinese_text: Punctuated Chinese text
            english_text: English translation
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            str: Historical commentary
            
        Raises:
            ValueError: If stage is not stage 8
        """
        # Call parent validation
        super().generate_commentary(chinese_text, english_text, token_tracker)
        
        # Get prompt from Stage8
        prompt = Stage8.get_prompt(chinese_text, english_text)
        
        # Call provider's API
        result = self._generate_content(prompt)
        
        # Track token usage if tracker provided
        if token_tracker:
            token_tracker.add_usage(
                stage=f"Stage {self.stage}",
                model=f"Stage {self.stage} Model {self.model_num} - {self.provider.title()} {self.model_name}",
                model_name=self.model_name,
                input_tokens=result['usage']['input_tokens'],
                output_tokens=result['usage']['output_tokens'],
                char_count=len(result['content'].strip())
            )
        
        return result['content'].strip()
