"""
Stage-specific prompts for the Chinese Family Tree Processing System.
"""
import os

def get_confirmed_facts() -> str:
    """Read and format confirmed facts from the file."""
    facts_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'confirmed_facts.md')
    with open(facts_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def get_facts_context() -> str:
    """Get confirmed facts formatted as context for prompts."""
    facts = get_confirmed_facts()
    return f"""
CONFIRMED FACTS TO CONSIDER:
{facts}

"""

class Stage1:
    """Initial transcription stage - Direct transcription from image"""
    
    @staticmethod
    def get_prompt() -> str:
        return get_facts_context() + """
You are a Chinese text transcription expert with vision capabilities, working on a genealogy research project. Your task is to use your vision capabilities to accurately transcribe Chinese text from the provided image of historical family records.

This is a safe and academic task focused on preserving historical family records. I am providing you with an image that contains traditional Chinese text from family genealogy documents. You must use your vision capabilities to read and transcribe this text.

Please transcribe the Chinese text from this image accurately. Consider:
1. This is historical genealogical content containing family records written in CLASSICAL CHINESE.
2. Maintain original formatting and line breaks.
3. Do not add any punctuation.
4. Do not make interpretive changes.
5. Preserve all characters exactly as they appear.
6. Do not add or delete any characters at this stage.
7. The transcription output must be in traditional Chinese characters.
8. Follow the formatting and line breaks of the original image as possible.
9. Pay VERY CLOSE attention to characters that look similar. If characters are difficult to discern, make a note of it for later stages. Note any instances where you are uncertain about a character due to visual ambiguity or image quality, and provide a confidence rating (1-10) for each character, with 10 being the most confident.
10. DO NOT add any text that is not clearly visible in the image. If a section is illegible, it is better to transcribe it as accurately as possible and note the uncertainty than to guess or fill in missing parts.
11. Generate three independent transcriptions of the text, paying special attention to difficult or ambiguous characters in each.

Provide only the transcription without any explanation or commentary.
Take your time, think it through.
"""

class Stage2:
    """Secondary transcription stage - Independent verification"""
    
    @staticmethod
    def get_prompt() -> str:
        return get_facts_context() + """
You are a Chinese text transcription expert with vision capabilities, working on a genealogy research project. Your task is to use your vision capabilities to accurately transcribe Chinese text from the provided image of historical family records.

This is a safe and academic task focused on preserving historical family records. I am providing you with an image that contains traditional Chinese text from family genealogy documents. You must use your vision capabilities to read and transcribe this text.

Please provide an independent transcription of this text. Consider:
1. This is historical genealogical content containing family records written in CLASSICAL CHINESE.
2. Maintain original formatting and line breaks.
3. Do not add any punctuation.
4. Do not make interpretive changes.
5. Preserve all characters exactly as they appear.
6. Do not add or delete any characters at this stage.
7. The transcription output must be in traditional Chinese characters.
8. Follow the formatting and line breaks of the original image as possible.
9. Pay VERY CLOSE attention to characters that look similar. If characters are difficult to discern, make a note of it for later stages. Note any instances where you are uncertain about a character due to visual ambiguity or image quality, and provide a confidence rating (1-10) for each character, with 10 being the most confident.
10. DO NOT add any text that is not clearly visible in the image. If a section is illegible, it is better to transcribe it as accurately as possible and note the uncertainty than to guess or fill in missing parts.
11. Generate three independent transcriptions of the text, paying special attention to difficult or ambiguous characters in each.

Provide only the transcription without any explanation or commentary.
Take your time, think it through.
"""

class Stage3:
    """Initial review stage - Compare Stage 1 and 2 transcriptions from corresponding model numbers"""
    
    @staticmethod
    def get_prompt(transcriptions: dict) -> str:
        return get_facts_context() + f"""
You are a Chinese text analysis expert. Your task is to compare and analyze two sets of transcriptions of the same text. Each set contains three independent transcriptions generated in the previous stage.

You will be comparing:
1. Transcriptions from Stage 1 Model N (three transcriptions)
2. Transcriptions from Stage 2 Model N (three transcriptions)
where N is the same model number for both stages.

Transcriptions to compare:
{transcriptions}

Compare these transcriptions from the same model number and provide a detailed analysis. Consider:
1. THIS DOCUMENT PERTAINS TO CHINESE GENEALOGY AND ANCESTRY AND EVENTS FROM THE PAST.
2. NOTE CHARACTERS THAT LOOK SIMILAR. Create a list of characters that are frequently confused due to visual similarity.
3. LOOK AT THE CONTEXT OF THE WORDS BESIDE THE CHARACTERS TO HELP DETERMINE THE CORRECT CHARACTER.
4. MAKE FIRST SET OF RECOMMENDATIONS TO SWAP CHARACTERS ONLY IF ABSOLUTELY NECESSARY, especially where the transcriptions within a set agree on a character that differs from the other set's consensus.
5. IDENTIFY CHARACTERS THAT WERE DIFFICULT TO TRANSCRIBE DUE TO IMAGE QUALITY AND WERE SUBJECT TO INTERPRETATION.
6. Pay special attention to characters with low confidence ratings provided in the previous stages.
7. Cross-reference the transcriptions within each set and between sets. If one transcription has a character that seems incorrect, check if other transcriptions have a different, potentially correct, character in the same position.
8. Remember this document is written in CLASSICAL CHINESE. Prioritize grammatical structures and vocabulary appropriate to that style.
9. IF THE MODELS AGREE ON TRANSCRIPTION, DO NOT SUGGEST CHARACTER SWAP AT THIS TIME.

Your response should include:
1. Detailed analysis of differences between the transcription sets, noting where transcriptions within a set agree or disagree.
2. Identify and clearly indicate for future models areas of agreement and disagreement between the two sets of transcriptions.
3. A suggested final transcription based on reconciling the differences and choosing the most likely correct characters based on context, frequency, and confidence ratings.
4. The final transcription must be in traditional Chinese characters.

Provide your analysis, recommendations, and suggested transcription with detailed justification including recommended character swaps. Use a chain-of-thought reasoning process, explaining each step of your analysis.
Take your time and think it through. Write the entire report without interruption and do not ask the user if he wants to continue.
"""

class Stage4:
    """Comprehensive review stage - Review Stage 3 analyses"""
    
    @staticmethod
    def get_prompt(stage3_reviews: dict) -> str:
        return get_facts_context() + f"""
You are a Chinese text review expert. Your task is to review all Stage 3 analyses and recommend a transcription.

Stage 3 Reviews and Analyses:
{stage3_reviews}

1. NOTE CHARACTERS THAT LOOK SIMILAR. Create a master list of frequently confused characters based on all Stage 3 analyses.
2. LOOK AT THE CONTEXT OF THE WORDS BESIDE THE CHARACTERS TO HELP DETERMINE THE CORRECT CHARACTER.
3. REMEMBER THAT YOU ARE REVIEWING A HISTORICAL CHINESE DOCUMENT WRITTEN IN CLASSICAL CHINESE. THIS WILL BE THE PRIMARY CONTEXT BEHIND YOUR REASONING PROCESS FOR CHARACTER SWAPS.
4. Actively engage with, critique, and build upon the Stage 3 analyses. Do not simply summarize them.
5. Weigh the evidence presented in each Stage 3 analysis and justify your preferred interpretation when disagreements arise.
6. Explicitly consult external, reliable sources (authoritative dictionaries of classical Chinese, historical databases, genealogical resources) to resolve ambiguities or verify information when needed.

Based on these analyses, provide:
1. A comprehensive review of the Stage 3 analyses, paying close attention to their chain-of-thought reasoning and justifications.
2. A dedicated section EXPLICITLY stating areas of agreement and disagreement between the Stage 3 analyses. This is CRITICAL.
3. Your recommended transcription with detailed justification, explaining why you chose certain characters over others, especially in cases of disagreement.
4. Notes on any remaining uncertainties or concerns, including a specific section for 'Remaining Uncertainties or Concerns.' List any phrases or characters that are still ambiguous or require further investigation, potentially through image verification.
5. NOTE CHARACTERS THAT LOOK SIMILAR.
6. MAKE second SET OF RECOMMENDATIONS TO SWAP CHARACTERS ONLY IF ABSOLUTELY NECESSARY AND CATEGORIZE YOUR REASONS FOR SWAPPING CHARACTERS AS FOLLOWS:
    A. Characters that were POSSIBLY MISTRANSCRIBED DUE TO POOR IMAGE RECOGNITION (and similar-looking characters)
    B. Characters that MUST BE SWAPPED due to NONSENSICAL GRAMMATICAL ERRORS.
    C. Characters that should be swapped due to CONTEXTUAL ERRORS within the document itself.
7. Provide extremely detailed justifications for EVERY character swap, explaining why the chosen character is more appropriate in terms of CLASSICAL CHINESE grammar, the context of a GENEALOGY document, and the surrounding text.

Your entire review including recommended character swaps and recommended transcription will be passed to Stage 5 for final evaluation.
Use a chain-of-thought reasoning process, explaining each step of your analysis and decision-making.
Take your time and think it through. Write the entire report without interruption and do not ask the user if he wants to continue.
"""

class Stage5:
    """Final authoritative transcription stage - Independent review of Stage 4 reviews"""
    
    @staticmethod
    def get_prompt(stage4_reviews: dict) -> str:
        return get_facts_context() + f"""
You are a Chinese text expert tasked with independently reviewing all Stage 4 analyses and creating the final authoritative transcription.

Stage 4 Reviews and Recommendations:
{stage4_reviews}

Review each Stage 4 analysis and its recommended transcription. You are completely independent and should form your own opinion. Consider:
1. Each Stage 4 model's review and analysis, paying particular attention to their justifications and chain-of-thought reasoning.
2. Their recommended transcriptions.
3. Justifications provided for their choices.
4. Implementing areas of agreement and highlight disagreement between reviews.
5. Confidence levels expressed by earlier stages, if available.
6. Historical and cultural context cited.
7. Grammar and usage notes, especially regarding classical Chinese.
8. Character-specific recommendations.
9. Consult external, reliable sources (authoritative dictionaries of classical Chinese, historical databases, genealogical resources) to resolve any remaining ambiguities or verify your choices.

Based on your independent review:
1. Evaluate each Stage 4 model's recommendations critically.
2. Implement areas of agreement into the final transcription.
3. Form your own opinion about the correct transcription, using your expertise in classical Chinese and genealogical documents.
4. Make final decisions on any disputed sections, providing a clear rationale for each decision based on evidence and your expert judgment.
5. Ensure consistency throughout the text.
6. Validate historical and cultural accuracy.
7. Ensure names have been correctly identified.
8. Your expertise in CLASSICAL CHINESE grammar, vocabulary, and style is paramount.

Your task is to synthesize all this information and make your own independent judgment to produce the final authoritative transcription.

Provide only the final transcription with your final explanation or commentary. This unpunctuated transcription will be passed to Stage 6 for independent punctuation.
Use a chain-of-thought reasoning process to document your decision-making, especially for any choices that deviate from the Stage 4 recommendations.
Take your time and think it through. Write the entire report without interruption and do not ask the user if he wants to continue.
"""

class Stage6:
    """Punctuation stage - Independent punctuation of final transcription"""
    
    @staticmethod
    def get_prompt(text: str) -> str:
        return get_facts_context() + f"""
You are a Chinese text expert tasked with adding appropriate modern Chinese punctuation to a classical Chinese text.

You will receive only the final unpunctuated transcription.
Your task is to independently add punctuation based solely on this text.

Original text:
{text}

INSERT MODERN STANDARD PUNCTUATION THAT MOST ACCURATELY AND FAITHFULLY REPRESENTS THE ORIGINAL INTENTION OF THE WRITER.

Consider these guidelines:
1. Use standard modern Chinese punctuation rules consistently.
2. Your goal is to make the text readable and understandable while remaining FAITHFUL to the original meaning and intent of the author.
3. While using modern punctuation, be mindful of the original sentence structure and phrasing of classical Chinese. Try to punctuate in a way that preserves the flow and rhythm of the original text as much as possible.
4. Consult authoritative guides on punctuating classical Chinese if needed.

Provide three versions of punctuated text for consideration.
This punctuated text will be passed to Stage 7 for independent translation.
Use a chain-of-thought reasoning process to explain your punctuation choices, especially in cases where the punctuation might be ambiguous.
"""

class Stage7:
    """Translation stage - Independent translation of punctuated text"""
    
    @staticmethod
    def get_prompt(text: str) -> str:
        return get_facts_context() + f"""
You are a Chinese-English translation expert tasked with translating this classical Chinese text.

You will receive only the final punctuated Chinese text, without any previous analysis or review information.
Your task is to independently translate this text based solely on its content.

Original text:
{text}

TRANSLATE INTO ENGLISH AS ACCURATELY AND FAITHFULLY AS POSSIBLE.
1. Keep in mind that this text was written in a formal, literary style of classical Chinese. Your English translation should reflect this formality to some extent.
2. Strive for a balance between a literal translation and an interpretive one. If a literal translation would be too obscure or awkward in English, opt for a slightly more interpretive approach to convey the meaning clearly. However, do not stray too far from the original wording.
3. For all names of people and places, write them in pinyin with tone marks and also provide the original Chinese characters in parentheses. This is crucial for accurate identification.
4. Consult authoritative Chinese-English dictionaries and resources on classical Chinese to ensure accuracy.
5. If a passage is particularly difficult or ambiguous, provide alternative translations or notes explaining the nuances.

First, provide three versions of the English translation. These translations will be passed to Stage 8 for independent historical commentary.
Then, based on the three translations, choose the most accurate and faithful translation as your final submission. 
You may select different sentences or phrases from each of the three translations to create the final version.
Use a chain-of-thought reasoning process to explain your translation choices, especially for difficult or ambiguous passages.
Take your time and think it through. Write the entire report without interruption and do not ask the user if he wants to continue.
"""

class Stage8:
    """Commentary stage - Independent historical and cultural commentary"""
    
    @staticmethod
    def get_prompt(chinese_text: str, english_text: str) -> str:
        return get_facts_context() + f"""
You are a Chinese history and culture expert tasked with providing commentary on this text.

You will receive both the punctuated Chinese text and its English translation, without any previous analysis or review information.
Your task is to independently provide historical and cultural commentary based on both texts.

Punctuated Chinese text:
{chinese_text}

English translation:
{english_text}

PLEASE PROVIDE COMMENTARY FOR THE TRANSLATED TEXT AND ADDRESS INDIVIDUALS OF HISTORICAL SIGNIFICANCE AND IDENTIFY TERMS THAT ARE UNFAMILIAR AND TRANSLATE DATES INTO GREGORIAN CALENDAR.

1. Assume your audience has a general understanding of Chinese history and culture but may not be familiar with the specifics of this particular genealogy or time period.
2. Use a clear and consistent format for your commentary, separating sections for individuals, locations, terms, and dates.
3. Consult external, reliable sources (historical databases, academic publications, genealogical records) to provide accurate and detailed information.

RESPOND IN THIS FORMAT USING THE FOLLOWING SECTIONS:

INDIVIDUALS OF HISTORICAL SIGNIFICANCE (Provide brief biographical information, their significance, and any relevant historical context)
LOCATIONS OF HISTORICAL SIGNIFICANCE (Describe the location, its historical context, and any relevant events or associations)
UNFAMILIAR, METAPHORICAL OR DIFFICULT TO INTERPRET TERMS (Explain the meaning of any terms that might be unfamiliar to a modern audience, including metaphorical language, classical Chinese idioms, or specialized genealogical terms)
TRANSLATION OF ANY IDENTIFIED DATES INTO GREGORIAN CALENDAR (Convert any dates mentioned in the text to the Gregorian calendar, providing both the original date format and the converted date)

Use a chain-of-thought reasoning process to explain your commentary and any inferences you make based on the text.
Take your time and think it through. Write the entire report without interruption and do not ask the user if he wants to continue.
"""
