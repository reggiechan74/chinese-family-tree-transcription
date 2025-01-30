# Chinese Family Tree Processing System Specifications

## System Overview

The Chinese Family Tree Processing System is a sophisticated multi-stage pipeline designed to process, analyze, and translate Chinese family tree images using multiple Large Language Models (LLMs). The system employs a parallel validation approach in early stages followed by specialized processing in later stages.

## Technical Requirements

### Environment Requirements
- Python 3.8+
- Required API keys:
  - OpenAI API key (GPT-4/Vision)
  - Anthropic API key (Claude-2)
  - Google API key (Gemini Pro)
- Sufficient disk space for image processing and output storage
- Memory requirements based on image size and processing needs

### Dependencies
- PIL/Pillow for image processing
- OpenAI API client
- Anthropic API client
- Google GenerativeAI client
- Additional utilities as specified in requirements.txt

## Processing Pipeline

### Stage 1: Initial Transcription (Parallel)
- **Purpose**: Generate initial independent transcriptions from image
- **Models**: LLM1, LLM2, LLM3 working in parallel
- **Input**: Raw image file
- **Output**: Three independent transcriptions (one from each model)
- **Validation**: Non-empty content verification
- **Note**: Independent operation, no cross-model communication

**Pseudocode**:
```python
def stage1_initial_transcription(image_path):
    # Initialize models in parallel
    models = [LLM1(), LLM2(), LLM3()]
    transcriptions = []
    
    # Process image in parallel
    for model in models:
        transcription = model.generate_transcription(image_path)
        validate_transcription(transcription)
        transcriptions.append(transcription)
    
    return transcriptions
```

### Stage 2: Secondary Transcription (Parallel)
- **Purpose**: Generate second set of independent transcriptions
- **Models**: LLM1, LLM2, LLM3 working in parallel
- **Input**: Same image file
- **Output**: Three additional independent transcriptions
- **Validation**: Content verification
- **Note**: Independent from Stage 1, provides second perspective

**Pseudocode**:
```python
def stage2_secondary_transcription(image_path):
    # Use same models for second pass
    models = [LLM1(), LLM2(), LLM3()]
    transcriptions = []
    
    # Generate second set of transcriptions
    for model in models:
        transcription = model.generate_transcription(image_path)
        validate_transcription(transcription)
        transcriptions.append(transcription)
    
    return transcriptions
```

### Stage 3: Analysis and Recommendations (Parallel)
- **Purpose**: Each model analyzes its own Stage 1 vs Stage 2 transcriptions
- **Models**: LLM1, LLM2, LLM3 working in parallel
- **Input**: Each model analyzes its respective pair of transcriptions
- **Output**: Three sets of analysis and recommendations
- **Validation**: Analysis completeness verification
- **Note**: Each model focuses on reconciling its own transcription differences

**Pseudocode**:
```python
def stage3_analysis(stage1_results, stage2_results):
    analyses = []
    
    # Each model analyzes its own transcriptions
    for i, model in enumerate([LLM1(), LLM2(), LLM3()]):
        analysis = model.analyze_context(
            stage1_results[i],
            stage2_results[i]
        )
        validate_analysis(analysis)
        analyses.append(analysis)
    
    return analyses
```

### Stage 4: Comprehensive Review (Parallel)
- **Purpose**: Each model performs comprehensive review of all previous data
- **Models**: LLM1, LLM2, LLM3 working in parallel
- **Input**: 
  * All Stage 1 transcriptions from all models
  * All Stage 2 transcriptions from all models
  * All Stage 3 analyses and recommendations
- **Output**: Three comprehensive reviews
- **Validation**: Complete review verification
- **Note**: Each model has full access to all previous transcriptions and analyses

**Pseudocode**:
```python
def stage4_comprehensive_review(stage1_results, stage2_results, stage3_analyses):
    reviews = []
    
    # Each model reviews all previous data
    for model in [LLM1(), LLM2(), LLM3()]:
        review = model.comprehensive_review(
            stage1_results,
            stage2_results,
            stage3_analyses
        )
        validate_review(review)
        reviews.append(review)
    
    return reviews
```

### Stage 5: Final Analysis and Transcription
- **Purpose**: Generate final authoritative analysis and transcription
- **Model**: LLM4
- **Input**: All three Stage 4 comprehensive reviews
- **Output**: Final analysis and recommended transcription
- **Validation**: Content completeness and quality check
- **Note**: Synthesizes insights from all previous parallel processing

**Pseudocode**:
```python
def stage5_final_transcription(stage4_reviews):
    llm4 = LLM4()
    
    # Generate final transcription
    final_transcription = llm4.generate_final_transcription(stage4_reviews)
    validate_final_transcription(final_transcription)
    
    return final_transcription
```

### Stage 6: Punctuation Addition
- **Purpose**: Add modern Chinese punctuation
- **Model**: LLM4
- **Input**: Final transcription
- **Output**: Punctuated transcription
- **Validation**: Punctuation accuracy check

**Pseudocode**:
```python
def stage6_add_punctuation(final_transcription):
    llm4 = LLM4()
    
    # Add punctuation
    punctuated_text = llm4.add_punctuation(final_transcription)
    validate_punctuation(punctuated_text)
    
    return punctuated_text
```

### Stage 7: Translation
- **Purpose**: English translation with Pinyin
- **Model**: LLM4
- **Input**: Punctuated transcription
- **Output**: English translation with Pinyin annotations
- **Validation**: Translation completeness check

**Pseudocode**:
```python
def stage7_translation(punctuated_text):
    llm4 = LLM4()
    
    # Generate translation with Pinyin
    translation = llm4.translate_to_english(punctuated_text)
    validate_translation(translation)
    
    return translation
```

