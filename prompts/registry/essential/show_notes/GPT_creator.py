import re

CHUNK_SIZE = 6000  # Target size in characters for each chunk

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

def split_into_chunks(transcript_text):
    """Split transcript into chunks of approximately CHUNK_SIZE characters"""
    # Split by double newlines to preserve paragraph structure
    paragraphs = re.split(r'\n\s*\n', transcript_text)
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for paragraph in paragraphs:
        paragraph_size = len(paragraph)
        
        # If adding this paragraph would exceed chunk size and we already have content,
        # start a new chunk
        if current_size + paragraph_size > CHUNK_SIZE and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_size = 0
            
        current_chunk.append(paragraph)
        current_size += paragraph_size
    
    # Add any remaining content as the last chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def create_chunk_messages(transcript_chunk, chunk_index, total_chunks):
    """Create messages for processing a single chunk"""
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": CHUNK_PROMPT_TEMPLATE.format(
                current_chunk=chunk_index + 1,
                total_chunks=total_chunks,
                transcript_text=transcript_chunk
            )
        }
    ]

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

def process_chunk(client, chunk, chunk_index, total_chunks):
    """Process a single transcript chunk"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=create_chunk_messages(chunk, chunk_index, total_chunks),
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing chunk {chunk_index + 1}: {e}")
        return None

def extract_gpt_content(client, transcript_text):
    """Extract GPT content using OpenAI API with chunking"""
    try:
        # Split transcript into chunks
        chunks = split_into_chunks(transcript_text)
        print(f"Split transcript into {len(chunks)} chunks")
        
        # Process each chunk
        chunk_insights = []
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1}/{len(chunks)}...")
            insights = process_chunk(client, chunk, i, len(chunks))
            if insights:
                chunk_insights.append(insights)
        
        if not chunk_insights:
            print("No insights were extracted from any chunks")
            return None
            
        # Combine insights into final show notes
        all_insights = "\n\n---\n\n".join(chunk_insights)
        
        # Generate final show notes
        print("Generating final show notes...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=create_final_messages(all_insights),
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error extracting GPT content: {e}")
        return None