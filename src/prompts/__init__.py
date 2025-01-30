"""
Prompts package for the Chinese Family Tree Processing System.
Contains stage-specific prompts and formatting utilities.
"""

from .stage_prompts import (
    Stage1,
    Stage2,
    Stage3,
    Stage4,
    Stage5,
    Stage6,
    Stage7,
    Stage8,
    format_prompt
)

__all__ = [
    'Stage1',
    'Stage2',
    'Stage3',
    'Stage4',
    'Stage5',
    'Stage6',
    'Stage7',
    'Stage8',
    'format_prompt'
]
