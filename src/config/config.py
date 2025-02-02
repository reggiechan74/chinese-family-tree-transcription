"""
General configuration settings for the Chinese Family Tree Processing System.
"""
import os
from typing import Dict, Any, Optional

# Provider-specific configurations with generic internal key names
PROVIDER_CONFIGS = {
    'openai': {
        'api_key_var': '_api_key_1',
        'models': [
            'gpt-4-turbo',           # Vision + Language
            'gpt-4-vision-preview',   # Vision + Language
            'chatgpt-4o-latest',     # Vision + Language
            'o1-mini',               # Vision + Language
            'o3-mini'                # Vision + Language
        ]
    },
    'anthropic': {
        'api_key_var': '_api_key_2',
        'models': [
            'claude-3-5-sonnet-20241022',  # Vision + Language
            'claude-3-opus-20240229'       # Vision + Language
        ]
    },
    'google': {
        'api_key_var': '_api_key_3',
        'models': [
            'gemini-2.0-flash-exp',   # Vision + Language
            'gemini-1.5-pro',         # Vision + Language
            'gemini-exp-1206',        # Vision + Language
            'gemini-pro',             # Language only
            'gemini-pro-vision'       # Vision + Language
        ]
    },
    'groq': {
        'api_key_var': '_api_key_4',
        'models': [
            'llama-3.2-90b-vision-preview',     # Vision + Language
            'deepseek-r1-distill-llama-70b',    # Language only
            'mixtral-8x7b-32768',               # Language only
            'llama2-70b-4096',                  # Language only
            'llama-3.3-70b-versatile'           # Language only
        ]
    },
    'openrouter': {
        'api_key_var': '_api_key_5',
        'models': [
            'meta-llama/llama-3.2-90b-vision-instruct',  # Vision + Language
            'deepseek/deepseek-r1:free',                 # Language only
            'x-ai/grok-2-vision-1212',                   # Vision + Language
            'qwen/qvq-72b-preview'                       # Vision + Language
        ]
    }
}

# Map provider to their API key environment variable names
_PROVIDER_API_KEYS = {
    'openai': 'OPENAI_API_KEY',
    'anthropic': 'ANTHROPIC_API_KEY',
    'google': 'GOOGLE_API_KEY',
    'groq': 'GROQ_API_KEY',
    'openrouter': 'OPENROUTER_API_KEY'
}

def validate_api_key(provider: str) -> None:
    """
    Validate that the API key exists for a provider.
    
    Args:
        provider: Provider name
        
    Raises:
        RuntimeError: If API key is missing
    """
    key_var = _PROVIDER_API_KEYS.get(provider)
    if not key_var:
        raise ValueError(f"Unknown provider: {provider}")
        
    api_key = os.getenv(key_var)
    if not api_key:
        raise RuntimeError(
            f"Missing API key for {provider}. "
            f"Please set {key_var} environment variable."
        )

def validate_model_params(temperature: float, top_p: float, max_tokens: Optional[int]) -> None:
    """
    Validate model parameters are within acceptable ranges.
    
    Args:
        temperature: Temperature parameter (0.0-1.0)
        top_p: Top-p parameter (0.0-1.0)
        max_tokens: Maximum tokens (None or positive integer)
        
    Raises:
        ValueError: If parameters are invalid
    """
    if not 0.0 <= temperature <= 1.0:
        raise ValueError(f"Temperature must be between 0.0 and 1.0, got {temperature}")
        
    if not 0.0 <= top_p <= 1.0:
        raise ValueError(f"Top-p must be between 0.0 and 1.0, got {top_p}")
        
    if max_tokens is not None and max_tokens <= 0:
        raise ValueError(f"Max tokens must be positive, got {max_tokens}")

def validate_model_capability(provider: str, model: str, stage: int) -> None:
    """
    Validate that a model has the required capabilities for a stage.
    
    Args:
        provider: Provider name
        model: Model name
        stage: Stage number
        
    Raises:
        ValueError: If model lacks required capabilities
    """
    # Vision capability required for stages 1-2
    vision_required = stage <= 2
    
    # Vision-capable models
    vision_models = {
        'openai': ['gpt-4-turbo', 'gpt-4-vision-preview', 'chatgpt-4o-latest', 'o1-mini', 'o3-mini'],
        'anthropic': ['claude-3-5-sonnet-20241022', 'claude-3-opus-20240229'],
        'google': ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-exp-1206', 'gemini-pro-vision'],
        'groq': ['llama-3.2-90b-vision-preview'],
        'openrouter': ['meta-llama/llama-3.2-90b-vision-instruct', 'x-ai/grok-2-vision-1212', 'qwen/qvq-72b-preview']
    }
    
    if vision_required and provider in vision_models:
        if model not in vision_models[provider]:
            raise ValueError(
                f"Model {model} from {provider} does not support vision capabilities "
                f"required for stage {stage}"
            )

