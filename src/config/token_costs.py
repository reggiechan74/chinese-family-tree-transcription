"""
Centralized configuration for token costs and tracking settings.
All costs are in USD per 1K tokens.
"""
import os
from typing import Dict

# Token tracking configuration
TOKEN_TRACKING_ENABLED = os.getenv('TOKEN_TRACKING_ENABLED', 'true').lower() == 'true'
DISPLAY_REALTIME_USAGE = os.getenv('DISPLAY_REALTIME_USAGE', 'true').lower() == 'true'
SAVE_USAGE_REPORT = os.getenv('SAVE_USAGE_REPORT', 'true').lower() == 'true'

# Token costs per 1K tokens
TOKEN_COSTS = {
    # OpenAI Models
    'gpt-4-vision': {
        'input': 0.01,    # $0.01 per 1K input tokens
        'output': 0.03    # $0.03 per 1K output tokens
    },
    'gpt-4': {
        'input': 0.01,
        'output': 0.03
    },
    'gpt-3.5-turbo': {
        'input': 0.001,
        'output': 0.002
    },
    
    # Anthropic Models
    'claude-2': {
        'input': 0.008,
        'output': 0.024
    },
    'claude-instant': {
        'input': 0.0008,
        'output': 0.0024
    },
    'claude-3-5-sonnet-20241022': {
        'input': 0.003,    # $3 per million input tokens
        'output': 0.015    # $15 per million output tokens
    },
    
    # Google Models
    'gemini-2.0-flash-exp': {
        'input': 0.001,    # $1 per million input tokens
        'output': 0.002    # $2 per million output tokens
    },
    'gemini-1.5-pro': {
        'input': 0.00125,  # $1.25 per million input tokens
        'output': 0.005    # $5.00 per million output tokens
    },
    'gemini-pro-vision': {
        'input': 0.001,    # $1 per million input tokens
        'output': 0.002    # $2 per million output tokens
    },

    # Default rates (used if model not found)
    'default': {
        'input': 0.01,    # Default to GPT-4 rates
        'output': 0.03
    }
}

def get_token_cost_rates(model_name: str) -> dict:
    """
    Get the token cost rates for a specific model.
    Returns a dict with 'input' and 'output' rates per 1K tokens.
    Falls back to default rates if model not found.
    """
    return TOKEN_COSTS.get(model_name.lower(), TOKEN_COSTS['default'])

def calculate_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the total cost for a given number of input and output tokens.
    Args:
        model_name: Name of the model used
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
    Returns:
        Total cost in USD
    """
    if not TOKEN_TRACKING_ENABLED:
        return 0.0
        
    rates = get_token_cost_rates(model_name)
    input_cost = (input_tokens * rates['input']) / 1000
    output_cost = (output_tokens * rates['output']) / 1000
    return input_cost + output_cost

def get_cost_breakdown(model_name: str, input_tokens: int, output_tokens: int) -> dict:
    """
    Get a detailed breakdown of costs.
    Returns a dict with input cost, output cost, and total cost.
    """
    if not TOKEN_TRACKING_ENABLED:
        return {
            'input_cost': 0.0,
            'output_cost': 0.0,
            'total_cost': 0.0,
            'rates': {
                'input_rate': 0.0,
                'output_rate': 0.0
            }
        }
        
    rates = get_token_cost_rates(model_name)
    input_cost = (input_tokens * rates['input']) / 1000
    output_cost = (output_tokens * rates['output']) / 1000
    
    return {
        'input_cost': input_cost,
        'output_cost': output_cost,
        'total_cost': input_cost + output_cost,
        'rates': {
            'input_rate': rates['input'],
            'output_rate': rates['output']
        }
    }

def is_token_tracking_enabled() -> bool:
    """Check if token tracking is enabled."""
    return TOKEN_TRACKING_ENABLED

def should_display_realtime_usage() -> bool:
    """Check if realtime usage display is enabled."""
    return DISPLAY_REALTIME_USAGE and TOKEN_TRACKING_ENABLED

def should_save_usage_report() -> bool:
    """Check if usage report saving is enabled."""
    return SAVE_USAGE_REPORT and TOKEN_TRACKING_ENABLED
