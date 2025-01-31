# Chinese Family Tree Processing System Flow

> **Flowchart Color Guide**:
> - 🟪 Pink boxes: File/Data operations
> - 🟦 Blue boxes: Decision points
> - 🟩 Green boxes: Processing stages
> - 🟥 Red boxes: Error handling

```mermaid
flowchart TD
    A[Start] --> B[Load Image]
    B --> C[Initialize Models]
    
    C --> D[Stage 1: Initial Transcription]
    D --> D1{For each LLM}
    D1 --> |Process Image| D2[Convert to Base64]
    D2 --> D3[Generate Transcription]
    D3 --> D4[Store Result]
    D4 --> D1
    
    D1 --> |All Complete| E[Stage 2: Second Transcription]
    E --> E1{For each LLM}
    E1 --> |With Context| E2[Generate Transcription]
    E2 --> E3[Store Result]
    E3 --> E1
    
    E1 --> |All Complete| F[Stage 3: Analysis]
    F --> F1{For each LLM}
    F1 --> |Compare Own Results| F2[Analyze Differences]
    F2 --> F3[Make Recommendations]
    F3 --> F4[Store Analysis]
    F4 --> F1
    
    F1 --> |All Complete| G[Stage 4: Comprehensive Review]
    G --> G1{For each LLM}
    G1 --> |Review All Data| G2[Analyze All Results]
    G2 --> G3[Make Final Recommendations]
    G3 --> G4[Store Review]
    G4 --> G1
    
    G1 --> |All Complete| H[Stage 5: Final Transcription]
    H --> H1[LLM4 Reviews Stage 4]
    H1 --> H2[Generate Authoritative Version]
    
    H2 --> I[Stage 6: Add Punctuation]
    I --> I1[LLM4 Adds Modern Punctuation]
    
    I1 --> J[Stage 7: Translation]
    J --> J1[LLM4 Translates to English]
    J1 --> J2[Add Pinyin for Names]
    
    J2 --> K[Stage 8: Commentary]
    K --> K1[LLM4 Provides Context]
    K1 --> K2[Historical Analysis]
    
    K2 --> L[Final Output]
    
    %% Error Handling
    B --> |Error| M[Image Error]
    C --> |Error| N[Model Error]
    D2 --> |Error| O[Provider Error]
    
    subgraph Initial Processing
        B
        C
    end
    
    subgraph Multi-LLM Stages
        D
        D1
        D2
        D3
        D4
        E
        E1
        E2
        E3
        F
        F1
        F2
        F3
        F4
        G
        G1
        G2
        G3
        G4
    end
    
    subgraph Final Processing
        H
        H1
        H2
        I
        I1
        J
        J1
        J2
        K
        K1
        K2
        L
    end
    
    subgraph Error Handling
        M
        N
        O
    end

    %% File Operations
    classDef file fill:#f9f,stroke:#333,stroke-width:2px;
    class B,D4,E3,F4,G4,L file;

    %% Decision Points
    classDef decision fill:#bbf,stroke:#333,stroke-width:2px;
    class D1,E1,F1,G1 decision;

    %% Processing Stages
    classDef process fill:#bfb,stroke:#333,stroke-width:2px;
    class D,E,F,G,H,I,J,K process;

    %% Errors
    classDef error fill:#fbb,stroke:#333,stroke-width:2px;
    class M,N,O error;
```

## Program Flow Description

1. **Initial Processing**
   - Load and validate input image
   - Initialize LLM providers (Gemini, OpenAI, Anthropic)
   - Convert image to standardized Base64 format

2. **Multi-LLM Stages (1-4)**
   - Parallel Processing
     * Each stage runs LLMs concurrently
     * Results synchronized after each stage
     * All LLMs must complete before next stage

   - Stage 1: Initial Transcription
     * Each LLM independently transcribes the image
     * No semantic context considered
     * Results stored for comparison
   
   - Stage 2: Context-Aware Transcription
     * Each LLM performs second transcription
     * Considers semantic and historical context
     * Results stored alongside Stage 1
   
   - Stage 3: Self-Analysis
     * Each LLM compares their Stage 1 & 2 results
     * Analyzes differences and patterns
     * Makes character-specific recommendations
   
   - Stage 4: Comprehensive Review
     * Each LLM reviews all transcriptions
     * Analyzes all recommendations
     * Provides final character suggestions

3. **Final Processing (Stages 5-8)**
   - Stage 5: Authoritative Transcription
     * LLM4 reviews all Stage 4 analyses
     * Resolves any conflicts
     * Produces definitive transcription
   
   - Stage 6: Punctuation
     * LLM4 adds modern Chinese punctuation
     * Maintains authenticity
     * Enhances readability
   
   - Stage 7: Translation
     * LLM4 translates to English
     * Adds Pinyin for names
     * Preserves relationships
   
   - Stage 8: Historical Context
     * LLM4 provides academic commentary
     * Explains cultural significance
     * Converts dates to Gregorian calendar

4. **Error Handling & Recovery**
   - Error Types
     * Image processing errors (format, size, corruption)
     * Model initialization errors (API keys, configuration)
     * Provider-specific errors (rate limits, timeouts)
     * Network connection issues

   - Recovery Mechanisms
     * Automatic retries with exponential backoff
     * Provider failover options
     * Partial results preservation
     * Session recovery capability

   - Error Reporting
     * Detailed error messages
     * Stage-specific error context
     * Processing history logs
     * Token usage at failure

## Key Components

1. **Model Management**
   - `model_manager.py`: Orchestrates LLM interactions
   - `model_factory.py`: Creates provider instances
   - `model_interfaces.py`: Defines provider interfaces

2. **Image Processing**
   - `image_utils.py`: Handles image operations
   - Consistent Base64 conversion for all providers
   - Size and quality optimization
   - Standard format across LLMs

3. **Stage Processing**
   - `stage_prompts.py`: Defines stage-specific prompts
   - Stage-specific error handling
   - Result storage and management

4. **Configuration**
   - `config.py`: System configuration
   - Environment variables management
   - Provider-specific settings

5. **Token Management**
   - `token_costs.py`: Defines cost rates
   - Real-time token tracking
   - Usage reporting
   - Cost calculation

6. **Output Management**
   - Stores transcriptions by stage
   - Tracks token usage
   - Generates usage reports
   - Maintains processing history
