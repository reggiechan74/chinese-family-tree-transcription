# Chinese Family Tree Processing System Flow

# Model Provider Management

1. **Provider Configuration**
   - Provider-specific settings in `config.py`
     * API key management
     * Available models per provider
     * Vision capability tracking
     * Token limit handling (e.g., Claude-3 Opus 4096, Sonnet 8192)

2. **Provider Types**
   - Direct API Providers
     * OpenAI (GPT-4 Vision models)
     * Anthropic (Claude-3 models)
     * Google (Gemini models)
     * Groq (Llama models)
   - API Aggregators
     * OpenRouter
       - Meta Llama models
       - Deepseek models
       - Grok models
       - Custom headers and routing

3. **Model Capabilities**
   - Vision + Language Models
     * Used in Stages 1-2 (transcription)
     * Provider-specific implementations
     * Base64 image handling
   - Language-Only Models
     * Used in Stages 3-8
     * Text processing and analysis
     * Translation and commentary

[Previous content through Output Management section remains exactly as before]

5. **Token Management**
   - `token_costs.py`: Provider-specific cost rates
   - `token_counter.py`: Comprehensive token tracking
     * Per-model token counting
     * Stage-level aggregation
     * Provider-level metrics
     * Real-time usage display
   - Cost Calculation
     * Provider-specific rates
     * Input/output token differentiation
     * Aggregated cost analysis
   - Usage Monitoring
     * Context window limits
     * Rate limit tracking
     * Cost optimization

6. **Output Management**
   - Run Directory Organization
     * Timestamped directories: `run_YYYYMMDD_HHMMSS/`
     * Stage-specific output files
     * Summary and presentation reports
   - Stage Output Files
     * Two-part structure
       - Input data with token counts
       - Generated output with token counts
     * Processing time in minutes and seconds (Xm XX.XXs)
     * Token usage metrics
   - Summary Report
     * Stage-by-stage breakdown with model metrics
     * Provider/Model summary with subtotals
     * Time summaries in minutes and seconds
     * Token usage and cost analysis
     * Efficiency metrics (cost per 1K tokens)
   - Presentation Report
     * User-friendly format without technical metrics
     * Three clear sections:
       - Part 1: Chinese Text (punctuated)
       - Part 2: English Translation
       - Part 3: Historical Commentary
   - Error State Preservation
     * Partial results saved immediately
     * Token usage at failure point
     * Error context for debugging

[Rest of the content remains exactly as before]
