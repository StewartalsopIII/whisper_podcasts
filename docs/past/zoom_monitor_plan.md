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


# Zoom Recording Monitor Implementation
February 5, 2025 - 18:00

## Achievements from Zoom Monitor Plan
Successfully implemented part 1 and 2 of the monitoring flow:

1. ✓ Monitor detects new Zoom folder creation
   - Configured to watch: `/Users/stewartalsop/Dropbox/Crazy Wisdom/Beautifully Broken/Test for Transcription`
   - Successfully detects new folders as they're created

2. ✓ Wait Period
   - Implemented file size monitoring to ensure complete conversion
   - Automatically detects when M4A file is fully written
   - Successfully waits for the full conversion process

## Technical Implementation Details

### Key Components
1. File System Monitoring
   - Used `watchdog` library with `PollingObserver`
   - Chose polling over filesystem events for better reliability with Dropbox
   - Recursive monitoring to catch all nested file events

2. M4A Detection System
   - Tracks processed files to avoid duplicates
   - Ignores files in 'Audio Record' subfolder
   - Waits for file size to stabilize before declaring ready

### Challenges Solved
1. Dropbox Sync Issues
   - Switched to `PollingObserver` from default observer
   - Added retry mechanisms for file size checks
   - Handled temporary files during conversion

2. Duplicate Event Handling
   - Implemented file tracking with sets
   - Added logic to prevent duplicate processing
   - Filtered out irrelevant file modifications

3. File Conversion Detection
   - Added file size monitoring
   - Configurable check intervals and timeout
   - Progress tracking during conversion

### Code Structure
```python
class ZoomFolderHandler(FileSystemEventHandler):
    - Monitors base directory
    - Tracks processed files
    - Handles file move events
    - Processes M4A files

def _wait_for_file_ready():
    - Monitors file size changes
    - Confirms when conversion is complete
    - Shows progress during conversion
```

## Next Steps
1. Implement transcription processing for ready files
2. Add guest name extraction from transcripts
3. Implement folder renaming system
4. Add error handling and logging
5. Add configuration management

## Lessons Learned
1. Filesystem Events
   - Dropbox requires different handling than local files
   - Polling is more reliable than event-based monitoring
   - Need to handle both temporary and final files

2. File Processing
   - Must wait for files to be fully written
   - Size stabilization is a reliable indicator
   - Need to track processed files to avoid duplicates

3. Error Handling
   - Important to handle moved/renamed files
   - Need to manage duplicate events
   - Must account for network filesystem quirks


   Feb 6 2025 learnings from folder renaming system

# Folder Renaming System Implementation

This document details the implementation of the automatic folder renaming system for podcast episodes.

## Overview

The system automatically renames podcast episode folders based on guest information extracted from the episode_info.md file. The new naming pattern follows the format: `Guest Name - YYYY-MM-DD`.

## Components

### 1. PodcastFolderManager Class

Located in `src/folder_manager.py`, this class handles all folder renaming operations.

Key features:
- Tracks processed folders to prevent duplicate operations
- Extracts guest information from episode_info.md
- Safely renames folders with error handling
- Cleans names for filesystem compatibility

Core methods:
```python
rename_folder(folder_path)          # Main entry point for renaming
_extract_episode_info(folder_path)  # Extracts guest and topic information
_extract_date(folder_path)         # Gets date from folder name
_generate_folder_name(...)         # Creates new folder name
_clean_name(name)                  # Sanitizes names for filesystem
_perform_rename(old_path, new_name) # Handles actual renaming
```

### 2. Integration with ZoomFolderHandler

Modified `src/dropbox_monitor.py` to integrate folder renaming:
- Added PodcastFolderManager instance to ZoomFolderHandler
- Implemented check to prevent reprocessing of renamed folders
- Added folder renaming step after successful transcription

## Implementation Details

### File Structure Requirements

1. Episode folder must contain:
   - episode_info.md with guest information
   - Original date in folder name (YYYY-MM-DD format)

2. episode_info.md format:
   ```markdown
   Guest: [Guest Name]
   Topic: [Topic]
   ```

### Process Flow

1. System monitors for new recordings
2. After transcription completes:
   - Reads episode_info.md
   - Extracts guest name
   - Finds date in original folder name
   - Generates new name: "Guest - Date"
   - Performs safe rename operation

### Error Handling

The system includes robust error handling for:
- Missing episode_info.md
- Invalid or missing guest information
- Invalid folder names
- File system errors
- Duplicate processing prevention

### Prevention of Reprocessing

Two mechanisms prevent infinite loops:
1. PodcastFolderManager tracks processed folders
2. ZoomFolderHandler checks for already processed paths

## Future Improvements

Potential enhancements:
1. Additional error logging
2. Backup functionality before renaming
3. Configurable naming patterns
4. Support for additional metadata in folder names

## Testing

To test the system:
1. Create a folder with date in name
2. Add episode_info.md with guest information
3. System should automatically rename after transcription

## Git Changes

Implementation involved:
1. New file: src/folder_manager.py
2. Modified: src/dropbox_monitor.py
3. Committed with message: "feat: Add automatic folder renaming with PodcastFolderManager - implement Guest-Date pattern"