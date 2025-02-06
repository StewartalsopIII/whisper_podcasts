SYSTEM_PROMPT = """You are a podcast show notes creator for the Crazy Wisdom AI podcast. Your task is to analyze podcast transcripts and create structured content for the podcast companion."""

USER_PROMPT_TEMPLATE = """Create a podcast companion for this Crazy Wisdom episode transcript. Follow these exact requirements:

1. Name: Format must be "Crazy Wisdom Companion: [Guest's Full Name]"
2. Description: Maximum 300 characters, capture the essence of the conversation
3. Instructions: Simple list of what listeners will learn
4. Conversation Starters: 3-5 specific questions that reference the guest and actual content from the transcript

Here's the transcript:

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

def extract_gpt_content(client, transcript_text):
    """Extract GPT content using OpenAI API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=create_messages(transcript_text),
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error extracting GPT content: {e}")
        return None