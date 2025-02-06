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