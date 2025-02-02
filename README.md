# Chinese Family Tree Processing System

A sophisticated system for processing Chinese family tree images through multiple stages of transcription, translation, and historical analysis using multiple LLM models.

## Features

- Multi-stage processing pipeline with 8 distinct stages
- Multiple LLM models working in parallel for accuracy
- Comprehensive token usage tracking and cost management
- Support for multiple LLM providers (OpenAI, Anthropic, Google)
- Detailed output reports with historical context

## System Architecture

### Core Components

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

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chinese-family-tree.git
cd chinese-family-tree
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

### Token Cost Configuration

Token costs are centrally managed in `src/config/token_costs.py`. Current rates:

- GPT-4/Vision: $0.01/1K input, $0.03/1K output
- GPT-3.5-Turbo: $0.001/1K input, $0.002/1K output
- Claude-2: $0.008/1K input, $0.024/1K output
- Gemini Pro: $0.001/1K input, $0.002/1K output

To update rates, modify the `TOKEN_COSTS` dictionary in `token_costs.py`.

### Model Configuration

Models are configured in `src/config/config.py`. You can:
- Assign different providers to each LLM
- Configure model parameters
- Set up provider-specific settings

### Confirmed Facts Configuration

The system uses a centralized facts file (`confirmed_facts_do_not_delete.md`) to provide consistent context across all processing stages. This file contains two types of facts:

1. **Document-Specific Facts**: Facts unique to the current document being processed
   - References to specific historical figures
   - Document-specific terminology
   - Unique contextual information

2. **Exercise-Wide Facts**: Facts that apply to all documents in the project
   - General information about the genealogy
   - Standard formatting conventions
   - Common terminology

To update confirmed facts:

1. Edit `confirmed_facts_do_not_delete.md` in the root directory
2. Maintain the existing structure:
   ```markdown
   # Confirmed Facts

   ## Document-Specific Facts
   - Fact 1
   - Fact 2

   ## Exercise-Wide Facts
   - Fact 1
   - Fact 2
   ```
3. Ensure facts are accurate and relevant
4. Keep the file name as `confirmed_facts_do_not_delete.md`
5. Commit changes to maintain version history

The system automatically includes these facts in every stage's prompt, ensuring consistent context throughout the processing pipeline.

## Usage

1. Process a single image:
```bash
python src/main.py process-image path/to/image.jpg
```

2. View token usage summary:
```bash
python src/main.py show-usage path/to/output.json
```

## Processing Pipeline

The system processes images through 8 distinct stages:

1. **Initial Transcription (Parallel)**
   - Three models (LLM1-3) independently transcribe the image
   - Ensures diverse initial interpretations

2. **Secondary Transcription (Parallel)**
   - Same models perform a second pass
   - Provides alternative perspectives

3. **Analysis and Recommendations (Parallel)**
   - Each model analyzes its own transcription pairs
   - Identifies discrepancies and suggests corrections

4. **Comprehensive Review (Parallel)**
   - Models review all previous transcriptions and analyses
   - Generates consolidated recommendations

5. **Final Analysis and Transcription**
   - LLM4 synthesizes all previous reviews
   - Produces authoritative transcription

6. **Punctuation Addition**
   - LLM4 adds modern Chinese punctuation
   - Enhances readability

7. **Translation**
   - LLM4 provides English translation with Pinyin
   - Ensures accessibility

8. **Historical Commentary**
   - LLM4 generates historical context
   - Adds cultural and genealogical insights

## Output

The system generates comprehensive output files containing:
- Final Chinese transcription with punctuation
- English translation with Pinyin annotations
- Historical commentary and analysis
- Detailed token usage and cost report

Output files are saved in `output/` with format:
```
transcription_[image]_[timestamp].md
transcription_[image]_[timestamp]_token_usage.json
```

## Token Usage Tracking

The system provides detailed token usage tracking:
- Real-time usage display
- Per-stage breakdowns
- Per-model statistics
- Cost calculations
- JSON reports

View token usage during or after processing:
```bash
python src/main.py show-usage --live  # Live tracking
python src/main.py show-usage path/to/report.json  # Saved report
```

## Error Handling

### Known Issues
A benign gRPC shutdown warning may appear after successful completion:
```
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
E0000 00:00:1738264116.131049 8410415 init.cc:232] grpc_wait_for_shutdown_with_timeout() timed out.
```
This is related to TensorFlow/gRPC cleanup and does not affect system functionality or output.

### Error Handling Features
The system includes comprehensive error handling:
- Validation at each processing stage
- Detailed error reporting
- Context window state logging
- Exception handling with cleanup

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Documentation

For detailed technical specifications and implementation details, see [specifications.md](specifications.md).
