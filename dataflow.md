# Chinese Family Tree Processing System Data Flow

## Model Independence

Each stage's models are completely independent and can be any provider/model:

### Parallel Processing Stages
- **Stage 1 (3 models)**:
  * Each model independently transcribes the image
  * No knowledge of other models' work
  * Can be any provider/model combination
  * Example: Model 1 (Gemini), Model 2 (GPT-4), Model 3 (Claude)

- **Stage 2 (3 models)**:
  * Each model independently transcribes the image
  * No knowledge of Stage 1 results
  * Can be any provider/model combination
  * Example: Model 1 (Claude), Model 2 (Gemini), Model 3 (GPT-4)

- **Stage 3 (3 models)**:
  * Each model reviews corresponding Stage 1/2 transcriptions:
    - Model 1 reviews Stage 1 Model 1 + Stage 2 Model 1
    - Model 2 reviews Stage 1 Model 2 + Stage 2 Model 2
    - Model 3 reviews Stage 1 Model 3 + Stage 2 Model 3
  * Can be different providers/models from Stage 1/2
  * Example: Model 1 (GPT-4), Model 2 (Claude), Model 3 (Gemini)

- **Stage 4 (3 models)**:
  * Each model reviews all Stage 3 analyses
  * Can be different providers/models from Stage 3
  * Makes independent recommendations
  * Example: Model 1 (Claude), Model 2 (GPT-4), Model 3 (Gemini)

### Sequential Processing Stages
- **Stage 5 (1 model)**:
  * Reviews all Stage 4 reviews and recommendations
  * Can be any provider/model
  * Independent from Stage 4 models
  * Example: Any model (Gemini, GPT-4, Claude, etc.)

- **Stage 6 (1 model)**:
  * Works only with Stage 5 transcript
  * Can be any provider/model
  * Independent from Stage 5 model
  * Example: Any model (different from Stage 5)

- **Stage 7 (1 model)**:
  * Works only with Stage 6 punctuated text
  * Can be any provider/model
  * Independent from Stage 6 model
  * Example: Any model (different from Stage 6)

- **Stage 8 (1 model)**:
  * Works with both Stage 6 Chinese text and Stage 7 translation
  * Can be any provider/model
  * Independent from Stage 6 and 7 models
  * Example: Any model (different from Stage 7)

## Available Models

### Vision + Language Models
These models can be used in any stage, but are required for Stages 1-2 (transcription):

- **OpenAI**:
  * gpt-4-turbo
  * gpt-4-vision-preview

- **Anthropic**:
  * claude-3-5-sonnet-20241022
  * claude-3-opus-20240229

- **Google**:
  * gemini-2.0-flash-exp
  * gemini-1.5-pro
  * gemini-exp-1206

- **Groq**:
  * llama-3.2-90b-vision-preview

### Language-Only Models
These models can be used in Stages 3-8 (review, translation, and commentary):

- **Google**:
  * gemini-pro

- **Groq**:
  * deepseek-r1-distill-llama-70b
  * mixtral-8x7b-32768
  * llama2-70b-4096
  * llama-3.3-70b-versatile

## Stage Details

### Stage 1 - Initial Transcription
- **Input**: 
  * Base64 encoded image
  * No dependencies on previous stages
- **Process**: 
  * 3 models independently transcribe the same image
  * Each model focuses on accurate character recognition and formatting
  * No knowledge of other models' transcriptions
- **Output**: 3 independent transcriptions stored as:
  * `Stage 1 Model 1 - {Provider1} {Model1} Transcription`
  * `Stage 1 Model 2 - {Provider2} {Model2} Transcription`
  * `Stage 1 Model 3 - {Provider3} {Model3} Transcription`
- **Output Format**:
  * Raw Chinese text without punctuation
  * Original formatting and line breaks preserved
  * No interpretive changes or annotations
  * Character-for-character transcription

### Stage 2 - Secondary Transcription
- **Input**: 
  * Same base64 encoded image as Stage 1
  * No dependencies on Stage 1 results
  * Fresh start for each model
- **Process**: 
  * 3 different models independently transcribe
  * Fresh attempt without knowledge of Stage 1 results
  * Focus on accuracy and detail
  * Special attention to similar-looking characters
- **Output**: 3 more independent transcriptions stored as:
  * `Stage 2 Model 1 - {Provider4} {Model4} Transcription`
  * `Stage 2 Model 2 - {Provider5} {Model5} Transcription`
  * `Stage 2 Model 3 - {Provider6} {Model6} Transcription`
