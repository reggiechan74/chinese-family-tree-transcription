import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from models.model_interfaces import TranscriptionModel, ReviewModel, FinalStageModel
from models.model_factory import ModelFactory
from utils.token_counter import count_tokens, TokenTracker

class ModelManager:
    """
    Manages the lifecycle and execution of models across all stages.
    """
    
    def __init__(self):
        """Initialize the model manager."""
        self.output_dir = None
        self.timestamp = None
        self.start_time = None
        self.token_tracker = TokenTracker()
        
    def initialize_run(self, output_dir: str):
        """Initialize a new processing run."""
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.start_time = datetime.now()
        os.makedirs(output_dir, exist_ok=True)
        
    def _get_processing_time(self) -> float:
        """Get processing time in seconds."""
        if not self.start_time:
            return 0.0
        return (datetime.now() - self.start_time).total_seconds()
        
    def _save_stage_output(self, stage_num: int, content: str, base_path: str, timestamp: str, next_stage_data: Dict[str, str] = None, input_data: Dict[str, str] = None):
        """Save stage output to a markdown file."""
        if not self.output_dir or not self.timestamp:
            raise RuntimeError("Output directory not initialized")
            
        filename = f"Stage{stage_num}_{timestamp}.md"
        filepath = os.path.join(base_path, filename)
        
        # Calculate total token count and cost for this stage
        input_tokens = 0
        output_tokens = 0
        total_cost = 0.0
        
        # Count input tokens
        if input_data:
            for data in input_data.values():
                input_tokens += count_tokens(data)
                
        # Count output tokens (from generated content and next stage data)
        output_tokens += count_tokens(content)
        if next_stage_data:
            for data in next_stage_data.values():
                output_tokens += count_tokens(data)
                
        # Calculate total cost using the model's rates
        model = ModelFactory.create_model(stage_num, 1)  # Use first model's rates for the stage
        from config.token_costs import calculate_cost
        total_cost = calculate_cost(model.model_name, input_tokens, output_tokens)
        total_tokens = input_tokens + output_tokens
        
        # Format processing time as minutes and seconds
        processing_time = self._get_processing_time()
        minutes = int(processing_time // 60)
        seconds = processing_time % 60
        time_str = f"{minutes}m {seconds:.2f}s"

        # Add header with processing time and totals
        header = f"# Stage {stage_num} Output\n\n"
        header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += f"Processing Time: {time_str}\n"
        header += f"Total Token Count: {total_tokens:,} tokens\n"
        header += f"Total Cost: ${total_cost:.4f}\n\n"
        
        # Part 1: Input from Previous Stage
        part1 = "## Input from Previous Stage\n\n"
        if stage_num == 1:
            part1 += "No input from previous stage\n\n"
        elif input_data:
            for key, data in input_data.items():
                token_count = count_tokens(data)
                part1 += f"### {key}\n"
                part1 += f"Token count: {token_count:,} tokens\n"
                part1 += f"```\n{data}\n```\n\n"
        
        # Part 2: Generated Output
        part2 = "## Generated Output\n\n"
        if next_stage_data:
            total_tokens = 0
            for key, data in next_stage_data.items():
                token_count = count_tokens(data)
                total_tokens += token_count
                part2 += f"### {key}\n"
                part2 += f"Token count: {token_count:,} tokens\n"
                part2 += f"```\n{data}\n```\n\n"
            part2 += f"\nTotal tokens being passed to next stage: {total_tokens:,} tokens\n"
        else:
            part2 += "No data passed to next stage (final stage)\n"
        
        # Write complete output
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header + part1 + part2)
        print(f"- Stage {stage_num} output saved to: {filepath}")
        
    def run_stage1(self, image_base64: str) -> Dict[str, str]:
        """Run Stage 1 - Initial Transcription."""
        stage_num = 1
        results = {}
        
        # Create models
        models = []
        for model_num in range(1, 4):
            model = ModelFactory.create_model(stage_num, model_num)
            models.append(model)
            
        # Run transcriptions in parallel
        for i, model in enumerate(models, 1):
            try:
                result = model.generate_transcription(image_base64, self.token_tracker)
                key = f"Stage {stage_num} Model {i} - {model.provider.title()} {model.model_name} Transcription"
                results[key] = result
            except Exception as e:
                raise RuntimeError(f"Failed to complete Stage {stage_num} Model {i}: {str(e)}")
                
        # Save stage output
        self._save_stage_output(stage_num, str(results), self.output_dir, self.timestamp, results)
        return results
        
    def run_stage2(self, image_base64: str) -> Dict[str, str]:
        """Run Stage 2 - Secondary Transcription."""
        stage_num = 2
        results = {}
        
        # Create models
        models = []
        for model_num in range(1, 4):
            model = ModelFactory.create_model(stage_num, model_num)
            models.append(model)
            
        # Run transcriptions in parallel
        for i, model in enumerate(models, 1):
            try:
                result = model.generate_transcription(image_base64, self.token_tracker)
                key = f"Stage {stage_num} Model {i} - {model.provider.title()} {model.model_name} Transcription"
                results[key] = result
            except Exception as e:
                raise RuntimeError(f"Failed to complete Stage {stage_num} Model {i}: {str(e)}")
                
        # Save stage output
        self._save_stage_output(stage_num, str(results), self.output_dir, self.timestamp, results)
        return results
        
    def run_stage3(self, stage1_results: Dict[str, str], stage2_results: Dict[str, str]) -> Dict[str, str]:
        """Run Stage 3 - Initial Review."""
        stage_num = 3
        results = {}
        
        # Create models
        models = []
        for model_num in range(1, 4):
            model = ModelFactory.create_model(stage_num, model_num)
            models.append(model)
            
        # Run analyses in parallel
        for i, model in enumerate(models, 1):
            try:
                # Create context with corresponding Stage 1 and 2 results
                context = {}
                for stage in [1, 2]:
                    key = f"Stage {stage} Model {i} - {model.provider.title()} {model.model_name} Transcription"
                    if key in (stage1_results if stage == 1 else stage2_results):
                        context[key] = stage1_results[key] if stage == 1 else stage2_results[key]
                
                result = model.analyze_context(context, self.token_tracker)
                key = f"Stage {stage_num} Model {i} - {model.provider.title()} {model.model_name} Review"
                results[key] = result
            except Exception as e:
                raise RuntimeError(f"Failed to complete Stage {stage_num} Model {i}: {str(e)}")
                
        # Save stage output
        input_data = {**stage1_results, **stage2_results}
        self._save_stage_output(stage_num, str(results), self.output_dir, self.timestamp, results, input_data)
        return results
        
    def run_stage4(self, stage3_results: Dict[str, str]) -> Dict[str, str]:
        """Run Stage 4 - Comprehensive Review."""
        stage_num = 4
        results = {}
        
        # Create models
        models = []
        for model_num in range(1, 4):
            model = ModelFactory.create_model(stage_num, model_num)
            models.append(model)
            
        # Run comprehensive reviews in parallel
        for i, model in enumerate(models, 1):
            try:
                result = model.comprehensive_review(stage3_results, self.token_tracker)
                key = f"Stage {stage_num} Model {i} - {model.provider.title()} {model.model_name} Review"
                results[key] = result
            except Exception as e:
                raise RuntimeError(f"Failed to complete Stage {stage_num} Model {i}: {str(e)}")
                
        # Save stage output
        self._save_stage_output(stage_num, str(results), self.output_dir, self.timestamp, results, stage3_results)
        return results
        
    def run_stage5(self, stage4_results: Dict[str, str]) -> str:
        """Run Stage 5 - Final Transcription."""
        stage_num = 5
        
        # Create model
        model = ModelFactory.create_model(stage_num, 1)
        
        try:
            result = model.generate_final_transcription(stage4_results, self.token_tracker)
            key = f"Stage {stage_num} Model 1 - {model.provider.title()} {model.model_name} Final Transcription"
            results = {key: result}
        except Exception as e:
            raise RuntimeError(f"Failed to complete Stage {stage_num}: {str(e)}")
            
        # Save stage output
        self._save_stage_output(stage_num, str(results), self.output_dir, self.timestamp, results, stage4_results)
        return result
        
    def run_stage6(self, final_transcription: str) -> str:
        """Run Stage 6 - Add Punctuation."""
        stage_num = 6
        
        # Create model
        model = ModelFactory.create_model(stage_num, 1)
        
        try:
            result = model.add_punctuation(final_transcription, self.token_tracker)
            key = f"Stage {stage_num} Model 1 - {model.provider.title()} {model.model_name} Punctuated Transcription"
            results = {key: result}
        except Exception as e:
            raise RuntimeError(f"Failed to complete Stage {stage_num}: {str(e)}")
            
        # Save stage output
        input_data = {"Final Transcription": final_transcription}
        self._save_stage_output(stage_num, str(results), self.output_dir, self.timestamp, results, input_data)
        return result
        
    def run_stage7(self, punctuated_text: str) -> str:
        """Run Stage 7 - Translation."""
        stage_num = 7
        
        # Create model
        model = ModelFactory.create_model(stage_num, 1)
        
        try:
            result = model.translate_to_english(punctuated_text, self.token_tracker)
            key = f"Stage {stage_num} Model 1 - {model.provider.title()} {model.model_name} Translation"
            results = {key: result}
        except Exception as e:
            raise RuntimeError(f"Failed to complete Stage {stage_num}: {str(e)}")
            
        # Save stage output
        input_data = {"Punctuated Text": punctuated_text}
        self._save_stage_output(stage_num, str(results), self.output_dir, self.timestamp, results, input_data)
        return result
        
    def process_image(self, image_base64: str, token_tracker: Optional[TokenTracker] = None) -> Dict[str, str]:
        """
        Process an image through all stages of the pipeline.
        
        Args:
            image_base64: Base64 encoded image string
            token_tracker: Optional token tracker for monitoring usage
            
        Returns:
            Dict containing all final outputs:
            - final_transcription: Final Chinese text without punctuation
            - punctuated_text: Chinese text with punctuation
            - translation: English translation
            - commentary: Historical commentary
        """
        # Use provided token tracker if available
        if token_tracker:
            self.token_tracker = token_tracker
            
        # Create output directory if not initialized
        if not self.output_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.initialize_run(f"output/run_{timestamp}")
        try:
            # Stage 1: Initial Transcription
            stage1_results = self.run_stage1(image_base64)
            
            # Stage 2: Secondary Transcription
            stage2_results = self.run_stage2(image_base64)
            
            # Stage 3: Initial Review
            stage3_results = self.run_stage3(stage1_results, stage2_results)
            
            # Stage 4: Comprehensive Review
            stage4_results = self.run_stage4(stage3_results)
            
            # Stage 5: Final Transcription
            final_transcription = self.run_stage5(stage4_results)
            
            # Stage 6: Add Punctuation
            punctuated_text = self.run_stage6(final_transcription)
            
            # Stage 7: Translation
            translation = self.run_stage7(punctuated_text)
            
            # Stage 8: Historical Commentary
            commentary = self.run_stage8(punctuated_text, translation)
            
            # Generate final summary report
            self._save_summary_report()
            
            # Generate final presentation report
            self._save_presentation_report(
                punctuated_text=punctuated_text,
                translation=translation,
                commentary=commentary
            )
            
            return {
                'final_transcription': final_transcription,
                'punctuated_text': punctuated_text,
                'translation': translation,
                'commentary': commentary
            }
        except Exception as e:
            raise RuntimeError(f"Error processing image: {str(e)}")
            
    def _save_presentation_report(self, punctuated_text: str, translation: str, commentary: str):
        """Generate and save a final presentation report in markdown format."""
        if not self.output_dir or not self.timestamp:
            raise RuntimeError("Output directory not initialized")
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"presentation_report_{timestamp}.md")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Chinese Family Tree Analysis\n\n")
            
            # Part 1: Chinese Text
            f.write("## Part 1: Chinese Text\n\n")
            f.write(f"{punctuated_text}\n\n")
            
            # Part 2: English Translation
            f.write("## Part 2: English Translation\n\n")
            f.write(f"{translation}\n\n")
            
            # Part 3: Historical Commentary
            f.write("## Part 3: Historical Commentary\n\n")
            f.write(f"{commentary}\n")
            
    def _save_summary_report(self):
        """Generate and save a final summary report in markdown format."""
        if not self.output_dir or not self.timestamp:
            raise RuntimeError("Output directory not initialized")
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(self.output_dir, f"summary_report_{timestamp}.md")
        
        # Collect stage metrics
        stages = []
        total_processing_time = self._get_processing_time()
        total_input_tokens = 0
        total_output_tokens = 0
        total_cost = 0.0
        
        for stage_num in range(1, 9):
            model = ModelFactory.create_model(stage_num, 1)  # Use first model's rates
            stage_metrics = self.token_tracker.get_stage_metrics(f"Stage {stage_num}")
            if stage_metrics:
                total_input_tokens += stage_metrics['input_tokens']
                total_output_tokens += stage_metrics['output_tokens']
                total_cost += stage_metrics['cost']
                stages.append({
                    'stage': stage_num,
                    'input_tokens': stage_metrics['input_tokens'],
                    'output_tokens': stage_metrics['output_tokens'],
                    'cost': stage_metrics['cost']
                })
        
        # Generate markdown report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Processing Summary Report\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            # Format total processing time
            minutes = int(total_processing_time // 60)
            seconds = total_processing_time % 60
            time_str = f"{minutes}m {seconds:.2f}s"
            f.write(f"Total Processing Time: {time_str}\n\n")
            
            # Write detailed stage metrics table
            f.write("## Stage-by-Stage Metrics\n\n")
            
            # Track provider/model totals
            provider_model_totals = {}  # {(provider, model_name): {'input': X, 'output': Y, 'cost': Z}}
            
            for stage_num in range(1, 9):
                stage_metrics = self.token_tracker.get_stage_metrics(f"Stage {stage_num}")
                if not stage_metrics:
                    continue
                    
                f.write(f"### Stage {stage_num}\n\n")
                f.write("| Model | Input Tokens | Output Tokens | Cost ($) |\n")
                f.write("|-------|--------------|---------------|----------|\n")
                
                stage_input = 0
                stage_output = 0
                stage_cost = 0.0
                
                # Get all models used in this stage
                stage_models = self.token_tracker.get_stage_models(f"Stage {stage_num}")
                for model_info in stage_models:
                    provider = model_info['provider']
                    model_name = model_info['model_name']
                    input_tokens = model_info['input_tokens']
                    output_tokens = model_info['output_tokens']
                    cost = model_info['cost']
                    
                    # Update provider/model totals
                    key = (provider, model_name)
                    if key not in provider_model_totals:
                        provider_model_totals[key] = {'input': 0, 'output': 0, 'cost': 0.0}
                    provider_model_totals[key]['input'] += input_tokens
                    provider_model_totals[key]['output'] += output_tokens
                    provider_model_totals[key]['cost'] += cost
                    
                    # Write model row
                    f.write(f"| {provider.title()} {model_name} | {input_tokens:,} | {output_tokens:,} | ${cost:.4f} |\n")
                    
                    stage_input += input_tokens
                    stage_output += output_tokens
                    stage_cost += cost
                
                # Write stage total row
                f.write("|-------|--------------|---------------|----------|\n")
                f.write(f"| **Stage {stage_num} Total** | **{stage_input:,}** | **{stage_output:,}** | **${stage_cost:.4f}** |\n\n")
            
            # Write grand total row
            f.write("### Pipeline Totals\n\n")
            f.write("| Stage | Input Tokens | Output Tokens | Cost ($) |\n")
            f.write("|-------|--------------|---------------|----------|\n")
            f.write(f"| **TOTAL** | **{total_input_tokens:,}** | **{total_output_tokens:,}** | **${total_cost:.4f}** |\n\n")
            
            # Write provider/model summary table
            f.write("## Provider and Model Summary\n\n")
            f.write("| Provider | Model | Input Tokens | Output Tokens | Cost ($) |\n")
            f.write("|----------|-------|--------------|---------------|----------|\n")
            
            provider_totals = {}  # {provider: {'input': X, 'output': Y, 'cost': Z}}
            
            # Write rows sorted by provider and model
            for (provider, model_name), totals in sorted(provider_model_totals.items()):
                f.write(f"| {provider.title()} | {model_name} | {totals['input']:,} | {totals['output']:,} | ${totals['cost']:.4f} |\n")
                
                # Update provider totals
                if provider not in provider_totals:
                    provider_totals[provider] = {'input': 0, 'output': 0, 'cost': 0.0}
                provider_totals[provider]['input'] += totals['input']
                provider_totals[provider]['output'] += totals['output']
                provider_totals[provider]['cost'] += totals['cost']
            
            # Write provider subtotals
            f.write("|----------|-------|--------------|---------------|----------|\n")
            for provider, totals in sorted(provider_totals.items()):
                f.write(f"| **{provider.title()} Total** | | **{totals['input']:,}** | **{totals['output']:,}** | **${totals['cost']:.4f}** |\n")
            
            # Add processing time summary
            f.write("## Time Summary\n\n")
            # Format processing times
            avg_time = total_processing_time / len(stages)
            avg_minutes = int(avg_time // 60)
            avg_seconds = avg_time % 60
            avg_time_str = f"{avg_minutes}m {avg_seconds:.2f}s"
            
            f.write(f"- Total Processing Time: {time_str}\n")
            f.write(f"- Average Time per Stage: {avg_time_str}\n\n")
            
            # Add token usage summary
            f.write("## Token Usage Summary\n\n")
            f.write(f"- Total Input Tokens: {total_input_tokens:,}\n")
            f.write(f"- Total Output Tokens: {total_output_tokens:,}\n")
            f.write(f"- Total Tokens: {total_input_tokens + total_output_tokens:,}\n\n")
            
            # Add cost summary
            f.write("## Cost Summary\n\n")
            f.write(f"- Total Cost: ${total_cost:.4f}\n")
            f.write(f"- Average Cost per Stage: ${(total_cost / len(stages)):.4f}\n")
            f.write(f"- Cost per 1K Tokens: ${(total_cost * 1000 / (total_input_tokens + total_output_tokens)):.4f}\n")
            
    def run_stage8(self, chinese_text: str, english_text: str) -> str:
        """Run Stage 8 - Historical Commentary."""
        stage_num = 8
        
        # Create model
        model = ModelFactory.create_model(stage_num, 1)
        
        try:
            result = model.generate_commentary(chinese_text, english_text, self.token_tracker)
            key = f"Stage {stage_num} Model 1 - {model.provider.title()} {model.model_name} Commentary"
            results = {key: result}
        except Exception as e:
            raise RuntimeError(f"Failed to complete Stage {stage_num}: {str(e)}")
            
        # Save stage output
        input_data = {
            "Chinese Text": chinese_text,
            "English Translation": english_text
        }
        self._save_stage_output(stage_num, str(results), self.output_dir, self.timestamp, results, input_data)
        return result
