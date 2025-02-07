"""
Module for generating natural, Stewart-voiced introduction paragraphs for Crazy Wisdom podcast episodes.
Integrates with guest extraction and maintains consistent formatting and style.
"""

SYSTEM_PROMPT = """You are an expert at writing natural introductions for the Crazy Wisdom Podcast in Stewart Alsop's voice. You craft engaging, flowing introductions that maintain his conversational style.

Follow these key principles:
- Start with "On this episode of the Crazy Wisdom Podcast, I, Stewart Alsop,"
- Write in first-person as Stewart
- Maintain a natural, conversational flow
- Connect topics smoothly using transitional phrases
- End with clear, correctly formatted contact information"""

USER_PROMPT_TEMPLATE = """Create an introduction paragraph for this Crazy Wisdom Podcast episode in Stewart's voice. Use this exact information:

Guest Name: {guest_name}
Topics From Transcript: {topics}
Contact Information: {contact_info}

Follow this exact format:
1. Start with: "On this episode of the Crazy Wisdom Podcast, I, Stewart Alsop, sit down with {guest_name}..."
2. Include their key role/expertise
3. Flow naturally through the main topics
4. End with: "For more on {guest_first_name}'s work, check out [links]"

Example Style:
"On this episode of the Crazy Wisdom Podcast, I, Stewart Alsop, sit down with Brendon Wong, the founder of Unize.org. We explore Brendon's work in knowledge management, touching on his recent talk at Nodes 2024 about using AI to generate knowledge graphs and trends in the field. Our conversation covers the evolution of personal and organizational knowledge management, the future of object-oriented systems, the integration of AI with knowledge graphs, and the challenges of autonomous agents. For more on Brendon's work, check out unize.org and his articles at web10.ai."

Ensure the intro:
- Maintains natural flow between topics
- Uses active voice
- Formats contact links exactly as provided
- Keeps to 2-3 sentences for the main content
- Preserves technical accuracy"""

def create_messages(guest_name, topics, contact_info):
    """
    Create messages for the OpenAI chat completion.
    
    Args:
        guest_name (str): Full name of the guest (from guest_extraction)
        topics (str): Main topics discussed in the episode
        contact_info (str): Guest's contact/social links
        
    Returns:
        list: Messages formatted for OpenAI chat completion
    """
    # Get first name for contact section
    guest_first_name = guest_name.split()[0]
    
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(
                guest_name=guest_name,
                guest_first_name=guest_first_name,
                topics=topics,
                contact_info=contact_info
            )
        }
    ]