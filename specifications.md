# Chinese Family Tree Processing System Specifications

[Previous content through Output Management System section remains exactly as before]

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
