# Image Processing Flow for Stage 1

> **Flowchart Color Guide**:
> - 🟪 Pink boxes: File operations (loading, processing, conversion)
> - 🟦 Blue boxes: Decision points (format validation, provider selection)
> - 🟩 Green boxes: Actions (API calls, content generation)
> - 🟥 Red boxes: Error conditions and handling

```mermaid
%% Legend
%% Pink boxes: File operations
%% Blue boxes: Decision points
%% Green boxes: Actions
%% Red boxes: Errors

flowchart TD
    A[Start] --> B[Load Image]
    B --> C[Validate Image Format]
    
    C -->|Valid| D1[Convert to RGB]
    D1 --> D2[Check Size]
    D2 -->|Too Large| D3[Resize Image]
    D2 -->|Size OK| D4[Optimize Quality]
    D3 --> D4
    D4 --> D[Preprocessed Image]
    C -->|Invalid| E[Raise Error]
    
    D --> F[Convert to Provider Format]
    
    F --> G{Which Provider?}
    
    G -->|Gemini| H[Use PIL Image Directly]
    G -->|OpenAI| I[Convert to Base64]
    G -->|Anthropic| J[Convert to Base64]
    
    H --> K[Generate Content]
    I --> K
    J --> K
    
    K --> L[Return Transcription]
    
    subgraph Image Loading
        B
        C
    end
    
    subgraph Image Processing
        D1
        D2
        D3
        D4
        D
        F
    end
    
    subgraph Provider-Specific Handling
        G
        H
        I
        J
    end
    
    subgraph Transcription
        K
        L
    end

    %% File Relationships
    classDef file fill:#f9f,stroke:#333,stroke-width:2px;
    class B,D1,D2,D3,D4,D,F file;

    %% Decision Points
    classDef decision fill:#bbf,stroke:#333,stroke-width:2px;
    class C,G decision;

    %% Actions
    classDef action fill:#bfb,stroke:#333,stroke-width:2px;
    class H,I,J,K action;

    %% Errors
    classDef error fill:#fbb,stroke:#333,stroke-width:2px;
    class E error;
```

## Flow Description

1. **Image Loading**
   - Image is loaded using PIL.Image.open
   - Format validation checks for supported image types

2. **Image Processing**
   - Convert image to RGB format for consistency
   - Check image dimensions against size limits
   - Resize if image exceeds maximum dimensions
   - Optimize quality while maintaining size limits
   - Prepare for provider-specific format conversion

3. **Provider-Specific Handling**
   - Gemini: Uses PIL Image object directly
   - OpenAI: Converts to base64 with data URL
   - Anthropic: Converts to base64 with specific format

4. **Transcription**
   - Image is sent to provider with prompt
   - Transcription is returned as text

## Key Components

- `image_utils.py`: Handles image loading, validation, and conversion
- `model_factory.py`: Manages provider-specific implementations
- `model_manager.py`: Orchestrates the transcription process

## File Operations

1. `load_image()`: Loads image file and performs initial validation
2. `preprocess_image()`:
   - Converts to RGB format
   - Checks image dimensions
   - Resizes if necessary
   - Optimizes quality
3. `convert_to_base64()`: Converts processed image to base64 for OpenAI/Anthropic
4. `generate_content()`:
   - Formats image for specific provider
   - Sends to API with prompt
   - Handles retries if needed
   - Returns transcription text

## Error Handling

1. **Image Loading Errors**
   - Unsupported file formats
   - File not found or inaccessible
   - Corrupt image data

2. **Processing Errors**
   - Invalid color mode
   - Dimension validation failures
   - Memory constraints during resize
   - Quality optimization issues

3. **Provider-Specific Errors**
   - Base64 conversion failures
   - API connection timeouts
   - Rate limiting responses
   - Authentication failures

4. **Recovery Mechanisms**
   - Automatic retry with exponential backoff
   - Detailed error reporting
   - Graceful failure handling
   - Clear error messages for debugging
