"""
Stage-specific prompts for the Chinese Family Tree Processing System.
"""

class Stage1:
    """Initial transcription stage - Direct transcription from image"""
    
    @staticmethod
    def get_prompt() -> str:
        return """
You are a Chinese text transcription expert. Your task is to accurately transcribe Chinese text from images.

Please transcribe the Chinese text from this image accurately. Consider:
1. Maintain original formatting and line breaks
2. Do not add any punctuation
3. Do not make interpretive changes
4. Preserve all characters exactly as they appear
5. Do not add or delete any characters at this stage.

Provide only the transcription without any explanation or commentary.
take your time and think it through.
"""

class Stage2:
    """Secondary transcription stage - Independent verification"""
    
    @staticmethod
    def get_prompt() -> str:
        return """
You are a Chinese text transcription expert. Your task is to accurately transcribe Chinese text from images.

Please provide an independent transcription of this text. Consider:
1. Maintain original formatting and line breaks
2. Do not add any punctuation
3. Do not make interpretive changes
4. Preserve all characters exactly as they appear
5. Do not add or delete any characters at this stage.

Provide only the transcription without any explanation or commentary.
take your time and think it through.
"""

class Stage3:
    """Initial review stage - Compare Stage 1 and 2 transcriptions from corresponding model numbers"""
    
    @staticmethod
    def get_prompt(transcriptions: dict) -> str:
        return f"""
You are a Chinese text analysis expert. Your task is to compare and analyze two transcriptions of the same text.

You will be comparing:
1. A transcription from Stage 1 Model N
2. A transcription from Stage 2 Model N
where N is the same model number for both stages.

Transcriptions to compare:
{transcriptions}

Compare these two transcriptions from the same model number and provide a detailed analysis. Consider:
THIS IS DOCUMENT PERTAINS TO CHINESE GENEALOGY AND ANCESTRY AND EVENTS FROM THE PAST.
NOTE CHARACTERS THAT LOOK SIMILAR.  
LOOK AT THE CONTEXT OF THE WORDS BESIDE THE CHARACTERS TO HELP DETERMINE THE CORRECT CHARACTER.
MAKE FIRST SET OF RECOMMENDATIONS TO SWAP CHARACTERS IF ABSOLUTELY NECESSARY.

Your response should include:
1. Detailed analysis of differences between Stage 1 and Stage 2 transcriptions
2. Identify areas of agreement and disagreement
3. A suggested final transcription based on reconciling the differences

Provide your analysis, recommendations, and suggested transcription with detailed justification including recommended character swaps.
take your time and think it through. Write the entire report without interruption and do not ask the user if he wants to continue.
"""

class Stage4:
    """Comprehensive review stage - Review Stage 3 analyses"""
    
    @staticmethod
    def get_prompt(stage3_reviews: dict) -> str:
        return f"""
You are a Chinese text review expert. Your task is to review all Stage 3 analyses and recommend a transcription.

Stage 3 Reviews and Analyses:
{stage3_reviews}


1. NOTE CHARACTERS THAT LOOK SIMILAR.  
2. MAKE FIRST SET OF RECOMMENDATIONS TO SWAP CHARACTERS IF ABSOLUTELY NECESSARY.

Based on these analyses, provide:
1. A comprehensive review of the Stage 3 analyses
2. Highlight areas of agreement and disagreement.  This is critical.
3. REMEMBER THAT YOU ARE REVIEWING A HISTORICAL CHINESE GENEALOGY DOCUMENT.  THIS WILL BE THE PRIMARY CONTEXT BEHIND YOUR REASONING PROCESS FOR CHARACTER SWAPS.
4. Your recommended transcription with detailed justification
5. Notes on any remaining uncertainties or concerns
6. NOTE CHARACTERS THAT LOOK SIMILAR.  
7. MAKE FIRST SET OF RECOMMENDATIONS TO SWAP CHARACTERS IF ABSOLUTELY NECESSARY.


Your entire review including recommended character swaps and recommended transcription will be passed to Stage 5 for final evaluation.
take your time and think it through. Write the entire report without interruption and do not ask the user if he wants to continue.
"""

