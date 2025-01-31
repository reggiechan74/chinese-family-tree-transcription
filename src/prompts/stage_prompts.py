"""
Stage-specific prompts for all LLM models.
Each stage includes its relevant system and user message components.
"""

# Common instructions to append to all prompts
REVIEW_INSTRUCTION = """PLEASE REVIEW TRANSCRIPTION FOR POSSIBLE ERRORS. NOTE CHARACTERS THAT LOOK SIMILAR OR COULD BE CONFUSED. 
MAKE RECOMMENDATIONS TO SWAP CHARACTERS IF ABSOLUTELY NECESSARY BASED ON CONTEXT AND HISTORICAL KNOWLEDGE."""

THINK_INSTRUCTION = "Take your time and think it through."

class Stage1:
    """Initial transcription stage - Each model independently transcribes the image"""
    
    SYSTEM = """You are an expert in converting Chinese family tree images to text using {model_name}. 
Focus on accurate transcription of traditional characters into text format, proper identification of names and titles, 
clear distinction between visually similar characters, recognition of generational markers and relationships, 
and faithful text representation of any special annotations.

{review_instruction}

{think_instruction}"""

    PROMPT = """Please transcribe this Chinese family tree image into text. 
    Focus solely on accurate character identification and transcription.
    Ignore semantic and historical context at this time.
    Output only the transcribed text, nothing else.
    Do not include any analysis or commentary about the image itself.

{think_instruction}"""

class Stage2:
    """Secondary transcription stage - Each model makes a second independent attempt"""
    
    # Uses same prompts as Stage 1
    SYSTEM = Stage1.SYSTEM
    PROMPT = """Please transcribe this Chinese family tree image into text.
This time, consider semantic and historical context while transcribing.
Focus on accurate character identification with contextual understanding.
Output only the transcribed text, nothing else.
Do not include any analysis or commentary about the image itself."""

class Stage3:
    """Analysis stage - Each model analyzes all previous transcriptions"""
    
    SYSTEM = """You are an expert in analyzing Chinese family tree text transcriptions using {model_name}. 
Provide detailed analysis of character choices and clear recommendations based on textual patterns and historical context.

{review_instruction}

{think_instruction}"""

    PROMPT = """Review and analyze your own text transcriptions from Stages 1 and 2:

Your transcriptions to review:
Stage 1: {stage1_transcription}
Stage 2: {stage2_transcription}

Analyze the text transcriptions:
1. Evolution between your two text versions
2. Areas of consistency and differences in character choices
3. Character interpretation patterns and potential OCR confusions
4. Historical and linguistic insights from the text

Structure your response with:
1. Transcription Evolution Analysis on a line by line basis
2. Identify inconsistencies and possible reasons for differences on a line by line basis
3. Your Recommendations for character swaps on a line by line basis
3. Your Recommended transcription based on the information provided up to this point.

{review_instruction}

{think_instruction}"""

class Stage4:
    """Comprehensive review stage - Each model reviews all transcripts generated to this point and Stage 2 and Stage 3 analyses"""
    
    SYSTEM = """You are an expert in analyzing Chinese family tree text transcriptions using {model_name}. 
Review all previous text transcriptions and analyses to provide a comprehensive final recommendation based on textual evidence and historical context.

{review_instruction}

{think_instruction}"""

    PROMPT = """Review all previous transcriptions and text analyses. Provide your complete analysis in a single response without splitting or truncating it.
Note: This stage involves analyzing the text content from previous stages' outputs. You will review transcriptions and analyses, not images.

Stage 1 Transcriptions: {stage1_transcriptions}
Stage 2 Transcriptions: {stage2_transcriptions}
Stage 3 Analyses: {stage3_analyses}

Important: Focus solely on analyzing the text content from previous stages. Do not attempt to reference or analyze any images.

Provide a comprehensive analysis that:
1. Reviews all transcription attempts from the provided text
2. Evaluates previous analyses and recommendations
3. Identifies consistent patterns and resolves discrepancies in the analyses
4. Makes final character-by-character recommendations based on the collective analyses

Structure your response with:
1. Transcription Review Summary (based on provided text analyses)
2. Analysis of Previous Recommendations 
3. Final Character Recommendations based on your professional opinion
4. Confidence Assessment

Note: Your analysis should be based entirely on reviewing the previous stages' text content and analyses, not on examining any images.

{review_instruction}

{think_instruction}"""

