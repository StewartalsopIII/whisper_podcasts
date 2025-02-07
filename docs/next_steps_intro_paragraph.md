# Next Steps: Implementing Intro Paragraph Generator

## Overview
The intro paragraph generator will create natural, engaging episode introductions that summarize the conversation and provide relevant links, following the style shown in existing examples.

## Implementation Plan

### 1. File Structure
```
prompts/registry/essential/show_notes/intro_paragraph.py
```

### 2. Core Components

#### a) Constants and Prompts
```python
SYSTEM_PROMPT = """You are an expert at crafting podcast introductions that sound natural and engaging. You write in Stewart Alsop's voice, avoiding typical AI writing patterns."""

USER_PROMPT_TEMPLATE = """Write an introduction paragraph for this podcast episode that:
1. Begins with "In this episode of the Crazy Wisdom Podcast"
2. Introduces Stewart Alsop and the guest
3. Summarizes key discussion topics
4. Ends with relevant links and contact information

Use this transcript: {transcript}

Write in a style that:
- Flows naturally
- Captures the conversation's essence
- Avoids formulaic AI writing patterns
- Maintains appropriate length (2-4 sentences for main content)"""
```

#### b) Core Functions

1. Main Generation Function:
```python
def generate_intro_paragraph(client, transcript_text):
    """
    Generates a natural introduction paragraph for the episode.
    
    Args:
        client: OpenAI client instance
        transcript_text: Full episode transcript
        
    Returns:
        str: Formatted introduction paragraph
    """
```

2. Link Extraction:
```python
def extract_contact_links(transcript_text):
    """
    Extracts and formats contact/social links mentioned in the episode.
    
    Args:
        transcript_text: Full episode transcript
        
    Returns:
        str: Formatted links section
    """
```

### 3. Integration Points

#### a) Post-Processing Integration
Update `post_transcription_processor.py`:
```python
from prompts.registry.essential.show_notes.intro_paragraph import generate_intro_paragraph

def process_transcript(transcript_path):
    # Existing code...
    
    # Generate intro paragraph
    intro = generate_intro_paragraph(client, transcript_text)
    
    # Add to episode_info.md
    with open(episode_info_path, 'a') as f:
        f.write("\n## Episode Introduction\n")
        f.write(intro)
```

#### b) Error Handling
- Handle missing transcripts
- Validate output format
- Ensure link extraction reliability

### 4. Testing Plan

1. Unit Tests:
- Test intro generation with sample transcripts
- Verify link extraction
- Check format consistency

2. Integration Tests:
- Full pipeline testing
- Output validation
- Style consistency checks

### 5. MVP Success Criteria
✓ Generates natural-sounding intros
✓ Includes all required components:
  - "In this episode..." opening
  - Guest introduction
  - Topic summary
  - Contact links
✓ Maintains consistent style with examples
✓ Integrates with existing pipeline

## Timeline
- Initial implementation: 1 day
- Testing and refinement: 1 day
- Integration: 1/2 day

## Next Actions
1. Create `intro_paragraph.py` with basic structure
2. Implement core generation function
3. Add link extraction
4. Update post-processing pipeline
5. Add tests
6. Test with sample transcripts

## Future Enhancements
- Topic clustering for better summary generation
- Guest expertise highlighting
- Dynamic length adjustment based on content
- Multiple style templates