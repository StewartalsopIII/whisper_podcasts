SYSTEM_PROMPT = """Extract 20 key technical terms, concepts, or themes that are central to this Crazy Wisdom podcast conversation. Focus on:
- Specific technologies or methodologies discussed
- Core philosophical or theoretical concepts
- Novel frameworks or approaches mentioned
- Impactful trends or developments highlighted"""

USER_PROMPT_TEMPLATE = """Extract the most important technical terms and concepts from this conversation.

Guest: {guest_name}
Main Topic: {topic}
Transcript excerpt: {transcript_text}

Return only a comma-separated list of 20 key terms/concepts."""

def create_messages(transcript_text, guest_name, topic):
    """Create messages for the OpenAI chat completion"""
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(
                guest_name=guest_name,
                topic=topic,
                transcript_text=transcript_text
            )
        }
    ]