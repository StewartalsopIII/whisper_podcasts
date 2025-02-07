"""
Module for generating natural, Stewart-voiced introduction paragraphs for Crazy Wisdom podcast episodes.
Integrates with guest extraction and maintains consistent formatting and style.
"""

import re
from typing import Optional, Tuple, List

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

def extract_contact_info(transcript_text: str) -> str:
    """
    Extract contact information and links from the transcript.
    Looks for common patterns like website URLs, social media handles, and email addresses.
    
    Args:
        transcript_text (str): The full transcript text
        
    Returns:
        str: Formatted contact information string
    """
    # Common patterns for contact info
    patterns = {
        'website': r'(?:check out|visit|at)\s+((?:https?://)?[\w\.-]+(?:\.[\w\.-]+)+\b)',
        'email': r'\b[\w\.-]+@[\w\.-]+\.\w+\b',
        'social': r'(?:@[\w\.-]+|(?:instagram|linkedin|twitter)\.com/[\w\.-]+)'
    }
    
    contact_info = []
    
    # Look for contact patterns in the last third of the transcript where they usually appear
    transcript_end = transcript_text[len(transcript_text)//3*2:]
    
    for pattern_type, pattern in patterns.items():
        matches = re.finditer(pattern, transcript_end, re.IGNORECASE)
        for match in matches:
            contact = match.group(1) if pattern_type == 'website' else match.group(0)
            if contact not in contact_info:
                contact_info.append(contact)
    
    return ', '.join(contact_info) if contact_info else ''

def extract_topics(transcript_text: str, max_length: int = 1000) -> str:
    """
    Extract main topics from the beginning of the transcript.
    
    Args:
        transcript_text (str): The full transcript text
        max_length (int): Maximum length of text to analyze
        
    Returns:
        str: Concatenated topics string
    """
    # Get the first portion of the transcript where topics are usually introduced
    intro_text = transcript_text[:max_length]
    
    # Remove timestamp lines and cleaning
    cleaned_lines = []
    for line in intro_text.split('\n'):
        if '-->' not in line and not line.strip().isdigit():
            cleaned_lines.append(line.strip())
    
    return ' '.join(cleaned_lines)

def create_messages(guest_name: str, topics: str, contact_info: str) -> List[dict]:
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

def generate_intro_paragraph(client, transcript_text: str, guest_name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generate an introduction paragraph for a Crazy Wisdom podcast episode.
    
    Args:
        client: OpenAI client instance
        transcript_text (str): Full episode transcript
        guest_name (str): Guest's name from guest_extraction
        
    Returns:
        Tuple[Optional[str], Optional[str]]: (intro_paragraph, error_message)
    """
    try:
        # Extract topics and contact information
        topics = extract_topics(transcript_text)
        contact_info = extract_contact_info(transcript_text)
        
        # If no contact info found, use a default format
        if not contact_info:
            print("Warning: No contact information found in transcript")
            contact_info = "their website"
        
        # Generate the introduction using our prompts
        messages = create_messages(guest_name, topics, contact_info)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        intro_paragraph = response.choices[0].message.content.strip()
        
        # Validate the generated intro
        if not intro_paragraph.startswith("On this episode"):
            print("Warning: Generated intro doesn't match expected format")
            return None, "Generated intro doesn't match expected format"
            
        return intro_paragraph, None
        
    except Exception as e:
        error_msg = f"Error generating intro paragraph: {str(e)}"
        print(error_msg)
        return None, error_msg