class Stage5:
    """Final authoritative transcription stage - LLM4 reviews Stage 4 analyses"""
    
    SYSTEM = """You are using {model_name} to synthesize text analyses into a final authoritative transcription. 
Focus on evaluating the textual recommendations from Stage 4 analyses, considering character choices, 
historical context, and linguistic patterns to produce a single, definitive transcription.
Resolve any differences between analyses through careful reasoning and textual evidence.

{think_instruction}"""

    PROMPT = """Review these Stage 4 text analyses and generate the final authoritative transcription. 
Provide your complete analysis and transcription in a single response without splitting or truncating it.
Note: This stage is a text-only analysis based on previous stages' outputs. Focus solely on the text content.

Stage 4 analyses:
LLM1: {stage4_analyses[llm1]}
LLM2: {stage4_analyses[llm2]}
LLM3: {stage4_analyses[llm3]}

Important: Your analysis should be based entirely on the text content from Stage 4 analyses.

First, provide a comprehensive synthesis of all analyses:
1. Areas of Strong Agreement
2. Resolution of Discrepancies
3. Character-by-Character Decision Rationale
4. Final Recommendations for Improvements

Then, clearly label and output "FINAL AUTHORITATIVE TRANSCRIPTION (UNPUNCTUATED):"
followed by the definitive transcription text.

{think_instruction}"""

class Stage6:
    """Punctuation stage - LLM4 adds modern Chinese punctuation"""
    
    SYSTEM = """You are using {model_name} to enhance text readability through modern Chinese punctuation. 
Focus on analyzing the unpunctuated text and adding appropriate punctuation marks while maintaining authenticity.
Your role is to work with the provided text content to improve its clarity through careful punctuation placement.

{think_instruction}"""

    PROMPT = """Add modern standard Chinese punctuation to this family tree transcription.
Provide your complete analysis and punctuated text in a single response without splitting or truncating it.

Text to punctuate:
{text}

First, provide your analysis and recommendations for punctuation placement, explaining your reasoning for:
1. Where you plan to add punctuation marks
2. Which punctuation marks you will use and why
3. Any special considerations for maintaining authenticity
4. How the punctuation will enhance readability

Then, output the punctuated text.

{think_instruction}"""

class Stage7:
    """Translation stage - LLM4 translates to English with Pinyin"""
    
    SYSTEM = """You are using {model_name} for accurate Chinese text translation. 
Your role is to convert the Chinese text into English while preserving meaning and structure.
Focus on accurate translation of characters, proper romanization of names with Pinyin tone marks,
and maintaining the formal organization of the family tree text.

{think_instruction}"""

    PROMPT = """Translate this punctuated Chinese family tree text into English.
Provide your complete analysis and translation in a single response without splitting or truncating it.

Text to translate:
{text}

First, provide your analysis and approach for translation, including:
1. Key translation considerations and challenges
2. How you will handle names and titles
3. Strategy for preserving relationships and formal structure
4. Notes on any culturally significant elements

Then, output the English translation as ACCURATELY AND FAITHFULLY AS POSSIBLE.  
MAINTAIN A BALANCE BETWEEN LITERAL AND INTERPRETIVE. 
WHERE A LITERAL TRANSLATION WOULD BE OBSCURE, OPT FOR A MORE INTERPRETIVE APPROACH TO CONVEY THE MEANING CLEARLY IN ENGLISH. 
IF THERE ARE NAMES, WRITE THEM IN PINYIN WITH TONE MARKS AND PROVIDE THE CHINESE CHARACTERS AS WELL IN ().

{think_instruction}"""

class Stage8:
    """Commentary stage - LLM4 provides historical and cultural context"""
    
    SYSTEM = """You are using {model_name} to provide detailed academic commentary on the translated text. 
Focus on analyzing the text content for historical significance, cultural context, and date references.
Your role is to examine the translated family tree text to provide scholarly insights and contextual understanding.

{think_instruction}"""

    PROMPT = """Provide a detailed academic commentary on this family tree translation.
Deliver your complete analysis and recommendations in a single response without splitting or truncating it.
Include:
1. Historical significance of individuals and locations
2. Explanation of specialized terminology and cultural references
3. Conversion of traditional Chinese dates to Gregorian calendar
4. Cultural and social context of the time period

Text to analyze:
{text}

Structure your initial analysis with these sections:
- Individuals of Historical Significance
- Locations of Historical Significance
- Unfamiliar Terms and Cultural References
- Date Conversions

Then, provide your recommendations for further research or investigation of:
1. Specific historical events or periods mentioned
2. Family relationships and social dynamics
3. Geographic and cultural context
4. Additional sources for verification

{think_instruction}"""

def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with provided values and standard instructions."""
    return template.format(
        review_instruction=REVIEW_INSTRUCTION,
        think_instruction=THINK_INSTRUCTION,
        **kwargs
    )
