"""
Configuration package for the Chinese Family Tree Processing System.
Contains token cost rates, model configurations, and other settings.
"""

from .token_costs import (
    TOKEN_COSTS,
    get_token_cost_rates,
    calculate_cost,
    get_cost_breakdown,
    is_token_tracking_enabled,
    should_display_realtime_usage,
    should_save_usage_report
)
from .config import (
    MODEL_CONFIGS,
    PROVIDER_CONFIGS,
    get_model_init_params,
    get_env_var_name
)

__all__ = [
    # Token costs and tracking
    'TOKEN_COSTS',
    'get_token_cost_rates',
    'calculate_cost',
    'get_cost_breakdown',
    'is_token_tracking_enabled',
    'should_display_realtime_usage',
    'should_save_usage_report',
    
    # Model configuration
    'MODEL_CONFIGS',
    'PROVIDER_CONFIGS',
    'get_model_init_params',
    'get_env_var_name'
]
