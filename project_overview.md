# Podcast Auto-Transcription System

## Project Overview
This project implements an automated system that monitors a designated podcast directory for new audio files (M4A format) and automatically transcribes them using OpenAI's Whisper API. The system utilizes Python's Watchdog library for file system monitoring and OpenAI's API for high-quality audio transcription.

## Core Features
1. **File System Monitoring**
   - Continuous monitoring of the `podcasts` directory
   - Detection of new M4A file uploads
   - Event-based processing trigger

2. **Audio Processing**
   - Automatic detection of M4A files
   - File validation and preprocessing
   - Integration with OpenAI Whisper API

3. **Transcription Pipeline**
   - Automated transcription of detected audio files
   - Output of transcribed text in structured format
   - Error handling and retry mechanisms

## System Architecture

### Directory Structure
```
project_root/
├── podcasts/           # Monitored directory for audio files
├── src/               
│   ├── monitor.py     # File system monitoring implementation
│   ├── transcriber.py # OpenAI Whisper API integration
│   └── utils.py       # Utility functions
├── output/            # Transcription output directory
└── config/            # Configuration files
```

### Components

1. **File Monitor (Watchdog)**
   - Implements real-time directory monitoring
   - Filters for M4A files
   - Triggers processing pipeline on file creation

2. **Transcription Service**
   - Handles OpenAI API authentication
   - Manages file upload and transcription requests
   - Processes API responses

3. **Output Handler**
   - Manages transcription output
   - Implements file naming conventions
   - Handles storage of transcribed text

## Implementation Plan

### Phase 1: Basic Setup
- [x] Create project structure
- [ ] Set up Watchdog file monitoring
- [ ] Implement basic M4A file detection

### Phase 2: OpenAI Integration
- [ ] Set up OpenAI API authentication
- [ ] Implement basic transcription functionality
- [ ] Add error handling

### Phase 3: Enhancement
- [ ] Add configuration management
- [ ] Implement logging
- [ ] Add progress tracking
- [ ] Implement retry mechanism

## Technical Requirements

- Python 3.8+
- Watchdog library
- OpenAI API access
- FFmpeg (for potential audio preprocessing)

## Configuration
The system will require the following configuration:
- OpenAI API credentials
- Watched directory path
- Output directory path
- Supported file types
- Logging preferences

## Future Enhancements
- Support for additional audio formats
- Batch processing capabilities
- Audio preprocessing options
- Advanced transcription options (timestamps, speaker detection)
- Integration with notification systems

## Getting Started
1. Install required dependencies
2. Configure API credentials
3. Set up directory structure
4. Run the monitoring service

## Notes
- The system will initially focus on M4A files only
- All processing will be asynchronous
- Failed transcriptions will be logged for manual review