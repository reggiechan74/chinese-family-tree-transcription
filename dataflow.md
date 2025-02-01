# Chinese Family Tree Processing System Data Flow

## Stage-by-Stage Data Flow

### Stage 1: Initial Transcription
- **Input**
  * Raw image file
  * Base64 encoded image data
  * Vision model prompts
- **Processing**
  * Three parallel vision models process image
  * Each model generates independent transcription
  * Token usage tracked per model
- **Output**
  * Three independent Chinese text transcriptions
  * Token usage metrics for each model
  * Processing time and status

### Stage 2: Secondary Transcription
- **Input**
  * Raw image file (same as Stage 1)
  * Base64 encoded image data
  * Stage 1 transcriptions (for context)
  * Vision model prompts
- **Processing**
  * Three parallel vision models process image
  * Each model generates new transcription
  * Compare with Stage 1 results
- **Output**
  * Three new Chinese text transcriptions
  * Comparison notes with Stage 1
  * Token usage metrics

### Stage 3: Analysis
- **Input**
  * Stage 1 transcriptions
  * Stage 2 transcriptions
  * Analysis prompts
- **Processing**
  * Each model analyzes its own Stage 1 & 2 results
  * Identify discrepancies and patterns
  * Generate recommendations
- **Output**
  * Analysis reports
  * Discrepancy lists
  * Recommended corrections
  * Token usage metrics

### Stage 4: Review
- **Input**
  * All Stage 3 analyses
  * Original transcriptions
  * Review prompts
- **Processing**
  * Cross-model analysis
  * Consensus building
  * Final recommendations
- **Output**
  * Comprehensive review reports
  * Consensus recommendations
  * Final transcription suggestions
  * Token usage metrics

### Stage 5: Final Transcription
- **Input**
  * Stage 4 review reports
  * Consensus recommendations
  * Transcription prompts
- **Processing**
  * Synthesize all previous analyses
  * Apply consensus corrections
  * Generate authoritative version
- **Output**
  * Final Chinese transcription
  * Confidence metrics
  * Token usage metrics

### Stage 6: Punctuation
- **Input**
  * Final transcription from Stage 5
  * Punctuation prompts
- **Processing**
  * Analyze text structure
  * Add appropriate punctuation
  * Enhance readability
- **Output**
  * Punctuated Chinese text
  * Formatting notes
  * Token usage metrics

### Stage 7: Translation
- **Input**
  * Punctuated Chinese text
  * Translation prompts
- **Processing**
  * Translate to English
  * Add Pinyin annotations
  * Preserve formatting
- **Output**
  * English translation
  * Pinyin annotations
  * Translation notes
  * Token usage metrics

### Stage 8: Commentary
- **Input**
  * Chinese text
  * English translation
  * Commentary prompts
- **Processing**
  * Historical analysis
  * Cultural context
  * Genealogical insights
- **Output**
  * Historical commentary
  * Cultural notes
  * Genealogical context
  * Token usage metrics

## Final Output Aggregation
- **Input**
  * All stage outputs
  * Token usage data
  * Processing metrics
- **Processing**
  * Compile all results
  * Generate summaries
  * Calculate metrics
- **Output**
  * Complete transcription package
  * Summary report
  * Token usage report
  * Performance metrics

## Output File Structure

### Stage Output Format
```markdown
# Stage N Output
Generated: YYYY-MM-DD HH:MM:SS
Processing Time: Xm XX.XXs
Total Token Count: X,XXX tokens
Total Cost: $X.XXXX

## Input from Previous Stage
[For Stage 1: "No input from previous stage"]
[For other stages, list each input with token count:]
### Input Name
Token count: X,XXX tokens
```content```

## Generated Output
[List each output with token count:]
### Output Name
Token count: X,XXX tokens
```content```

Total tokens being passed to next stage: X,XXX tokens
```

### Presentation Report Format
```markdown
# Chinese Family Tree Analysis

## Part 1: Chinese Text
[Punctuated Chinese text]

## Part 2: English Translation
[English translation with Pinyin annotations]

## Part 3: Historical Commentary
[Historical and cultural analysis]
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
