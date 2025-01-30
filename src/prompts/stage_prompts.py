"""
Stage-specific prompts for all LLM models.
Each stage includes its relevant system and user message components.
"""

# Common instructions to append to all prompts
REVIEW_INSTRUCTION = """PLEASE REVIEW TRANSCRIPTION FOR POSSIBLE ERRORS AGAINST THE IMAGE. NOTE CHARACTERS THAT LOOK SIMILAR. 
MAKE RECOMMENDATIONS TO SWAP CHARACTERS IF ABSOLUTELY NECESSARY."""

THINK_INSTRUCTION = "Take your time and think it through."

class Stage1:
    """Initial transcription stage - Each model independently transcribes the image"""
    
    SYSTEM = """You are an expert in transcribing Chinese family trees using {model_name}. 
Focus on accurate transcription of traditional characters, proper identification of names and titles, 
clear distinction between similar-looking characters, recognition of generational markers and relationships, 
and preservation of special annotations. Output only the transcription text.

{review_instruction}

{think_instruction}"""

    PROMPT = """Please transcribe this Chinese family tree image. Output only the transcription text, nothing else.

{think_instruction}"""

class Stage2:
    """Secondary transcription stage - Each model makes a second independent attempt"""
    
    # Uses same prompts as Stage 1
    SYSTEM = Stage1.SYSTEM
    PROMPT = Stage1.PROMPT

class Stage3:
    """Analysis stage - Each model analyzes all previous transcriptions"""
    
    SYSTEM = """You are an expert in analyzing Chinese family tree transcriptions using {model_name}. 
Provide detailed analysis and clear recommendations based on the provided transcriptions.

{review_instruction}

{think_instruction}"""

    PROMPT = """Review and analyze your own transcriptions from Stages 1 and 2:

Your transcriptions to review:
Stage 1: {stage1_transcription}
Stage 2: {stage2_transcription}

Analyze:
1. Evolution between your two transcriptions
2. Areas of consistency and differences
3. Character interpretation patterns
4. Historical and linguistic insights

Structure your response with:
1. Transcription Evolution Analysis
2. Key Patterns Identified
3. Recommendations for Final Transcription

{review_instruction}

{think_instruction}"""

class Stage4:
    """Comprehensive review stage - Each model reviews all transcripts and Stage 3 analyses"""
    
    SYSTEM = """You are an expert in analyzing Chinese family tree transcriptions using {model_name}. 
Review all previous transcriptions and analyses to provide a comprehensive final recommendation.

{review_instruction}

{think_instruction}"""

    PROMPT = """Review all previous transcriptions and analyses:

Stage 1 Transcriptions: {stage1_transcriptions}
Stage 2 Transcriptions: {stage2_transcriptions}
Stage 3 Analyses: {stage3_analyses}

Provide a comprehensive analysis that:
1. Reviews all transcription attempts
2. Evaluates previous analyses and recommendations
3. Identifies consistent patterns and resolves discrepancies
4. Makes final character-by-character recommendations

Structure your response with:
1. Transcription Review Summary
2. Analysis of Previous Recommendations
3. Final Character Recommendations
4. Confidence Assessment

{review_instruction}

{think_instruction}"""

class Stage5:
    """Final authoritative transcription stage - LLM4 reviews Stage 4 analyses"""
    
    SYSTEM = """You are using {model_name} to generate the final authoritative transcription. 
Focus on synthesizing the key recommendations from Stage 4 analyses into a single, definitive transcription.
Consider areas of agreement between models and resolve any differences with careful reasoning.

{think_instruction}"""

    PROMPT = """Review these Stage 4 analyses and generate the final authoritative transcription.
Focus on areas of agreement and resolve any differences to produce the definitive version.

Stage 4 analyses:
LLM1: {stage4_analyses[llm1]}
LLM2: {stage4_analyses[llm2]}
LLM3: {stage4_analyses[llm3]}

Output only the final transcription text, with no additional commentary.

{think_instruction}"""

class Stage6:
    """Punctuation stage - LLM4 adds modern Chinese punctuation"""
    
    SYSTEM = """You are using {model_name} to add modern Chinese punctuation. 
Focus on enhancing readability while maintaining authenticity.

{think_instruction}"""

    PROMPT = """Add modern standard Chinese punctuation to this family tree transcription.
Follow proper Chinese punctuation conventions and ensure the punctuation enhances readability
while maintaining authenticity.

Text to punctuate:
{text}

Output only the punctuated text.

{think_instruction}"""

class Stage7:
    """Translation stage - LLM4 translates to English with Pinyin"""
    
    SYSTEM = """You are using {model_name} for accurate Chinese to English translation. 
Include Pinyin with tone marks for names and preserve the formal structure.

{think_instruction}"""

    PROMPT = """Translate this punctuated Chinese family tree text into English.
Include Pinyin with tone marks for names (with Chinese characters in parentheses).
Preserve the formal structure and relationships.

Text to translate:
{text}

Output only the English translation.

{think_instruction}"""

class Stage8:
    """Commentary stage - LLM4 provides historical and cultural context"""
    
    SYSTEM = """You are using {model_name} to provide detailed academic commentary. 
Focus on historical significance, cultural context, and accurate date conversions.

{think_instruction}"""

    PROMPT = """Provide a detailed academic commentary on this family tree translation.
Include:
1. Historical significance of individuals and locations
2. Explanation of specialized terminology and cultural references
3. Conversion of traditional Chinese dates to Gregorian calendar
4. Cultural and social context of the time period

Text to analyze:
{text}

Structure your response with these sections:
- Individuals of Historical Significance
- Locations of Historical Significance
- Unfamiliar Terms and Cultural References
- Date Conversions

{think_instruction}"""

def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with provided values and standard instructions."""
    return template.format(
        review_instruction=REVIEW_INSTRUCTION,
        think_instruction=THINK_INSTRUCTION,
        **kwargs
    )
