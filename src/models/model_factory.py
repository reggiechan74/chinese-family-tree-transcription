
import os
import importlib
from typing import Union, Any, Dict, Optional
import google.generativeai as genai
import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from utils.image_utils import convert_to_base64  # Updated import path
from config.config import get_model_init_params, get_env_var_name  # Updated import path

class ModelProvider:
    """Base class for model providers."""
    def __init__(self, api_key: Optional[str], config: Dict[str, Any]):
        self._api_key = api_key
        self.config = config
        self._client = None
        
    def get_default_max_tokens(self) -> int:
        """Get the default maximum tokens for this provider."""
        provider = self.config['provider']
        if provider == 'google':
            # For Gemini, this is used for output tokens
            # Input tokens can go up to 2,000,000 but that's handled separately
            return 32768  # Gemini's max output tokens
        elif provider == 'anthropic':
            return 8192    # Claude-3.5-sonnet's max tokens
        elif provider == 'openai':
            return 4096     # GPT-4's max tokens
        return 8192        # Conservative default

    @property
    def api_key(self) -> str:
        """Lazy load API key only when needed"""
        if self._api_key is None:
            self._api_key = os.getenv(self.config['api_key_var'])
            if not self._api_key:
                provider_name = {
                    'openai': 'OpenAI',
                    'anthropic': 'Anthropic',
                    'google': 'Google'
                }.get(self.config['provider'], self.config['provider'].title())
                raise Exception(f"{provider_name} API error: Missing API key. Please check your environment configuration.")
        return self._api_key

    @property
    def client(self) -> Any:
        """Lazy initialize client only when needed"""
        if self._client is None:
            self._client = self._initialize_client()
        return self._client

    def _initialize_client(self) -> Any:
        raise NotImplementedError

    def generate_content(self, prompt: str, image: Optional[Any] = None, system: Optional[str] = None) -> str:
        raise NotImplementedError

class GeminiProvider(ModelProvider):
    """Provider for Google's Gemini models."""
    def _initialize_client(self) -> Any:
        genai.configure(api_key=self.api_key)
        if self.config["requires_model_name_param"]:
            return genai.GenerativeModel(model_name=self.config["name"])
        return genai.GenerativeModel(self.config["name"])

    def generate_content(self, prompt: str, image: Optional[Any] = None, system: Optional[str] = None) -> str:
        # Gemini has a 2M input token limit handled by the API internally
        # We only need to set the output token limit in generation_config
        generation_config = {
            'temperature': self.config['temperature'],
            'top_p': self.config['top_p'],
            'max_output_tokens': self.config['max_tokens'] if self.config['max_tokens'] is not None else self.get_default_max_tokens()
        }
        
        try:
            # Only handle image if it's a PIL Image or dict with 'pil' key
            if image and (isinstance(image, dict) and 'pil' in image or 'PIL' in str(type(image))):
                pil_image = image.get('pil') if isinstance(image, dict) else image
                response = self.client.generate_content(
                    [prompt, pil_image],
                    generation_config=generation_config
                )
            else:
                response = self.client.generate_content(
                    prompt,
                    generation_config=generation_config
                )
            
            return response.text
        except Exception as e:
            # Handle API key errors securely
            if 'API key' in str(e):
                raise Exception("Authentication error: Please verify your API configuration.")
            # Extract error message from Gemini's error response
            error_msg = str(e)
            if hasattr(e, 'message'):
                error_msg = e.message
            raise Exception(f"Gemini API error: {error_msg}")

class AnthropicProvider(ModelProvider):
    """Provider for Anthropic's Claude models."""
    def _initialize_client(self) -> Any:
        try:
            anthropic = importlib.import_module('anthropic')
            return anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "Anthropic package not found. Install it with:\n"
                "pip install anthropic httpx"
            )

    def generate_content(self, prompt: str, image: Optional[Any] = None, system: Optional[str] = None) -> str:
        messages_content = []
        
        # Only handle image if it's a PIL Image or dict with 'base64' key
        if image and (isinstance(image, dict) and 'base64' in image or 'PIL' in str(type(image))):
            image_base64 = image.get('base64') if isinstance(image, dict) else convert_to_base64(image)
            messages_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_base64
                }
            })
        
        messages_content.append({
            "type": "text",
            "text": prompt
        })

        message_params = {
            "model": self.config["name"],
            "temperature": self.config["temperature"],
            "max_tokens": self.config['max_tokens'] if self.config['max_tokens'] is not None else self.get_default_max_tokens(),
            "messages": [{
                "role": "user",
                "content": messages_content
            }]
        }

        if system:
            message_params["system"] = system

        try:
            response = self.client.messages.create(**message_params)
            return response.content[0].text
        except Exception as e:
            # Handle API key errors securely
            if 'API key' in str(e):
                raise Exception("Authentication error: Please verify your API configuration.")
            # Extract error message from Anthropic's error response
            error_msg = str(e)
            if hasattr(e, 'message'):
                error_msg = e.message
            raise Exception(f"Anthropic API error: {error_msg}")

class OpenAIProvider(ModelProvider):
    """Provider for OpenAI's GPT models."""
    def _initialize_client(self) -> Any:
        try:
            openai = importlib.import_module('openai')
            return openai.Client(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "OpenAI package not found. Install it with:\n"
                "pip install openai"
            )

    def generate_content(self, prompt: str, image: Optional[Any] = None, system: Optional[str] = None) -> str:
        messages = []
        
        if system:
            messages.append({
                "role": "system",
                "content": system
            })
        
        # Only handle image if it's a PIL Image or dict with 'base64' key
        if image and (isinstance(image, dict) and 'base64' in image or 'PIL' in str(type(image))):
            image_bytes = image.get('base64') if isinstance(image, dict) else convert_to_base64(image)
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_bytes}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            })
        else:
            messages.append({
                "role": "user",
                "content": prompt
            })

        try:
            params = {
                "model": self.config["name"],
                "messages": messages,
                "temperature": self.config["temperature"]
            }
            # Only add max_tokens if explicitly set
            if self.config['max_tokens'] is not None:
                params["max_tokens"] = self.config["max_tokens"]
            
            response = self.client.chat.completions.create(**params)
            
            return response.choices[0].message.content
        except Exception as e:
            # Handle API key errors securely
            if 'API key' in str(e):
                raise Exception("Authentication error: Please verify your API configuration.")
            # Extract error message from OpenAI's error response
            error_msg = str(e)
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                error_data = e.response.json()
                if 'error' in error_data:
                    error_msg = error_data['error'].get('message', str(e))
            raise Exception(f"OpenAI API error: {error_msg}")

class ModelFactory:
    """Factory class to create model instances based on provider configuration."""
    
    PROVIDERS = {
        "google": GeminiProvider,
        "anthropic": AnthropicProvider,
        "openai": OpenAIProvider
    }
    
    @staticmethod
    def create_model(llm_number: int) -> ModelProvider:
        """
        Create and configure a model instance based on the provider and configuration.
        
        Args:
            llm_number: The LLM number (1-4)
            
        Returns:
            A configured ModelProvider instance
        
        Raises:
            ImportError: If the required package for the selected model is not installed
            ValueError: If the API key is missing or provider is unknown
        """
        config = get_model_init_params(llm_number)
        provider = config["provider"]
        provider_class = ModelFactory.PROVIDERS.get(provider)
        
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider}")
            
        # Pass provider name and model number to allow lazy loading of API key
        config['api_key_var'] = get_env_var_name(provider, llm_number)
        return provider_class(None, config)
