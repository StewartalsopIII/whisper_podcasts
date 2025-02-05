SYSTEM_PROMPT = """You are an assistant that extracts main topics from podcast transcripts. Focus on identifying the key themes and subjects discussed."""

USER_PROMPT_TEMPLATE = """Extract the main topics discussed in this Crazy Wisdom podcast transcript. Return a comma-separated list of the most important topics:

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