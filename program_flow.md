# Chinese Family Tree Processing System Flow

1. **Model Provider Management**
   - Provider Configuration
     * API key management in .env
     * Model capability tracking
     * Token limit handling
       - Claude-3 Opus: 4096 tokens
       - Claude-3 Sonnet: 8192 tokens
       - Other models: Provider limits

   - Provider Types
     * Direct API Providers
       - OpenAI (GPT-4 Vision models)
       - Anthropic (Claude-3 models)
       - Google (Gemini models)
       - Groq (Llama models)
     * API Aggregators
       - OpenRouter
         * Meta Llama models
         * Deepseek models
         * Grok models
         * Custom headers and routing

   - Model Capabilities
     * Vision + Language Models
       - Used in Stages 1-2 (transcription)
       - Provider-specific implementations
       - Base64 image handling
     * Language-Only Models
       - Used in Stages 3-8
       - Text processing and analysis
       - Translation and commentary

2. **Model Factory System**
   - Stage-specific Model Creation
     * Model capability validation
     * Provider-specific initialization
     * Token limit configuration

   - Client Management
     * Provider-specific API clients
     * Authentication handling
     * Error recovery

3. **Processing Pipeline**
   - Stage 1: Initial Transcription
     * Parallel processing with 3 models
     * Vision model handling
     * Base64 image encoding

   - Stage 2: Secondary Transcription
     * Alternative perspectives
     * Cross-validation
     * Error detection

   - Stage 3: Analysis
     * Transcription comparison
     * Discrepancy identification
     * Recommendation generation

   - Stage 4: Review
     * Comprehensive analysis
     * Consensus building
     * Final recommendations

   - Stage 5: Final Transcription
     * Authoritative version
     * Error correction
     * Quality assurance

   - Stage 6: Punctuation
     * Modern Chinese punctuation
     * Readability enhancement
     * Format standardization

   - Stage 7: Translation
     * English translation
     * Pinyin annotation
     * Cultural context

   - Stage 8: Commentary
     * Historical analysis
     * Cultural insights
     * Genealogical context

4. **Token Management**
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

5. **Output Management**
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
