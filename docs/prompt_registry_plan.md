# Prompt Registry System Design

## Overview
This document outlines the design and workflow for a flexible prompt registry system that manages, versions, and automates the application of analysis prompts to podcast transcripts.

## Core Concepts

### 1. Prompt Definition
- Each prompt is a self-contained YAML file
- Contains both the prompt template and its metadata
- Includes automation rules and trigger conditions
- Versioned for tracking changes and improvements

### 2. Registry Structure
```
prompts/
├── registry/           # Active prompt templates
│   ├── essential/     # Must-run prompts
│   ├── conditional/   # Trigger-based prompts
│   └── experimental/  # Testing prompts
└── versions/          # Historical versions

output/
└── {episode_name}/    # All episode-related content
    ├── transcription.md  # Initial transcription
    ├── summary.md        # Analysis results
    ├── analysis.md       # Analysis results
    └── insights.md       # Analysis results
```

### 3. Workflow Stages

#### A. Prompt Creation
1. Author creates new prompt file
2. System validates prompt structure
3. Prompt is registered in the system
4. Test run on sample transcript
5. Prompt moved to appropriate category

#### B. Transcript Processing
1. New transcript detected in output folder
2. Metadata extracted
3. Trigger conditions checked
4. Matching prompts identified
5. Processing queue created
6. Results saved directly to episode folder

#### C. Result Management
1. All results stored in episode folder
2. Standard output format (markdown)
3. Cross-reference capabilities via metadata
4. Error tracking in processing log
5. Performance metrics per episode

## Automation Levels

### 1. Essential Processing
- Runs on every transcript
- Core analysis prompts
- Basic metadata extraction
- Quality checks

### 2. Conditional Processing
- Based on episode metadata
- Triggered by specific conditions
- Category-specific analysis
- Guest-specific prompts

### 3. Manual Processing
- One-off analysis
- Experimental prompts
- Custom investigations
- Research-specific queries

## Prompt Lifecycle

### 1. Creation Phase
- Draft prompt template
- Define metadata
- Set trigger conditions
- Specify output format
- Add validation rules

### 2. Testing Phase
- Validate structure
- Test on sample data
- Review outputs
- Adjust parameters
- Document behavior

### 3. Active Phase
- Regular usage
- Performance monitoring
- Result validation
- User feedback
- Iteration tracking

### 4. Maintenance Phase
- Version updates
- Performance tuning
- Output refinement
- Documentation updates
- Usage analytics

## Result Management

### 1. Storage Structure
```
output/
└── {episode_name}/
    ├── transcription.md     # Original transcript
    ├── metadata.yaml        # Episode metadata
    ├── summary.md           # Generated summary
    ├── analysis.md          # Detailed analysis
    ├── insights.md          # Key insights
    └── processing_log.yaml  # Processing history
```

### 2. Output Formats
- Markdown for human-readable results
- JSON for structured data
- YAML for configuration
- CSV for data exports
- HTML for web viewing

## Usage Examples

### 1. Adding New Prompt
```yaml
# Example workflow
1. Create prompt file in prompts/registry/experimental/
2. Test with sample transcript
3. Review results
4. Adjust as needed
5. Move to appropriate category
```

### 2. Automated Processing
```yaml
# Processing flow
1. New transcript detected
2. Metadata extracted
3. Essential prompts run
4. Triggers checked
5. Conditional prompts run
6. Results saved
7. Processing log updated
```

### 3. Manual Analysis
```yaml
# Manual workflow
1. Select transcript
2. Choose prompts
3. Run analysis
4. Review results
5. Save insights
6. Update documentation
```

## Future Enhancements

### 1. Short Term
- Prompt validation system
- Result templating
- Basic automation rules
- Error handling
- Performance tracking

### 2. Medium Term
- Web interface
- Result visualization
- Prompt marketplace
- Advanced triggers
- Batch processing

### 3. Long Term
- AI-assisted prompt creation
- Advanced analytics
- Integration APIs
- Collaborative features
- Learning system

## Implementation Phases

### Phase 1: Foundation
- Basic directory structure
- Simple prompt registry
- Manual processing
- Result storage
- Basic documentation

### Phase 2: Automation
- Trigger system
- Processing queue
- Result formatting
- Error handling
- Logging system

### Phase 3: Enhancement
- Web interface
- Analytics
- Advanced triggers
- Batch processing
- API access

### Phase 4: Advanced Features
- AI assistance
- Collaborative tools
- Integration options
- Custom workflows
- Advanced analytics

## Detailed Phase 1 Implementation Steps

### 1. Basic Directory Structure
1. Create initial prompt registry structure:
   ```
   prompts/
   ├── registry/
   │   ├── essential/      # Core analysis prompts
   │   ├── conditional/    # Context-specific prompts
   │   └── experimental/   # Development prompts
   └── versions/          # Version history
   ```

### 2. Simple Prompt Registry
1. Design YAML prompt template:
   ```yaml
   id: unique_prompt_id
   version: 1.0
   category: essential|conditional|experimental
   name: "Prompt Name"
   description: "What this prompt does"
   trigger_conditions:
     required_fields: []
     content_markers: []
   template: |
     Your analysis instructions here
     {transcript_content}
   output_format: markdown
   ```

2. Create core prompt templates:
   - Basic episode summary
   - Key points extraction
   - Topic identification
   - Guest background (if applicable)
   - Action items/takeaways

3. Implement prompt validation:
   - YAML structure verification
   - Required fields checking
   - Template variable validation

### 3. Manual Processing
1. Create processing script:
   ```python
   # Basic workflow
   - Load prompt template
   - Read transcription
   - Apply prompt
   - Save results
   ```

2. Implement basic handlers:
   - Transcription file reading
   - Template variable substitution
   - Output formatting
   - Error handling

3. Add manual processing tools:
   - CLI for running prompts
   - Prompt selection interface
   - Result preview
   - Basic error reporting

### 4. Result Storage
1. Implement result writer:
   - Format validation
   - File naming convention
   - Metadata tracking
   - Version stamping

2. Set up episode folder structure:
   ```
   output/
   └── {episode_name}/
       ├── transcription.md     # Original transcript
       ├── metadata.yaml        # Episode metadata
       ├── summary.md           # Generated summary
       ├── analysis.md          # Detailed analysis
       ├── insights.md          # Key insights
       └── processing_log.yaml  # Processing history
   ```

3. Add result validation:
   - Output format checking
   - File integrity verification
   - Metadata completeness
   - Log consistency

### 5. Basic Documentation
1. Create core documentation:
   - System overview
   - Directory structure
   - Prompt format specification
   - Processing workflow

2. Add usage guides:
   - Prompt creation tutorial
   - Manual processing steps
   - Result interpretation
   - Troubleshooting guide

3. Implement documentation tools:
   - Template generator
   - Example creator
   - Validation checker
   - Quick start guide

### Success Criteria for Phase 1
- Directory structure is complete and validated
- Basic prompt templates are created and working
- Manual processing successfully generates results
- Results are properly stored and organized
- Documentation is clear and comprehensive

### Next Steps After Phase 1
- Review system performance
- Gather user feedback
- Identify automation opportunities
- Plan Phase 2 implementation details