### Stage 8: Historical Commentary
- **Purpose**: Generate historical context and analysis
- **Model**: LLM4
- **Input**: English translation
- **Output**: Detailed historical commentary
- **Validation**: Commentary completeness check

**Pseudocode**:
```python
def stage8_historical_commentary(translation):
    llm4 = LLM4()
    
    # Generate historical context
    commentary = llm4.generate_commentary(translation)
    validate_commentary(commentary)
    
    return commentary
```

## Main Process Flow

**Pseudocode**:
```python
def process_family_tree_image(image_path):
    try:
        # Initialize token tracking
        token_tracker = TokenTracker()
        
        # Stage 1: Initial parallel transcription
        stage1_results = stage1_initial_transcription(image_path)
        
        # Stage 2: Secondary parallel transcription
        stage2_results = stage2_secondary_transcription(image_path)
        
        # Stage 3: Individual analyses
        stage3_analyses = stage3_analysis(stage1_results, stage2_results)
        
        # Stage 4: Comprehensive review
        stage4_reviews = stage4_comprehensive_review(
            stage1_results,
            stage2_results,
            stage3_analyses
        )
        
        # Stage 5: Final transcription
        final_transcription = stage5_final_transcription(stage4_reviews)
        
        # Stage 6: Add punctuation
        punctuated_text = stage6_add_punctuation(final_transcription)
        
        # Stage 7: Translation
        translation = stage7_translation(punctuated_text)
        
        # Stage 8: Historical commentary
        commentary = stage8_historical_commentary(translation)
        
        # Generate final output
        generate_output_files(
            final_transcription,
            punctuated_text,
            translation,
            commentary,
            token_tracker.get_usage_report()
        )
        
    except Exception as e:
        handle_error(e)
        raise
```

## Model Specifications

### LLM1-3 (Early Stage Models)
- **Interface**: BaseModel
- **Required Methods**:
  - generate_transcription()
  - analyze_context()
  - comprehensive_review()
  - count_tokens()
- **Provider Options**: OpenAI, Anthropic, Google
- **Configuration**: Via config.py and environment variables
- **Token Limits**:
  - Gemini: Input handled by API (2M limit), 32,768 output tokens
  - Claude-3.5-sonnet: 8,192 tokens
  - GPT-4: 4,096 tokens

### LLM4 (Final Stage Model)
- **Interface**: FinalStageModel
- **Required Methods**:
  - generate_final_transcription()
  - add_punctuation()
  - translate_to_english()
  - generate_commentary()
  - count_tokens()
- **Provider**: Configurable via factory
- **Configuration**: Via config.py and environment variables
- **Token Limits**: Same as LLM1-3 based on selected provider

## Token Management

### Token Limits and Handling
- **Gemini Models**:
  - Input tokens: 2M limit (handled automatically by API)
  - Output tokens: 32,768 maximum
  - No need to specify input token limit
- **Claude Models**:
  - Maximum tokens: 8,192
  - Single max_tokens parameter for output
- **OpenAI Models**:
  - Maximum tokens: 4,096
  - Optional max_tokens parameter for output

### Tracking Configuration
- TOKEN_TRACKING_ENABLED (default: true)
- DISPLAY_REALTIME_USAGE (default: true)
- SAVE_USAGE_REPORT (default: true)

### Cost Rates (per 1K tokens)
- GPT-4/Vision: $0.01 input, $0.03 output
- GPT-3.5-Turbo: $0.001 input, $0.002 output
- Claude-2: $0.008 input, $0.024 output
- Gemini Pro: $0.001 input, $0.002 output

## Output Specifications

### Results File (transcription_[image]_[timestamp].md)
- Generated: [Date and Time]
- Final transcription with punctuation
- English translation with Pinyin
- Historical commentary
- Processing metadata:
  * Date and time of processing
  * Image file name
  * System version

### Token Usage Report (transcription_[image]_[timestamp]_token_usage.json)
- Per-stage token usage:
  * Input tokens per model
  * Output tokens per model
  * Cost per model
  * Stage total tokens and cost
- Per-model statistics:
  * Total input tokens
  * Total output tokens
  * Total cost
- Grand Totals:
  * Total input tokens across all stages
  * Total output tokens across all stages
  * Total cost for entire process
- Processing timestamps

## Error Handling

### Known Issues
- gRPC shutdown timeout warning may appear after successful completion:
  ```
  WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
  E0000 00:00:1738264116.131049 8410415 init.cc:232] grpc_wait_for_shutdown_with_timeout() timed out.
  ```
  This is a benign warning related to TensorFlow/gRPC cleanup and does not affect system functionality or output.

### Validation Requirements
- Non-empty content verification
- Stage completion verification
- Data consistency checks
- Token tracking validation

### Error Recovery
- Detailed error reporting
- Context window state logging
- Stage-specific error messages
- Exception handling with cleanup

## Performance Considerations

### Optimization Areas
- Token usage efficiency
- Image preprocessing
- Context window management
- Memory utilization

### Recommended Limits
- Maximum image size: Based on provider limits
- Token context windows: Provider-specific
- Concurrent processing: Based on API rate limits

## Security Requirements

### API Key Management
- Secure storage in .env file
- No hardcoded credentials
- Environment variable validation

### Input Validation
- Image file validation
- Content safety checks
- Token limit enforcement
- API response validation

## Future Enhancements

### Planned Features
- Result caching system
- Concurrent processing
- Batch processing capabilities
- Enhanced error recovery
- Performance benchmarking
- Comprehensive testing suite

### Integration Points
- API endpoint support
- Batch processing interface
- External service integration
- Enhanced reporting capabilities
