import re
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class ChunkMetadata:
    index: int
    total_chunks: int

CHUNK_SIZE = 6000  # Default size in characters for each chunk

def split_into_chunks(transcript_text: str) -> List[str]:
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

def create_chunk_messages(transcript_chunk: str, chunk_index: int, total_chunks: int, 
                         system_prompt: str, chunk_prompt_template: str) -> List[Dict[str, str]]:
    """Create messages for processing a single chunk"""
    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": chunk_prompt_template.format(
                current_chunk=chunk_index + 1,
                total_chunks=total_chunks,
                transcript_text=transcript_chunk
            )
        }
    ]

def process_chunk(client, chunk: str, chunk_index: int, total_chunks: int, 
                 system_prompt: str, chunk_prompt_template: str) -> str:
    """Process a single transcript chunk"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=create_chunk_messages(chunk, chunk_index, total_chunks, 
                                        system_prompt, chunk_prompt_template),
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing chunk {chunk_index + 1}: {e}")
        return None

def process_chunks(client, transcript_text: str, system_prompt: str, 
                  chunk_prompt_template: str) -> List[str]:
    """Process all chunks of a transcript"""
    chunks = split_into_chunks(transcript_text)
    print(f"Split transcript into {len(chunks)} chunks")
    
    chunk_results = []
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        result = process_chunk(client, chunk, i, len(chunks), 
                             system_prompt, chunk_prompt_template)
        if result:
            chunk_results.append(result)
            
    return chunk_results