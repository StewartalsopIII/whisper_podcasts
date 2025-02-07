import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from .GPT_creator import extract_gpt_content
from .timestamps import extract_timestamps

class ShowNotesCompiler:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def compile_show_notes(self, transcript_path, timestamps=None):
        """
        Compile show notes from transcript
        Args:
            transcript_path: Path to the transcript file
            timestamps: Optional pre-generated timestamps
        """
        # Read transcript
        transcript = Path(transcript_path).read_text(encoding='utf-8')
        
        # Generate GPT content with timestamps if provided
        gpt_content = extract_gpt_content(self.client, transcript, timestamps)
        
        if not gpt_content:
            print("Failed to generate GPT content")
            return None
            
        # Set full content
        full_content = gpt_content
            
        # Create show notes file path
        output_dir = Path(transcript_path).parent
        show_notes_path = output_dir / "show_notes.md"
        
        # Write show notes
        show_notes_path.write_text(gpt_content, encoding='utf-8')
        
        print(f"Show notes generated at: {show_notes_path}")
        return str(show_notes_path)

def generate_show_notes(transcript_path, timestamps=None):
    """
    Convenience function to generate show notes
    Args:
        transcript_path: Path to the transcript file
        timestamps: Optional pre-generated timestamps
    """
    compiler = ShowNotesCompiler()
    return compiler.compile_show_notes(transcript_path, timestamps)