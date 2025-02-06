SYSTEM_PROMPT = """You are an assistant that extracts podcast guest names from transcripts. The guest name is usually mentioned in the first few lines when the host introduces them."""

USER_PROMPT_TEMPLATE = """Return ONLY the guest's full name with no additional text or explanation.
For example:
❌ "The guest's name is John Smith"
✅ "John Smith"

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