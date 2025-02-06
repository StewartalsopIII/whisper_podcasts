import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from .GPT_creator import extract_gpt_content

class ShowNotesCompiler:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def compile_show_notes(self, transcript_path):
        """
        Compile show notes from transcript
        Args:
            transcript_path: Path to the transcript file
        """
        # Read transcript
        transcript = Path(transcript_path).read_text(encoding='utf-8')
        
        # Generate GPT content
        gpt_content = extract_gpt_content(self.client, transcript)
        
        if not gpt_content:
            print("Failed to generate GPT content")
            return None
            
        # Create show notes file path
        output_dir = Path(transcript_path).parent
        show_notes_path = output_dir / "show_notes.md"
        
        # Write show notes
        show_notes_path.write_text(gpt_content, encoding='utf-8')
        
        print(f"Show notes generated at: {show_notes_path}")
        return str(show_notes_path)

def generate_show_notes(transcript_path):
    """Convenience function to generate show notes"""
    compiler = ShowNotesCompiler()
    return compiler.compile_show_notes(transcript_path)