class Stage5:
    """Final authoritative transcription stage - Independent review of Stage 4 reviews"""
    
    @staticmethod
    def get_prompt(stage4_reviews: dict) -> str:
        return f"""
You are a Chinese text expert tasked with independently reviewing all Stage 4 analyses and creating the final authoritative transcription.

Stage 4 Reviews and Recommendations:
{stage4_reviews}

Review each Stage 4 analysis and its recommended transcription. You are completely independent and should form your own opinion. Consider:
1. Each Stage 4 model's review and analysis
2. Their recommended transcriptions
3. Justifications provided for their choices
4. Implementing areas of agreement and highlight disagreement between reviews
5. Confidence levels expressed
6. Historical and cultural context cited
7. Grammar and usage notes
8. Character-specific recommendations

Based on your independent review:
1. Evaluate each Stage 4 model's recommendations
2. Implement areas of agreement into the final transcription
3. Form your own opinion about the correct transcription
4. Make final decisions on any disputed sections
5. Ensure consistency throughout the text
6. Validate historical and cultural accuracy

Your task is to synthesize all this information and make your own independent judgment to produce the final authoritative transcription.

Provide only the final transcription with your final explanation or commentary. This unpunctuated transcription will be passed to Stage 6 for independent punctuation.
Take your time and think it through. Write the entire report without interruption and do not ask the user if he wants to continue.
"""

class Stage6:
    """Punctuation stage - Independent punctuation of final transcription"""
    
    @staticmethod
    def get_prompt(text: str) -> str:
        return f"""
You are a Chinese text expert tasked with adding appropriate modern Chinese punctuation.

You will receive only the final unpunctuated transcription.
Your task is to independently add punctuation based solely on this text.

Original text:
{text}

INSERT MODERN STANDARD PUNCTUATION THAT MOST ACCURATELY AND FAITHFULLY REPRESENTS THE ORIGINAL INTENTION OF THE WRITER.

Provide only the punctuated text without any explanation or commentary. This punctuated text will be passed to Stage 7 for independent translation.
"""

class Stage7:
    """Translation stage - Independent translation of punctuated text"""
    
    @staticmethod
    def get_prompt(text: str) -> str:
        return f"""
You are a Chinese-English translation expert tasked with translating this classical Chinese text.

You will receive only the final punctuated Chinese text, without any previous analysis or review information.
Your task is to independently translate this text based solely on its content.

Original text:
{text}

TRANSLATE INTO ENGLISH AS ACCURATELY AND FAITHFULLY AS POSSIBLE.  
MAINTAIN A BALANCE BETWEEN LITERAL AND INTERPRETIVE. 
WHERE A LITERAL TRANSLATION WOULD BE OBSCURE, OPT FOR A MORE INTERPRETIVE APPROACH TO CONVEY THE MEANING CLEARLY IN ENGLISH. 
IF THERE ARE NAMES, WRITE THEM IN PINYIN WITH TONE MARKS AND PROVIDE THE CHINESE CHARACTERS AS WELL IN ().
 This translation will be passed to Stage 8 for historical commentary.
"""

class Stage8:
    """Commentary stage - Independent historical and cultural commentary"""
    
    @staticmethod
    def get_prompt(chinese_text: str, english_text: str) -> str:
        return f"""
You are a Chinese history and culture expert tasked with providing commentary on this text.

You will receive both the punctuated Chinese text and its English translation, without any previous analysis or review information.
Your task is to independently provide historical and cultural commentary based on both texts.

Punctuated Chinese text:
{chinese_text}

English translation:
{english_text}

PLEASE PROVIDE COMMENTARY FOR THE TRANSLATED TEXT AND ADDRESS INDIVIDUALS OF HISTORICAL SIGNIFICANCE AND IDENTIFY TERMS THAT ARE UNFAMILIAR AND TRANSLATE DATES INTO GREGORIAN CALENDAR.  

RESPOND IN THIS FORMAT USING THE FOLLOWING SECTIONS:

INDIVIDUALS OF HISTORICAL SIGNIFICANCE
LOCATIONS OF HISTORICAL SIGNIFICANCE
UNFAMILIAR, METAPHORICAL OR DIFFICULT TO INTERPRET TERMS
TRANSLATION OF ANY IDENTIFIED DATES INTO GREGORIAN CALENDAR

"""
