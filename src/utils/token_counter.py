"""
Utility for tracking token usage and costs across all stages and models.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import sys
import os
import tiktoken

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.token_costs import (
    calculate_cost,
    get_cost_breakdown,
    is_token_tracking_enabled,
    should_display_realtime_usage,
    should_save_usage_report
)

def count_tokens(text: str) -> int:
    """
    Count the number of tokens in a text string using GPT-4's tokenizer.
    
    Args:
        text: The text to count tokens for
        
    Returns:
        int: Number of tokens in the text
    """
    try:
        # Use GPT-4's tokenizer
        enc = tiktoken.encoding_for_model("gpt-4")
        return len(enc.encode(text))
    except Exception as e:
        print(f"Warning: Error counting tokens: {str(e)}")
        # Fallback to rough character-based estimate
        return len(text) // 4

@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int
    cost: float
    char_count: int = 0

class TokenTracker:
    def __init__(self):
        self.usage_by_stage: Dict[str, Dict[str, TokenUsage]] = {}
        self.stage_totals: Dict[str, TokenUsage] = {}
        self.grand_total = TokenUsage(0, 0, 0.0, 0)
        self.tracking_enabled = is_token_tracking_enabled()

    def add_usage(self, stage: str, model: str, model_name: str, input_tokens: int, output_tokens: int, char_count: Optional[int] = None):
        """Record token usage and character count for a specific stage and model."""
        if not self.tracking_enabled:
            return

        if stage not in self.usage_by_stage:
            self.usage_by_stage[stage] = {}
            self.stage_totals[stage] = TokenUsage(0, 0, 0.0, 0)

        # Calculate cost using centralized token costs
        cost = calculate_cost(model_name, input_tokens, output_tokens)

        char_count_value = char_count if char_count is not None else 0
        usage = TokenUsage(input_tokens, output_tokens, cost, char_count_value)
        usage_dict = {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'cost': cost,
            'char_count': char_count_value
        }
        self.usage_by_stage[stage][model] = usage_dict

        # Update stage totals
        stage_total = self.stage_totals[stage]
        stage_total.input_tokens += input_tokens
        stage_total.output_tokens += output_tokens
        stage_total.cost += cost
        stage_total.char_count += char_count_value

        # Update grand total
        self.grand_total.input_tokens += input_tokens
        self.grand_total.output_tokens += output_tokens
        self.grand_total.cost += cost
        self.grand_total.char_count += char_count_value

        # Display realtime usage if enabled
        if should_display_realtime_usage():
            self.print_stage_usage(stage)

    def print_stage_usage(self, stage: str):
        """Print token usage for a specific stage."""
        if not self.tracking_enabled or not should_display_realtime_usage():
            return

        if stage not in self.usage_by_stage:
            return

        print(f"\n=== {stage} Token Usage ===")
        for model, usage in self.usage_by_stage[stage].items():
            print(f"- {model}:")
            print(f"  - Input tokens:  {usage['input_tokens']:,}")
            print(f"  - Output tokens: {usage['output_tokens']:,}")
            print(f"  - Cost: ${usage['cost']:.4f}")
            if 'char_count' in usage:
                print(f"  - Chinese Characters: {usage['char_count']:,}")
        
        stage_total = self.stage_totals[stage]
        print(f"\nStage Totals:")
        print(f"- Total input tokens:  {stage_total.input_tokens:,}")
        print(f"- Total output tokens: {stage_total.output_tokens:,}")
        print(f"- Total cost: ${stage_total.cost:.4f}")
        if stage_total.char_count > 0:
            print(f"- Total Chinese Characters: {stage_total.char_count:,}")

    def print_summary(self):
        """Print complete summary of token usage and costs."""
        if not self.tracking_enabled:
            return
            
        print("\n=== Token Usage Summary ===")
        
        for stage in sorted(self.usage_by_stage.keys()):
            print(f"\n{stage}")
            stage_total = self.stage_totals[stage]
            print(f"- Input tokens:  {stage_total.input_tokens:,}")
            print(f"- Output tokens: {stage_total.output_tokens:,}")
            print(f"- Cost: ${stage_total.cost:.4f}")
            if stage_total.char_count > 0:
                print(f"- Chinese Characters: {stage_total.char_count:,}")

        print("\n=== Grand Totals ===")
        print(f"- Total input tokens:  {self.grand_total.input_tokens:,}")
        print(f"- Total output tokens: {self.grand_total.output_tokens:,}")
        print(f"- Total cost: ${self.grand_total.cost:.4f}")
        if self.grand_total.char_count > 0:
            print(f"- Total Chinese Characters: {self.grand_total.char_count:,}")

    def get_stage_metrics(self, stage: str) -> Optional[Dict[str, Any]]:
        """Get total metrics for a specific stage."""
        if not self.tracking_enabled or stage not in self.stage_totals:
            return None
            
        stage_total = self.stage_totals[stage]
        return {
            'input_tokens': stage_total.input_tokens,
            'output_tokens': stage_total.output_tokens,
            'cost': stage_total.cost,
            'char_count': stage_total.char_count
        }
        
    def get_stage_models(self, stage: str) -> List[Dict[str, Any]]:
        """Get detailed metrics for each model in a stage."""
        if not self.tracking_enabled or stage not in self.usage_by_stage:
            return []
            
        models = []
        for model_key, usage in self.usage_by_stage[stage].items():
            # Parse provider and model name from the model key
            # Format: "Stage X Model Y - Provider ModelName Type"
            parts = model_key.split(' - ')
            if len(parts) != 2:
                continue
            provider_model = parts[1].split(' ')
            provider = provider_model[0].lower()
            model_name = ' '.join(provider_model[1:-1])  # Exclude the last part (Type)
            
            model_data = {
                'provider': provider,
                'model_name': model_name,
                'input_tokens': usage['input_tokens'],
                'output_tokens': usage['output_tokens'],
                'cost': usage['cost']
            }
            if 'char_count' in usage:
                model_data['char_count'] = usage['char_count']
            models.append(model_data)
            
        return sorted(models, key=lambda x: (x['provider'], x['model_name']))
        
    def get_summary_dict(self) -> dict:
        """Get summary as a dictionary for saving to output file."""
        if not self.tracking_enabled:
            return {}

        summary = {
            'stages': {},
            'grand_total': {
                'input_tokens': self.grand_total.input_tokens,
                'output_tokens': self.grand_total.output_tokens,
                'cost': round(self.grand_total.cost, 4),
                'char_count': self.grand_total.char_count
            }
        }

        for stage, models in self.usage_by_stage.items():
            stage_data = {
                'models': {},
                'total': {
                    'input_tokens': self.stage_totals[stage].input_tokens,
                    'output_tokens': self.stage_totals[stage].output_tokens,
                    'cost': round(self.stage_totals[stage].cost, 4),
                    'char_count': self.stage_totals[stage].char_count
                }
            }
            
            for model, usage in models.items():
                model_data = {
                    'input_tokens': usage['input_tokens'],
                    'output_tokens': usage['output_tokens'],
                    'cost': round(usage['cost'], 4)
                }
                if 'char_count' in usage:
                    model_data['char_count'] = usage['char_count']
                stage_data['models'][model] = model_data
            
            summary['stages'][stage] = stage_data

        return summary

    def save_to_file(self, output_path: str):
        """Save token usage summary to a markdown file."""
        if not self.tracking_enabled or not should_save_usage_report():
            return
            
        summary = self.get_summary_dict()
        
        with open(output_path, 'w') as f:
            # Header
            f.write("# Token Usage and Cost Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Grand Totals
            f.write("## Grand Totals\n\n")
            f.write(f"- Total Input Tokens: {summary['grand_total']['input_tokens']:,}\n")
            f.write(f"- Total Output Tokens: {summary['grand_total']['output_tokens']:,}\n")
            f.write(f"- Total Cost: ${summary['grand_total']['cost']:.4f}\n")
            if summary['grand_total']['char_count'] > 0:
                f.write(f"- Total Chinese Characters: {summary['grand_total']['char_count']:,}\n")
            f.write("\n")
            
            # Stage-by-Stage Breakdown
            f.write("## Stage-by-Stage Breakdown\n\n")
            for stage, data in summary['stages'].items():
                f.write(f"### {stage}\n\n")
                
                # Stage totals
                f.write("#### Stage Totals\n")
                f.write(f"- Input Tokens: {data['total']['input_tokens']:,}\n")
                f.write(f"- Output Tokens: {data['total']['output_tokens']:,}\n")
                f.write(f"- Cost: ${data['total']['cost']:.4f}\n")
                if data['total']['char_count'] > 0:
                    f.write(f"- Total Chinese Characters: {data['total']['char_count']:,}\n")
                f.write("\n")
                
                # Per-model breakdown
                f.write("#### Model Breakdown\n")
                for model, usage in data['models'].items():
                    f.write(f"**{model}**\n")
                    f.write(f"- Input Tokens: {usage['input_tokens']:,}\n")
                    f.write(f"- Output Tokens: {usage['output_tokens']:,}\n")
                    f.write(f"- Cost: ${usage['cost']:.4f}\n")
                    if 'char_count' in usage:
                        f.write(f"- Chinese Characters: {usage['char_count']:,}\n")
                    f.write("\n")

    def get_detailed_cost_breakdown(self) -> dict:
        """Get a detailed breakdown of costs by stage and model."""
        if not self.tracking_enabled:
            return {}

        breakdown = {
            'stages': {},
            'grand_total': {
                'input_tokens': self.grand_total.input_tokens,
                'output_tokens': self.grand_total.output_tokens,
                'cost': round(self.grand_total.cost, 4)
            }
        }

        for stage, models in self.usage_by_stage.items():
            stage_breakdown = {
                'models': {},
                'total': get_cost_breakdown(
                    'default',  # Use default rates for stage totals
                    self.stage_totals[stage].input_tokens,
                    self.stage_totals[stage].output_tokens
                )
            }
            
            for model, usage in models.items():
                stage_breakdown['models'][model] = get_cost_breakdown(
                    model,
                    usage.input_tokens,
                    usage.output_tokens
                )
            
            breakdown['stages'][stage] = stage_breakdown

        return breakdown
