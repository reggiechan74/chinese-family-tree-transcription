# Chinese Family Tree Processing System Specifications

[Previous content for System Overview, Technical Requirements, and Dependencies sections remains exactly the same]

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

[Rest of the content remains exactly the same]
