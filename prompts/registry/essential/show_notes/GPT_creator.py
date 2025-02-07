from . import chunker

SYSTEM_PROMPT = """You are a podcast show notes creator for the Crazy Wisdom AI podcast. Your task is to analyze podcast transcripts and create structured content for the podcast companion."""

CHUNK_PROMPT_TEMPLATE = """This is part {current_chunk} of {total_chunks} of a Crazy Wisdom episode transcript. Extract key insights and notable discussion points that could be relevant for show notes. Focus on:

1. Main topics discussed in this segment
2. Key insights or learnings
3. Notable quotes or examples
4. Any specific references or resources mentioned

Here's the transcript segment:

{transcript_text}"""

FINAL_PROMPT_TEMPLATE = """Create a podcast companion for this Crazy Wisdom episode using the extracted insights from the full transcript. Follow these exact requirements:

1. Name: Format must be "Crazy Wisdom Companion: [Guest's Full Name]"
2. Description: Maximum 300 characters, capture the essence of the conversation
3. Instructions: Simple list of what listeners will learn
4. Conversation Starters: 3-5 specific questions that reference the guest and actual content from the transcript

Use these extracted insights from the full episode:

{all_insights}"""

def create_final_messages(all_insights):
    """Create messages for final show notes compilation"""
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": FINAL_PROMPT_TEMPLATE.format(all_insights=all_insights)
        }
    ]

def extract_gpt_content(client, transcript_text, timestamps=None):
    """Extract GPT content using OpenAI API with chunking"""
    try:
        # Process chunks using the chunker
        chunk_insights = chunker.process_chunks(
            client,
            transcript_text,
            SYSTEM_PROMPT,
            CHUNK_PROMPT_TEMPLATE
        )
        
        if not chunk_insights:
            print("No insights were extracted from any chunks")
            return None
            
        # Combine insights into final show notes
        all_insights = "\n\n---\n\n".join(chunk_insights)
        
        # Generate final show notes
        print("Generating final show notes...")
        show_notes = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=create_final_messages(all_insights),
            temperature=0.7
        ).choices[0].message.content
        
        # Add timestamps if available
        if timestamps:
            show_notes = f"{show_notes}\n\n{timestamps}"
        
        return show_notes
        
    except Exception as e:
        print(f"Error extracting GPT content: {e}")
        return None