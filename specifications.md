# Chinese Family Tree Processing System Specifications

# System Components

## Model Providers and Capabilities

### Vision + Language Models
- OpenAI
  * gpt-4-turbo
  * gpt-4-vision-preview

- Anthropic
  * claude-3-opus-20240229 (4096 max output tokens)
  * claude-3-5-sonnet-20241022 (8192 max output tokens)

- Google
  * gemini-2.0-flash-exp
  * gemini-1.5-pro
  * gemini-exp-1206
  * gemini-pro-vision

- OpenRouter
  * meta-llama/llama-3.2-90b-vision-instruct
  * x-ai/grok-2-vision-1212

### Language-Only Models
- Google
  * gemini-pro

- OpenRouter
  * deepseek/deepseek-r1:free

- Groq
  * llama-3.2-90b-vision-preview
  * deepseek-r1-distill-llama-70b
  * mixtral-8x7b-32768
  * llama2-70b-4096
  * llama-3.3-70b-versatile

## Directory Structure

```
src/
├── config/               # Configuration management
│   ├── __init__.py
│   ├── token_costs.py   # Token cost rates and calculations
│   └── config.py        # System configuration and model providers
├── models/              # LLM model implementations
│   ├── __init__.py
│   ├── model_interfaces.py  # Base interfaces for model types
│   ├── model_factory.py    # Factory for creating model instances
│   ├── model_manager.py    # Manages model lifecycle and interactions
│   └── stage_model.py      # Stage-specific model implementation
├── prompts/             # Stage-specific prompts
│   ├── __init__.py
│   └── stage_prompts.py    # Prompts for each processing stage
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── image_utils.py      # Image processing utilities
│   └── token_counter.py    # Token usage tracking
└── output/              # Generated output files

cline_docs/              # System documentation
├── projectRoadmap.md    # Project goals and progress
├── currentTask.md       # Current objectives and context
├── techStack.md         # Technology decisions
└── codebaseSummary.md   # Project structure overview
```

## Model Management System

### Provider Configuration
- API key management through environment variables
- Model capability validation
- Token limit handling
  * Claude-3 Opus: 4096 max output tokens
  * Claude-3 Sonnet: 8192 max output tokens
  * Other models: Provider-specific limits

### Model Factory
- Stage-specific model instantiation
- Provider-specific client initialization
- Capability validation for each stage

### Model Manager
- Model lifecycle management
- Token usage tracking
- Error handling and recovery

## Output Management System

### Output Directory Structure
```
run_YYYYMMDD_HHMMSS/
├── Stage1_YYYYMMDD_HHMMSS.md
├── Stage2_YYYYMMDD_HHMMSS.md
...
├── Stage8_YYYYMMDD_HHMMSS.md
└── summary_report_YYYYMMDD_HHMMSS.md
```

### Stage Output Format
```markdown
# Stage N Output
Generated: YYYY-MM-DD HH:MM:SS
Processing Time: Xm XX.XXs
Total Token Count: X,XXX tokens
Total Cost: $X.XXXX

## Input from Previous Stage
[Input data with token counts]

## Generated Output
[Output data with token counts]
Total tokens being passed to next stage: X,XXX tokens
```

### Summary Report Format
```markdown
# Processing Summary Report
Generated: YYYY-MM-DD HH:MM:SS
Total Processing Time: Xm XX.XXs

## Stage-by-Stage Metrics
### Stage 1
| Model | Input Tokens | Output Tokens | Cost ($) |
|-------|-------------|---------------|----------|
[Model-specific metrics]
| **Stage 1 Total** | **X,XXX** | **X,XXX** | **$X.XX** |

## Provider and Model Summary
| Provider | Model | Input Tokens | Output Tokens | Cost ($) |
|----------|-------|--------------|---------------|----------|
[Provider/model metrics with subtotals]

## Time Summary
- Total Processing Time: Xm XX.XXs
- Average Time per Stage: Xm XX.XXs

## Token Usage Summary
- Total Input Tokens: X,XXX
- Total Output Tokens: X,XXX
- Total Tokens: X,XXX

## Cost Summary
- Total Cost: $X.XX
- Average Cost per Stage: $X.XX
- Cost per 1K Tokens: $X.XX
```

### OutputManager Class
```python
class OutputManager:
    def __init__(self, token_tracker: TokenTracker):
        self.token_tracker = token_tracker
        self.output_dir = None
        self.timestamp = None

    def initialize_run(self, output_dir: str):
        """Initialize a new processing run."""
        # Create timestamped directory
        # Set up output paths

    def save_stage_output(self, stage_num: int, content: str,
                         next_stage_data: Dict[str, str] = None,
                         input_data: Dict[str, str] = None):
        """Save stage output to a markdown file."""
        # Calculate token counts and costs
        # Format processing time as minutes and seconds
        # Generate two-part output file
        # Save to timestamped file

    def generate_summary_report(self):
        """Generate and save final summary report."""
        # Collect metrics from token tracker
        # Generate detailed breakdown tables
        # Calculate efficiency metrics
        # Format processing times
        # Save to timestamped report file
```

[Rest of the content remains exactly as before]
