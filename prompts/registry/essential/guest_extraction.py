SYSTEM_PROMPT = """You are an assistant that extracts podcast guest names from transcripts. The guest name is usually mentioned in the first few lines when the host introduces them."""

USER_PROMPT_TEMPLATE = """Extract the guest name from this Crazy Wisdom podcast transcript. Return only the guest's full name:

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