- **Output Format**:
  * Raw Chinese text without punctuation
  * Original formatting and line breaks preserved
  * No interpretive changes or annotations
  * Character-for-character transcription

### Stage 3 - Initial Review
- **Input**: 
  * Each model looks at corresponding model number transcriptions:
    - Model 1: Stage 1 Model 1 + Stage 2 Model 1 transcriptions
    - Model 2: Stage 1 Model 2 + Stage 2 Model 2 transcriptions
    - Model 3: Stage 1 Model 3 + Stage 2 Model 3 transcriptions
  * Each model only analyzes transcriptions from its corresponding model number
- **Process**: 
  * Each model compares Stage 1 and Stage 2 transcriptions from same model number
  * Analyzes differences and similarities between attempts
  * Identifies potential errors and ambiguities
  * Makes recommendations for improvements
  * Suggests a final transcription based on reconciling differences
  * Provides confidence levels for different sections
  * Flags challenging characters or uncertain readings
- **Output**: 3 independent analyses stored as:
  * `Stage 3 Model 1 - {Provider7} {Model7} Review`
  * `Stage 3 Model 2 - {Provider8} {Model8} Review`
  * `Stage 3 Model 3 - {Provider9} {Model9} Review`
- **Output Format**:
  * Detailed analysis of differences between Stage 1 and 2
  * Specific recommendations for improvements
  * Suggested transcription based on reconciling differences
  * Justification for each change or decision
  * Confidence ratings for different sections
  * Notes on challenging characters or sections

### Stage 4 - Comprehensive Review
- **Input**: 
  * All Stage 3 reviews and analyses:
    - Stage 3 Model 1 Review (analysis + recommended transcription)
    - Stage 3 Model 2 Review (analysis + recommended transcription)
    - Stage 3 Model 3 Review (analysis + recommended transcription)
  * Full access to all Stage 3 analyses and recommendations
  * Each Stage 4 model sees all Stage 3 reviews
- **Process**: 
  * Each model reviews all Stage 3 analyses and recommendations
  * Compares different perspectives and suggested transcriptions
  * Analyzes patterns and consensus points across reviews
  * Evaluates justifications for different readings
  * Considers confidence levels reported by each model
  * Weighs competing interpretations of challenging sections
  * Develops own recommendation based on comprehensive analysis
  * Synthesizes insights from all Stage 3 analyses
- **Output**: 3 comprehensive reviews stored as:
  * `Stage 4 Model 1 - {Provider10} {Model10} Review`
  * `Stage 4 Model 2 - {Provider11} {Model11} Review`
  * `Stage 4 Model 3 - {Provider12} {Model12} Review`
- **Output Format**:
  * Analysis of all Stage 3 reviews and recommendations
  * Comparison of different suggested transcriptions
  * New recommended transcription with detailed justification
  * Discussion of areas of agreement and disagreement
  * Resolution of conflicting interpretations
  * Notes on remaining uncertainties or concerns
  * Confidence assessment for final recommendation

### Stage 5 - Final Independent Review and Transcription
- **Input**: 
  * All Stage 4 reviews, analyses, and recommended transcriptions:
    - Stage 4 Model 1 Review (analysis + recommended transcript)
    - Stage 4 Model 2 Review (analysis + recommended transcript)
    - Stage 4 Model 3 Review (analysis + recommended transcript)
  * Full access to each Stage 4 model's:
    - Comprehensive analysis
    - Recommended transcription
    - Justifications for choices
    - Confidence assessments
    - Notes on uncertainties
- **Process**: 
  * Independent model (can be any provider) reviews all Stage 4 input
  * Evaluates each Stage 4 model's recommendations independently
  * Considers justifications and evidence from each review
  * Forms own opinion about correct transcription
  * Makes independent decisions on disputed sections
  * Not bound by consensus of Stage 4 models
  * Ensures consistency throughout the text
  * Validates historical and cultural accuracy
  * Makes final judgment based on all available information
- **Output**: Final authoritative transcription stored as:
  * `Stage 5 Model 1 - {Provider13} {Model13} Final Transcription`
- **Output Format**:
  * Clean Chinese text without punctuation
  * Authoritative version based on independent judgment
  * No annotations or alternatives
  * Character-for-character final version
  * Result of independent evaluation, not just consensus

