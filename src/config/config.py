"""
General configuration settings for the Chinese Family Tree Processing System.
"""
import os
from typing import Dict, Any, Optional

# Provider-specific configurations with generic internal key names
PROVIDER_CONFIGS = {
    'openai': {
        'api_key_var': '_api_key_1',  # Generic key names to avoid exposing actual env var names
        'models': ['gpt-4', 'gpt-4-vision', 'gpt-3.5-turbo']
    },
    'anthropic': {
        'api_key_var': '_api_key_2',
        'models': ['claude-2', 'claude-instant', 'claude-3-5-sonnet-20241022']
    },
    'google': {
        'api_key_var': '_api_key_3',
        'models': ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-pro-vision']
    }
}

# Internal mapping of model numbers to actual environment variable names
# This mapping is only used internally and not exposed in error messages
_ENV_VAR_MAPPING = {
    '_api_key_1': 'OPENAI_API_KEY',
    '_api_key_2': 'CLAUDE35_SONNET_API_KEY',
    '_api_key_3': 'GEMINI_FLASH_EXP_API_KEY',
    'google_1': 'GEMINI_FLASH_EXP_API_KEY',
    'google_2': 'GEMINI_PRO_API_KEY',
    'google_4': 'GEMINI_FLASH_EXP_API_KEY',
    'anthropic_3': 'CLAUDE35_SONNET_API_KEY'
}

# Default configurations if not set in environment
DEFAULT_CONFIGS = {
    1: {'provider': None, 'name': None},
    2: {'provider': None, 'name': None},
    3: {'provider': None, 'name': None},
    4: {'provider': None, 'name': None}
}

def get_provider_config(provider: str) -> Dict[str, Any]:
    """Get provider configuration."""
    if provider not in PROVIDER_CONFIGS:
        raise ValueError("Invalid provider configuration")
    return PROVIDER_CONFIGS[provider]

def get_model_config(model_num: int) -> Dict[str, Optional[str]]:
    """Get model configuration from environment variables."""
    provider_var = f'LLM{model_num}_PROVIDER'
    model_var = f'LLM{model_num}_MODEL'
    
    # Get provider and model from environment
    provider = os.getenv(provider_var)
    model = os.getenv(model_var)
    
    # Validate provider if set
    if provider and provider not in PROVIDER_CONFIGS:
        raise ValueError("Invalid provider configuration")
    
    return {
        'provider': provider,
        'name': model
    }

# Model configurations
MODEL_CONFIGS = {
    1: get_model_config(1) or DEFAULT_CONFIGS[1],
    2: get_model_config(2) or DEFAULT_CONFIGS[2],
    3: get_model_config(3) or DEFAULT_CONFIGS[3],
    4: get_model_config(4) or DEFAULT_CONFIGS[4]
}

def get_model_init_params(model_num: int) -> Optional[Dict[str, Any]]:
    """Get initialization parameters for a specific model number."""
    if model_num not in MODEL_CONFIGS:
        raise ValueError("Invalid model configuration")
    
    config = MODEL_CONFIGS[model_num]
    provider = config['provider']
    name = config['name']
    
    # Return None if model is not configured
    if not provider or not name:
        return None
    
    if provider not in PROVIDER_CONFIGS:
        raise ValueError("Invalid provider configuration")
    
    # Return only the basic config without checking API key
    return {
        'provider': provider,
        'name': name,
        'api_key_var': get_env_var_name(provider, model_num),  # Get model-specific API key var
        'requires_model_name_param': provider == 'google',  # Gemini requires model name param
        'temperature': 0.7,  # Default temperature
        'top_p': 0.95,      # Default top_p
        'max_tokens': None  # Use model's default maximum token limit
    }

def get_env_var_name(provider: str, model_num: int = None) -> str:
    """Get the environment variable name for a provider's API key."""
    if provider not in PROVIDER_CONFIGS:
        raise ValueError("Invalid provider configuration")
    
    # Use internal mapping to get actual environment variable name
    if model_num is not None:
        key = f"{provider}_{model_num}"
        if key in _ENV_VAR_MAPPING:
            return _ENV_VAR_MAPPING[key]
    
    # Default to provider's mapped API key
    provider_key = PROVIDER_CONFIGS[provider]['api_key_var']
    return _ENV_VAR_MAPPING.get(provider_key, '')
