# Chinese Family Tree Processing System Data Flow

[Previous content through Output File Structure section remains exactly as before]

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

[Rest of the content remains exactly as before]
