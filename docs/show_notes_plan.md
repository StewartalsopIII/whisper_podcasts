# Show Notes Automation Plan

## Overview
This document outlines the strategy for automating comprehensive show notes generation for Crazy Wisdom podcast episodes using a series of specialized prompts and a central compilation system.

## Component Structure

### 1. Show Notes Registry
```
prompts/registry/essential/show_notes/
├── __init__.py
├── components/
│   ├── GPT_creator.py        # Episode name, description, conversation starters
│   ├── timestamps.py            # 5-minute interval content markers
│   ├── intro_paragraph.py       # Stewart's intro with guest links
│   ├── title_suggestions.py     # Title options based on conversation style
│   ├── keywords.py              # Episode keywords
│   ├── key_insights.py          # Main takeaways in paragraph form
│   ├── guest_blurb.py           # Guest perspective summary
│   └── contact_info.py          # Guest contact information
└── compiler.py                  # Show notes assembly system
```

## Component Details

### GPT Creator (`GPT_creator.py`)
- **Input**: Full transcript
- **Output**: 
  - Name (format: "Crazy Wisdom Companion: [Guest Name]")
  - Description (max 300 chars)
  - Instructions
  - Conversation starters (guest-specific)
- **Special Handling**: Ensures conversation starters reference transcript content

### Timestamps (`timestamps.py`)
- **Input**: Full transcript
- **Output**: 5-minute interval markers with discussion topics
- **Format**: 
  - HH:MM:SS for 60+ minute episodes
  - MM:SS for shorter episodes
- **Exclusions**: Skips intro/outro sections

### Intro Paragraph (`intro_paragraph.py`)
- **Input**: Full transcript
- **Output**: Single paragraph with:
  - Stewart Alsop introduction
  - Guest's full name
  - Show notes links
- **Style**: Avoids generic AI writing patterns

### Title Suggestions (`title_suggestions.py`)
- **Input**: Full transcript
- **Output**: 10 creative titles
- **Analysis**: Focuses on Stewart's conversation style
- **Goal**: Capture authentic podcast voice

### Keywords (`keywords.py`)
- **Input**: Full transcript
- **Output**: Comma-separated keyword list in sentence form
- **Focus**: Key topics and concepts

### Key Insights (`key_insights.py`)
- **Input**: Full transcript
- **Output**: 7 key insights in paragraph form
- **Format**: Numbered list with full explanations

### Guest Blurb (`guest_blurb.py`)
- **Input**: Full transcript
- **Output**: 2-3 sentence episode summary
- **Style**: Written from guest's perspective

### Contact Info (`contact_info.py`)
- **Input**: Full transcript
- **Output**: Contact details shared during conversation
- **Focus**: End-of-episode mentions

## Compilation System

### Show Notes Compiler
- **Purpose**: Orchestrate prompt execution and combine outputs
- **Features**:
  1. Sequential prompt execution
  2. Error handling for each component
  3. Consistent formatting
  4. Final assembly in markdown format

### Implementation Steps

1. **Phase 1: Core Components**
   - Implement basic prompt structure
   - Create compiler framework
   - Test with sample transcripts

2. **Phase 2: Refinement**
   - Fine-tune prompts based on results
   - Add error handling
   - Implement retry logic for failed components

3. **Phase 3: Integration**
   - Connect with existing transcription system
   - Add configuration options
   - Create logging system

## Usage Flow
1. Transcription completes
2. Show notes generation triggered
3. Prompts execute sequentially
4. Results compiled into final document
5. Output saved in episode folder

## Next Steps
1. Create base prompt structure
2. Implement 2-3 components for testing
3. Build basic compiler
4. Test with sample transcripts
5. Iterate based on results
