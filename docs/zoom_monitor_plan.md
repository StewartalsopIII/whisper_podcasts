# Zoom Recording Monitor Plan

## Overview
Plan to monitor Zoom recording folder, process .m4a files, and rename folders based on content extraction.

## Current Guest Extraction System
```python
SYSTEM_PROMPT = """You are an assistant that extracts podcast guest names from transcripts. The guest name is usually mentioned in the first few lines when the host introduces them."""

USER_PROMPT_TEMPLATE = """Extract the guest name from this Crazy Wisdom podcast transcript. Return only the guest's full name:

{transcript_text}"""
```

## Monitoring Flow
1. Monitor detects new Zoom folder creation
   - WD: /Users/stewartalsop/Dropbox/Crazy Wisdom/Beautifully Broken/Test for Transcription


2. Wait Period
   - 10 minutes delay to allow Zoom to complete .m4a file conversion

3. Processing
   - Transcribe .m4a using existing WhisperTranscriber
   - Run guest extraction using existing prompt
   - Extract folder naming components

4. Folder Renaming
   - Pattern: "Guest Name - Topic - YYYY-MM-DD"
   - Example: "John Smith - AI Ethics Discussion - 2025-02-04"

## Technical Components
1. Directory Monitor
   - Watch Zoom recordings folder
   - Detect new folder creation events
   - Implement 10-minute wait timer

2. Content Processing
   - Use existing WhisperTranscriber
   - Use existing guest_extraction.py
   - Extract guest name from transcript

3. Folder Management
   - Rename folder using extracted information
   - Maintain original date for reference
   - Handle any rename operation errors

## Required Modifications
1. Guest Extraction Prompt
   - Current: Only extracts guest name
   - Need: Expand to include topic/theme extraction
   - Keep same prompt structure

2. Naming Pattern
   - Format: "Guest Name - Topic - YYYY-MM-DD"
   - Components:
     - Guest Name: From guest_extraction.py
     - Topic: From expanded prompt
     - Date: From original folder name