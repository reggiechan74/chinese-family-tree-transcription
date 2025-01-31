"""
Model factory and provider implementations.
"""
import os
import importlib
from typing import Union, Any, Dict, Optional
import sys

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
            # Input tokens handled by API
            return 32768  # Maximum output tokens
        elif provider == 'anthropic':
            return 8192   # Maximum tokens
        elif provider == 'openai':
            return 4096   # Maximum tokens
        return 8192      # Conservative default

    @property
    def api_key(self) -> str:
        """Lazy load API key only when needed"""
        if self._api_key is None:
            self._api_key = os.getenv(self.config['api_key_var'])
            if not self._api_key:
                raise Exception("Authentication error: Please check your environment configuration.")
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
    """Provider implementation."""
    def _initialize_client(self) -> Any:
        try:
            genai = importlib.import_module('google.generativeai')
            genai.configure(api_key=self.api_key)
            if self.config["requires_model_name_param"]:
                return genai.GenerativeModel(model_name=self.config["name"])
            return genai.GenerativeModel(self.config["name"])
        except ImportError:
            raise ImportError(
                "Required package not found. Please check .env.example for setup instructions."
            )

    def generate_content(self, prompt: str, image: Optional[Any] = None, system: Optional[str] = None) -> str:
        # Configure generation parameters
        generation_config = {
            'temperature': self.config['temperature'],
            'top_p': self.config['top_p'],
            'max_output_tokens': self.config['max_tokens'] if self.config['max_tokens'] is not None else self.get_default_max_tokens()
        }
        
        try:
            # Handle Base64 image
            if image:
                try:
                    # Convert to base64 if not already
                    image_base64 = image.get('base64') if isinstance(image, dict) and 'base64' in image else convert_to_base64(image)
                    response = self.client.generate_content(
                        [
                            {"text": prompt},
                            {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                        ],
                        generation_config=generation_config
                    )
                except Exception as img_e:
                    raise Exception(f"Failed to process image: {str(img_e)}")
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
            # Extract error message
            error_msg = str(e)
            if hasattr(e, 'message'):
                error_msg = e.message
            raise Exception(f"API error: {error_msg}")

class AnthropicProvider(ModelProvider):
    """Provider implementation."""
    def _initialize_client(self) -> Any:
        try:
            anthropic = importlib.import_module('anthropic')
            return anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "Required package not found. Please check .env.example for setup instructions."
            )

    def generate_content(self, prompt: str, image: Optional[Any] = None, system: Optional[str] = None) -> str:
        messages_content = []
        
        # Handle Base64 image
        if image:
            try:
                # Convert to base64 if not already
                image_base64 = image.get('base64') if isinstance(image, dict) and 'base64' in image else convert_to_base64(image)
            except Exception as img_e:
                raise Exception(f"Failed to process image: {str(img_e)}")
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
            # Extract error message
            error_msg = str(e)
            if hasattr(e, 'message'):
                error_msg = e.message
            raise Exception(f"API error: {error_msg}")

class OpenAIProvider(ModelProvider):
    """Provider implementation."""
    def _initialize_client(self) -> Any:
        try:
            openai = importlib.import_module('openai')
            return openai.Client(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "Required package not found. Please check .env.example for setup instructions."
            )

    def generate_content(self, prompt: str, image: Optional[Any] = None, system: Optional[str] = None) -> str:
        messages = []
        
        if system:
            messages.append({
                "role": "system",
                "content": system
            })
        
        # Handle image for OpenAI
        if image:
            try:
                # Convert image to base64 for OpenAI
                image_bytes = convert_to_base64(image)
            except Exception as img_e:
                raise Exception(f"Failed to convert image to base64 for OpenAI: {str(img_e)}")
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_bytes}",
                            "detail": "high"
                        }
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
            
            # Add timeout and retry logic
            max_retries = 3
            retry_count = 0
            while retry_count < max_retries:
                try:
                    # OpenAI client handles timeouts internally
                    response = self.client.chat.completions.create(**params)
                    break
                except Exception as retry_e:
                    retry_count += 1
                    if retry_count == max_retries:
                        raise retry_e
                    print(f"Connection error, retrying ({retry_count}/{max_retries})...")
                    import time
                    time.sleep(2 ** retry_count)  # Exponential backoff
            
            return response.choices[0].message.content
        except Exception as e:
            # Handle API key errors securely
            if 'API key' in str(e):
                raise Exception("Authentication error: Please verify your API configuration.")
            # Extract error message
            error_msg = str(e)
            if hasattr(e, 'response') and hasattr(e.response, 'json'):
                error_data = e.response.json()
                if 'error' in error_data:
                    error_msg = error_data['error'].get('message', str(e))
            # Check for SSL/connection errors
            if 'ssl' in error_msg.lower() or 'connection' in error_msg.lower():
                raise Exception(f"Connection error with OpenAI API. Please try again: {error_msg}")
            raise Exception(f"API error: {error_msg}")

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
