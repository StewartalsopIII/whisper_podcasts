SYSTEM_PROMPT = """You are an assistant that extracts the main topic from Crazy Wisdom podcast transcripts. Analyze the conversation to identify:
- The core theme or subject being discussed
- Key technical terms or concepts that appear repeatedly
- The central technology, methodology, or field of focus

Provide a concise topic (2-5 words) that accurately represents the main discussion."""

USER_PROMPT_TEMPLATE = """Extract the core topic from this Crazy Wisdom podcast transcript. Focus on the main subject, not subtopics. Return only a brief (2-5 words) description of what this episode is primarily about:

{transcript_text}"""

def create_messages(transcript_text):
    """Create messages for the OpenAI chat completion"""
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(transcript_text=transcript_text)
        }
    ]