### Stage 6 - Independent Punctuation
- **Input**: 
  * Only the final unpunctuated transcription from Stage 5
  * No access to previous analyses or reviews
  * Clean text without annotations or alternatives
- **Process**: 
  * Independent model (can be any provider)
  * Works solely with the provided text
  * Makes punctuation decisions based on:
    - Classical Chinese grammar structures
    - Natural pause points
    - Logical grouping of ideas
    - Modern punctuation conventions
    - Text flow and readability
    - Semantic units and relationships
  * No influence from previous stages' analyses
  * Independent judgment based on text alone
- **Output**: Punctuated text stored as:
  * `Stage 6 Model 1 - {Provider14} {Model14} Punctuated Transcription`
- **Output Format**:
  * Chinese text with modern punctuation
  * Original text preserved exactly
  * Appropriate punctuation marks added
  * No other modifications to the text
  * Result of independent punctuation decisions

### Stage 7 - Independent Translation
- **Input**: 
  * Only the final punctuated Chinese text from Stage 6
  * No access to previous analyses, reviews, or transcription history
  * Clean text with modern Chinese punctuation
- **Process**: 
  * Independent model (can be any provider)
  * Works solely with the provided punctuated text
  * Makes translation decisions based on:
    - Classical Chinese grammar structures
    - Historical and cultural context
    - Idiomatic expressions
    - Proper names and titles
    - Semantic relationships indicated by punctuation
    - Text flow and readability
  * No influence from previous stages' analyses
  * Independent judgment based on text alone
- **Output**: English translation stored as:
  * `Stage 7 Model 1 - {Provider15} {Model15} Translation`
- **Output Format**:
  * Clear English translation
  * Proper handling of names and titles
  * Idiomatic expressions preserved
  * Cultural nuances maintained
  * Original meaning accurately conveyed
  * Result of independent translation decisions

### Stage 8 - Comprehensive Historical Commentary
- **Input**: 
  * Final punctuated Chinese text from Stage 6 (required)
  * Final English translation from Stage 7 (required)
  * Both texts must be present for commentary generation
  * No access to previous analyses, reviews, or transcription decisions
  * Parallel analysis of source and translated texts
- **Process**: 
  * Independent model (can be any provider)
  * Simultaneous analysis of Chinese and English versions
  * Cross-referential commentary generation:
    - Compares nuances between Chinese and English texts
    - Identifies cultural elements that may be lost in translation
    - Highlights linguistic features specific to Classical Chinese
    - Notes semantic shifts in the English rendering
  * Makes commentary decisions based on:
    - Historical context and significance
    - Cultural practices and beliefs
    - Family relationships and hierarchy
    - Notable historical figures or events
    - Social structures and customs
    - Traditional values and norms
    - Historical period context
    - Linguistic features preserved or adapted
    - Cultural concepts requiring additional explanation
  * Synthesizes insights from both language versions
  * No influence from previous stages' analyses
  * Independent judgment based on parallel text analysis
- **Output**: Historical commentary stored as:
  * `Stage 8 Model 1 - {Provider16} {Model16} Commentary`
- **Output Format**:
  * Detailed historical context
  * Cultural significance explained
  * Family relationships clarified
  * Notable references explained
  * Historical background provided
  * Cultural practices illuminated
  * Insights from both Chinese and English versions
  * Result of independent analysis

## Key Points

### Parallel vs Sequential Processing
- **Parallel Processing (Stages 1-4)**:
  * Stages 1-2: 3 models transcribe independently
  * Stage 3: Each model analyzes corresponding model number transcriptions
  * Stage 4: Each model reviews all Stage 3 analyses
  * Models work simultaneously within each stage
- **Sequential Processing (Stages 5-8)**:
  * Stage 5: Independent review of Stage 4 reviews → final transcript
  * Stage 6: Independent punctuation of Stage 5 transcript → punctuated text
  * Stage 7: Independent translation of Stage 6 text → English translation
  * Stage 8: Independent commentary using Stage 6 Chinese text and Stage 7 translation
  * Each stage works independently with only its required input

### Data Management
- Each stage validates required inputs before processing
- Context window maintains all stage outputs
- Token usage tracked throughout pipeline
- Base64 image data removed after transcription stages
- All intermediate outputs preserved for reference
- Each stage receives only the data it needs to operate
- No access to previous stages' analysis or decisions

### Error Handling
- Stage dependencies strictly enforced
- Empty or invalid outputs rejected
- Detailed error messages for missing data
- Token usage monitored to prevent overflows
- Input validation at each stage
