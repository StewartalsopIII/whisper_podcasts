import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from prompts.registry.essential.show_notes.timestamps import extract_timestamps

# Get absolute path to project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from prompts.registry.essential.guest_extraction import create_messages as create_guest_messages
from prompts.registry.essential.topic_extraction import create_messages as create_topic_messages
from prompts.registry.essential.show_notes import generate_show_notes
from prompts.registry.essential.show_notes.intro_paragraph import generate_intro_paragraph
from prompts.registry.essential.show_notes.keyword_extraction import create_messages as create_keyword_messages
from prompts.registry.essential.show_notes.title_suggestions import create_messages as create_title_messages

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

def save_episode_info(episode_folder, guest_name, topic, intro_paragraph=None, titles=None, keywords=None):
    """Save guest and topic information to a markdown file"""
    content = ["# Episode Information\n"]
    
    if intro_paragraph:
        content.append(intro_paragraph + "\n")
    
    content.extend([
        f"Guest: {guest_name}\n",
        f"Topic: {topic}\n"
    ])

    if keywords:
        content.append(f"\n## Keywords\n{keywords}\n")

    if titles:
        content.append("\n## Title Suggestions\n" + titles + "\n")
    
    info_file_path = Path(episode_folder) / "episode_info.md"
    info_file_path.write_text(
        "\n".join(content),
        encoding='utf-8'
    )
    return str(info_file_path)

def validate_extraction(guest_name=None, topic=None):
    """
    Check if extracted information is valid
    Returns tuple of (is_valid, error_message)
    """
    if guest_name is not None:
        if not guest_name or guest_name == "Unknown Guest":
            return False, "Guest name is empty or unknown"
    
    if topic is not None:
        # Check if topic is 2-5 words
        word_count = len(topic.split())
        if word_count < 2 or word_count > 5:
            return False, f"Topic must be 2-5 words (got {word_count} words)"
    
    return True, ""

def extract_guest_name(transcript_content):
    """Extract guest name using OpenAI API"""
    load_dotenv()
    
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        http_client=None
    )
    
    try:
        intro_text = clean_transcript_intro(transcript_content)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=create_guest_messages(intro_text)
        )
        
        guest_name = response.choices[0].message.content.strip()
        
        # Check for error messages or invalid responses
        if (not guest_name or 
            len(guest_name) > 50 or 
            "sorry" in guest_name.lower() or 
            "i apologize" in guest_name.lower() or
            "could not" in guest_name.lower() or
            "cannot" in guest_name.lower() or
            "don't see" in guest_name.lower() or
            "do not see" in guest_name.lower()):
            return None
            
        print("Guest identified:", guest_name)
        return guest_name
        
    except Exception as e:
        print("Error extracting guest name:", e)
        return None

def extract_topic(transcript_content):
    """Extract main topic using OpenAI API"""
    load_dotenv()
    
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        http_client=None
    )
    
    try:
        intro_text = clean_transcript_intro(transcript_content, max_chars=3000)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=create_topic_messages(intro_text)
        )
        
        topic = response.choices[0].message.content.strip()
        is_valid, error_msg = validate_extraction(topic=topic)
        
        if not is_valid:
            print(f"Warning: {error_msg}")
            return "General Discussion"
            
        print("Topic identified:", topic)
        return topic
        
    except Exception as e:
        print("Error extracting topic:", e)
        return "General Discussion"

def run_after_transcription(transcription_path):
    """Main function to process transcript and save episode information"""
    print(f"\nAnalyzing transcript: {transcription_path}")
    
    try:
        # Get transcript content
        transcript_content = read_transcript(transcription_path)
        
        # Get both guest name and topic
        guest_name = extract_guest_name(transcript_content)
        topic = extract_topic(transcript_content)
        
        print("Guest name extracted:", guest_name)
        print("Topic extracted:", topic)
        
        # Determine the name to use for the folder
        if guest_name and not any(phrase in guest_name.lower() for phrase in [
            "does not mention",
            "no guest",
            "cannot find",
            "could not find",
            "sorry",
            "apologize"
        ]):
            folder_name = guest_name
            metadata_guest = guest_name
        elif topic and 2 <= len(topic.split()) <= 5:
            folder_name = topic
            metadata_guest = "Unknown Speaker"
            print(f"Using topic as folder name: {topic}")
        else:
            folder_name = "Unknown Speaker"
            metadata_guest = "Unknown Speaker"
            topic = "General Discussion"
            
        # Generate intro paragraph
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        intro_paragraph, error = generate_intro_paragraph(client, transcript_content, metadata_guest)
        if error:
            print(f"Warning: {error}")
            intro_paragraph = None
        else:
            print("Successfully generated intro paragraph")
            
        # Save information with correct metadata
        episode_folder = get_episode_folder(transcription_path)
        info_file_path = save_episode_info(episode_folder, metadata_guest, topic, intro_paragraph)
        
        print(f"Episode information saved to: {info_file_path}")
        print(f"Folder will be named: {folder_name}")
        # Generate timestamps and show notes
        try:
            # First generate timestamps
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            timestamps = extract_timestamps(client, transcript_content)
            
            # Extract keywords and generate titles
            try:
                # Extract keywords
                keywords_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=create_keyword_messages(transcript_content[:3000], metadata_guest, topic)
                )
                keywords = keywords_response.choices[0].message.content.strip()
                print(f"Keywords extracted: {keywords}")

                # Validate keywords
                if keywords and "," in keywords:  # Ensure we got a comma-separated list
                    # Generate title suggestions
                    titles_response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=create_title_messages(metadata_guest, topic, keywords)
                    )
                    titles = titles_response.choices[0].message.content.strip()
                    if titles and titles.count("\n") >= 5:  # Basic validation that we got multiple titles
                        print("Title suggestions generated")
                    else:
                        print("Warning: Title generation produced unexpected format")
                        titles = None
                else:
                    print("Warning: Keyword extraction produced unexpected format")
                    titles = None
            except Exception as e:
                print(f"Error in title generation pipeline: {e}")
                titles = None

            # Update episode info with keywords and titles (if we have them)
            info_file_path = save_episode_info(episode_folder, metadata_guest, topic, intro_paragraph, titles, keywords)

            # Generate show notes
            show_notes_path = generate_show_notes(transcription_path, timestamps)
            if show_notes_path:
                print(f"Show notes generated at: {show_notes_path}")
        except Exception as e:
            print(f"Error generating show notes: {e}")
        
        return folder_name
        
    except Exception as e:
        print(f"Error processing transcript: {e}")
        return "Unknown Speaker"
    
if __name__ == "__main__":
    # Test with a sample path - adjust this path as needed
    sample_path = Path("output/test_episode/transcription.md")
    run_after_transcription(str(sample_path))