def get_stage_type(stage: int) -> str:
    """Get the type of processing for a given stage."""
    if stage <= 2:
        return 'transcription'
    return 'review'

def get_provider_config(provider: str) -> Dict[str, Any]:
    """
    Get provider configuration.
    
    Args:
        provider: Provider name
        
    Returns:
        Dict containing provider configuration
        
    Raises:
        ValueError: If provider is invalid
    """
    if provider not in PROVIDER_CONFIGS:
        raise ValueError(f"Invalid provider: {provider}")
    return PROVIDER_CONFIGS[provider]

def get_stage_model_config(stage: int, model_num: int) -> Dict[str, Any]:
    """
    Get model configuration for a specific stage and model number.
    
    Args:
        stage: Stage number (1-8)
        model_num: Model number (1-3)
        
    Returns:
        Dict containing model configuration
        
    Raises:
        ValueError: If configuration is invalid
        RuntimeError: If required environment variables are missing
    """
    # Validate stage and model number
    if not 1 <= stage <= 8:
        raise ValueError(f"Invalid stage number: {stage}")
    if not 1 <= model_num <= 3:
        raise ValueError(f"Invalid model number: {model_num}")
    
    # Get provider and model from environment variables
    env_provider = os.getenv(f'STAGE{stage}_MODEL{model_num}_PROVIDER')
    env_model = os.getenv(f'STAGE{stage}_MODEL{model_num}_NAME')
    
    # If no specific configuration, use defaults from environment
    if not env_provider or not env_model:
        if stage <= 4:  # Stages 1-4 use all three models by default
            if model_num == 2:
                env_provider = os.getenv('DEFAULT_MODEL2_PROVIDER')
                env_model = os.getenv('DEFAULT_MODEL2_NAME')
            elif model_num == 3:
                env_provider = os.getenv('DEFAULT_MODEL3_PROVIDER')
                env_model = os.getenv('DEFAULT_MODEL3_NAME')
        
        # If still no configuration, use the default model
        if not env_provider or not env_model:
            env_provider = os.getenv('DEFAULT_MODEL_PROVIDER')
            env_model = os.getenv('DEFAULT_MODEL_NAME')
    
    # Validate provider
    if not env_provider or env_provider not in PROVIDER_CONFIGS:
        raise RuntimeError(
            f"Invalid or missing provider configuration for Stage {stage} Model {model_num}. "
            "Please check provider configuration in .env"
        )
    
    # Validate model name is available for provider
    if not env_model or env_model not in PROVIDER_CONFIGS[env_provider]['models']:
        raise RuntimeError(
            f"Invalid or missing model configuration for Stage {stage} Model {model_num}. "
            f"Model {env_model} not available for provider {env_provider}"
        )
    
    # Validate API key exists
    validate_api_key(env_provider)
    
    # Validate model capabilities
    validate_model_capability(env_provider, env_model, stage)
    
    return {
        'provider': env_provider,
        'name': env_model
    }

def get_model_init_params(stage: int, model_num: int) -> Dict[str, Any]:
    """
    Get initialization parameters for a specific stage and model number.
    
    Args:
        stage: Stage number (1-8)
        model_num: Model number (1-3)
        
    Returns:
        Dict containing model initialization parameters
        
    Raises:
        ValueError: If configuration is invalid
        RuntimeError: If required environment variables are missing
    """
    config = get_stage_model_config(stage, model_num)
    provider = config['provider']
    name = config['name']
    
    if provider not in PROVIDER_CONFIGS:
        raise ValueError(f"Invalid provider: {provider}")
    
    # Get and validate parameters
    try:
        temperature = float(os.getenv(f'STAGE{stage}_MODEL{model_num}_TEMPERATURE', '0.7'))
        top_p = float(os.getenv(f'STAGE{stage}_MODEL{model_num}_TOP_P', '0.95'))
        max_tokens_str = os.getenv(f'STAGE{stage}_MODEL{model_num}_MAX_TOKENS', '0')
        max_tokens = int(max_tokens_str) if max_tokens_str != '0' else None
        
        validate_model_params(temperature, top_p, max_tokens)
        
    except ValueError as e:
        raise RuntimeError(
            f"Invalid model parameters for Stage {stage} Model {model_num}: {str(e)}"
        ) from e
    
    return {
        'provider': provider,
        'name': name,
        'api_key_var': get_env_var_name(provider),
        'requires_model_name_param': provider == 'google',
        'temperature': temperature,
        'top_p': top_p,
        'max_tokens': max_tokens
    }

def get_env_var_name(provider: str) -> str:
    """
    Get the environment variable name for a provider's API key.
    
    Args:
        provider: Provider name
        
    Returns:
        Environment variable name
        
    Raises:
        ValueError: If provider is invalid
    """
    if provider not in _PROVIDER_API_KEYS:
        raise ValueError(f"Invalid provider: {provider}")
    
    return _PROVIDER_API_KEYS[provider]
