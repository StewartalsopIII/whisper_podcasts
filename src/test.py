import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

def clean_transcript_intro(transcript_content, max_chars=2000):
    """Clean and get introduction portion of transcript"""
    # Get first portion of transcript
    intro = transcript_content[:max_chars]
    
    # Remove timestamp lines and numbers
    cleaned_lines = []
    for line in intro.split('\n'):
        # Skip timestamp lines and standalone numbers
        if '-->' in line or line.strip().isdigit():
            continue
        cleaned_lines.append(line.strip())
    
    return ' '.join(cleaned_lines)

def read_transcript(file_path):
    """Read the transcript file content"""
    transcript_path = Path(file_path)
    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript file not found: {file_path}")
    return transcript_path.read_text(encoding='utf-8')

def get_episode_folder(transcription_path):
    """Get the episode folder from transcription path"""
    return Path(transcription_path).parent

def save_guest_info(episode_folder, guest_name):
    """Save guest information to a markdown file"""
    guest_file_path = Path(episode_folder) / "guest_info.md"
    guest_file_path.write_text(
        "# Episode Guest Information\n\n"
        f"Guest: {guest_name}\n",
        encoding='utf-8'
    )
    return str(guest_file_path)

def test_openai_api(transcript_content):
    """Process transcript with OpenAI to extract guest name"""
    load_dotenv()
    
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        http_client=None
    )
    
    try:
        # Clean and get introduction portion
        intro_text = clean_transcript_intro(transcript_content)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that extracts podcast guest names from transcripts. The guest name is usually mentioned in the first few lines when the host introduces them."
                },
                {
                    "role": "user", 
                    "content": f"Extract the guest name from this Crazy Wisdom podcast transcript. Return only the guest's full name:\n\n{intro_text}"
                }
            ]
        )
        
        guest_name = response.choices[0].message.content.strip()
        print("Guest identified!")
        print("Interview Guest:", guest_name)
        return guest_name
        
    except Exception as e:
        print("Error occurred:")
        print(e)
        return "Unknown Guest"

def run_after_transcription(transcription_path):
    """Main function to process transcript and save guest information"""
    print(f"\nAnalyzing transcript: {transcription_path}")
    
    try:
        # Get transcript content
        transcript_content = read_transcript(transcription_path)
        
        # Get guest name
        guest_name = test_openai_api(transcript_content)
        
        # Get episode folder and save guest info
        episode_folder = get_episode_folder(transcription_path)
        guest_file_path = save_guest_info(episode_folder, guest_name)
        
        print(f"Guest information saved to: {guest_file_path}")
        return guest_name
        
    except Exception as e:
        print(f"Error processing transcript: {e}")
        return None

if __name__ == "__main__":
    # Test with a sample path - adjust this path as needed
    sample_path = Path("output/test_episode/transcription.md")
    run_after_transcription(str(sample_path))