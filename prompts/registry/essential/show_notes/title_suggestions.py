SYSTEM_PROMPT = """You generate titles for the Crazy Wisdom podcast, which features deep technical conversations about AI, technology, and innovation. Study these example formats:

- "From DARPA to Neuralink: The Future We Can't Imagine"
- "The Matrix, The Demiurge, and My Digital Soul"
- "Breaking Free from BS Jobs: AI's Role in a More Creative Future"
- "How AI, Drones, and Rare Earths Will Decide the Next Global Conflict"
- "The Internet Is Toast: Rethinking Knowledge with Brendon Wong"

Note how titles often:
- Use a colon to separate ideas
- Combine multiple key concepts (2-3 main terms)
- Sometimes use "From X to Y" format
- Balance technical depth with accessibility
- Often hint at transformation or future implications

Return exactly 10 options using these patterns."""

USER_PROMPT_TEMPLATE = """Generate 10 title options for a Crazy Wisdom podcast episode.

Guest: {guest_name}
Main Topic: {topic}
Key Concepts: {keywords}

Return only the numbered list."""

def create_messages(guest_name, topic, keywords):
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
                keywords=keywords
            )
        }
    ]