"""
General configuration settings for the Chinese Family Tree Processing System.
"""
import os
from typing import Dict, Any, Optional

# Provider-specific configurations
PROVIDER_CONFIGS = {
    'openai': {
        'api_key_var': 'OPENAI_API_KEY',
        'models': ['gpt-4', 'gpt-4-vision', 'gpt-3.5-turbo']
    },
    'anthropic': {
        'api_key_var': 'CLAUDE35_SONNET_API_KEY',
        'models': ['claude-2', 'claude-instant', 'claude-3-5-sonnet-20241022']
    },
    'google': {
        'api_key_var': 'GEMINI_FLASH_EXP_API_KEY',
        'models': ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-pro-vision']
    }
}

# Model-specific API key mappings
MODEL_API_KEYS = {
    ('google', 1): 'GEMINI_FLASH_EXP_API_KEY',
    ('google', 2): 'GEMINI_PRO_API_KEY',
    ('google', 4): 'GEMINI_FLASH_EXP_API_KEY',
    ('anthropic', 3): 'CLAUDE35_SONNET_API_KEY'
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
        raise ValueError(f"Invalid provider: {provider}. Must be one of: {', '.join(PROVIDER_CONFIGS.keys())}")
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
        raise ValueError(f"Invalid provider in {provider_var}: {provider}. Must be one of: {', '.join(PROVIDER_CONFIGS.keys())}")
    
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
        raise ValueError(f"Invalid model number: {model_num}")
    
    config = MODEL_CONFIGS[model_num]
    provider = config['provider']
    name = config['name']
    
    # Return None if model is not configured
    if not provider or not name:
        return None
    
    if provider not in PROVIDER_CONFIGS:
        raise ValueError(f"Invalid provider: {provider}")
    
    # Return only the basic config without checking API key
    return {
        'provider': provider,
        'name': name,
        'api_key_var': get_env_var_name(provider, model_num),  # Get model-specific API key var
        'requires_model_name_param': provider == 'google',  # Gemini requires model name param
        'temperature': 0.7,  # Default temperature
        'top_p': 0.95,      # Default top_p
        'max_tokens': 8192  # Max tokens for Gemini models
    }

def get_env_var_name(provider: str, model_num: int = None) -> str:
    """Get the environment variable name for a provider's API key."""
    if provider not in PROVIDER_CONFIGS:
        raise ValueError(f"Invalid provider: {provider}")
    
    # Check for model-specific API key
    if model_num is not None and (provider, model_num) in MODEL_API_KEYS:
        return MODEL_API_KEYS[(provider, model_num)]
    
    # Default to provider's default API key
    return PROVIDER_CONFIGS[provider]['api_key_var']
