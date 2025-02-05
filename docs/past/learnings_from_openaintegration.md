# Prompt Registry System Design

[Previous content remains the same...]

## Technical Dependencies and Version Compatibility

### OpenAI Integration
- **Version Requirements**:
  - OpenAI package version 1.5.0 recommended
  - HTTPX version < 0.28.0 required (0.27.2 confirmed working)
  - Python 3.13 compatible

### Version Compatibility Notes
1. **Known Working Configurations**:
   - OpenAI 1.5.0 + HTTPX 0.27.2
   - Avoid HTTPX 0.28.0+ due to removal of 'proxies' argument

2. **Dependency Management**:
   - Use explicit version pinning in requirements.txt
   - Test dependency upgrades in isolation
   - Document working configurations

3. **Troubleshooting Common Issues**:
   - HTTPX proxy configuration conflicts
   - OpenAI client initialization errors
   - Version mismatch resolutions

4. **Upgrade Guidelines**:
   - Test OpenAI package upgrades with compatible HTTPX versions
   - Document any breaking changes
   - Maintain backup of working configurations

[Rest of the original content remains the same...]

# Prompt Registry Implementation Changes

This document outlines the changes made to implement the prompt registry structure for the Whisper Podcasts project.

## Directory Structure Changes

Created the following empty `__init__.py` files to establish the Python package structure:
```
/prompts/__init__.py
/prompts/registry/__init__.py
/prompts/registry/essential/__init__.py
```

## New Files Created

### /prompts/registry/essential/guest_extraction.py

Created with the following structure:
```python
SYSTEM_PROMPT = """You are an assistant that extracts podcast guest names from transcripts. The guest name is usually mentioned in the first few lines when the host introduces them."""

USER_PROMPT_TEMPLATE = """Extract the guest name from this Crazy Wisdom podcast transcript. Return only the guest's full name:

{transcript_text}"""

def create_messages(transcript_text):
    """Create messages for the OpenAI chat completion"""
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": USER_PROMPT_TEMPLATE.format(transcript_text=transcript_text)
        }
    ]
```

## Modified Files

### src/test.py

Added import path resolution and switched to using the prompt registry:
```python
import sys
import os

# Get absolute path to project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from prompts.registry.essential.guest_extraction import create_messages
```

Replaced hardcoded OpenAI messages with the imported prompt:
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=create_messages(intro_text)
)
```

## Path Resolution Approaches

Several approaches were tested for resolving the Python import path:

1. Using relative imports (e.g., `from ...prompts`) - Did not work reliably
2. Using simple relative path addition (`sys.path.append("..")`) - Too brittle
3. Setting PYTHONPATH in .env file - Works but not necessary with final solution

## Final Working Solution

The final solution uses absolute path resolution in test.py to ensure Python can find the prompts package from anywhere in the project. This approach:
- Is more robust than environment variables
- Works regardless of where the script is run from
- Doesn't require system-level configuration