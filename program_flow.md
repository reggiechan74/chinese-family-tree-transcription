# Chinese Family Tree Processing System Flow

> **Flowchart Color Guide**:
> - 🟪 Pink boxes: File/Data operations
> - 🟦 Blue boxes: Decision points
> - 🟩 Green boxes: Processing stages
> - 🟥 Red boxes: Error handling

```mermaid
flowchart TD
    %% System Initialization
    A[Start] --> B[Parse Arguments]
    B --> C[Load Environment]
    C --> D[Initialize Token Tracker]
    D --> E[Load & Encode Image]
    
    %% Context Window Setup
    E --> F[Initialize Context Window]
    F --> G[Store Image in Context]
    
    %% Parallel Processing Stages
    G --> H[Stage 1: Initial Transcription]
    H --> H1{For each Model 1-3}
    H1 --> |Process Image| H2[Generate Transcription]
    H2 --> H3[Store in Context]
    H3 --> |Track Tokens| H4[Update Usage]
    H4 --> H1
    
    H1 --> |All Complete| I[Stage 2: Context-Aware]
    I --> I1{For each Model 1-3}
    I1 --> |With Context| I2[Generate Transcription]
    I2 --> I3[Store in Context]
    I3 --> |Track Tokens| I4[Update Usage]
    I4 --> I1
    
    I1 --> |All Complete| J[Stage 3: Self-Analysis]
    J --> J1{For each Model 1-3}
    J1 --> |Compare Own Results| J2[Analyze Differences]
    J2 --> J3[Store Analysis]
    J3 --> |Track Tokens| J4[Update Usage]
    J4 --> J1
    
    J1 --> |All Complete| K[Stage 4: Cross-Analysis]
    K --> K1{For each Model 1-3}
    K1 --> |Review All Data| K2[Comprehensive Review]
    K2 --> K3[Store Review]
    K3 --> |Track Tokens| K4[Update Usage]
    K4 --> K1
    
    %% Final Processing Stages
    K1 --> |All Complete| L[Remove Image from Context]
    L --> M[Stage 5: Final Version]
    M --> M1[Generate Authoritative Text]
    M1 --> |Track Tokens| M2[Update Usage]
    
    M2 --> N[Stage 6: Punctuation]
    N --> N1[Add Modern Punctuation]
    N1 --> |Track Tokens| N2[Update Usage]
    
    N2 --> O[Stage 7: Translation]
    O --> O1[English Translation]
    O1 --> O2[Add Pinyin]
    O2 --> |Track Tokens| O3[Update Usage]
    
    O3 --> P[Stage 8: Commentary]
    P --> P1[Historical Context]
    P1 --> P2[Cultural Analysis]
    P2 --> |Track Tokens| P3[Update Usage]
    
    %% Output Generation
    P3 --> Q[Generate Output Files]
    Q --> Q1[Final Results MD]
    Q --> Q2[Interim Analysis MD]
    Q --> Q3[Token Usage Report]
    
    %% Error Handling
    E --> |Error| R1[Image Error]
    F --> |Error| R2[Context Error]
    H2 --> |Error| R3[Provider Error]
    Q --> |Error| R4[Output Error]
    
    %% Recovery Paths
    R1 --> |Retry| E
    R2 --> |Reset| F
    R3 --> |Fallback| H1
    R4 --> |Retry| Q
    
    subgraph System Setup
        A
        B
        C
        D
        E
        F
        G
    end
    
    subgraph Parallel Processing
        H
        H1
        H2
        H3
        H4
        I
        I1
        I2
        I3
        I4
        J
        J1
        J2
        J3
        J4
        K
        K1
        K2
        K3
        K4
    end
    
    subgraph Final Stages
        L
        M
        M1
        M2
        N
        N1
        N2
        O
        O1
        O2
        O3
        P
        P1
        P2
        P3
    end
    
    subgraph Output
        Q
        Q1
        Q2
        Q3
    end
    
    subgraph Error Handling
        R1
        R2
        R3
        R4
    end

    %% Styling
    classDef setup fill:#e1d5e7,stroke:#9673a6;
    classDef parallel fill:#dae8fc,stroke:#6c8ebf;
    classDef final fill:#d5e8d4,stroke:#82b366;
    classDef output fill:#fff2cc,stroke:#d6b656;
    classDef error fill:#f8cecc,stroke:#b85450;
    classDef token fill:#ffe6cc,stroke:#d79b00;
    
    class A,B,C,D,E,F,G setup;
    class H,H1,H2,H3,H4,I,I1,I2,I3,I4,J,J1,J2,J3,J4,K,K1,K2,K3,K4 parallel;
    class L,M,M1,M2,N,N1,N2,O,O1,O2,O3,P,P1,P2,P3 final;
    class Q,Q1,Q2,Q3 output;
    class R1,R2,R3,R4 error;
    class H4,I4,J4,K4,M2,N2,O3,P3 token;
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
