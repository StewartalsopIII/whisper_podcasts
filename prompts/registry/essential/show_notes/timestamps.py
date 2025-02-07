import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class TimestampEntry:
    time: str  # In MM:SS format
    topic: str

@dataclass
class SRTEntry:
    index: int
    start_time: str
    end_time: str
    text: str

SYSTEM_PROMPT = """You are an expert at creating podcast timestamps and summarizing discussion topics.
Your task is to identify key discussion points at regular 5-minute intervals from podcast transcripts.
For each interval, provide a concise (1-2 sentence) summary of the main topics discussed."""

CHUNK_PROMPT_TEMPLATE = """Analyze this segment of a podcast transcript and identify the main topics 
discussed in each 5-minute interval. This is chunk {current_chunk} of {total_chunks}.

Transcript segment with timestamps:
{transcript_text}

For each 5-minute interval, provide:
1. A timestamp (MM:SS format)
2. A concise summary of the main topics discussed

Use this format:
05:00 - Discussion of topic A
10:00 - Discussion of topic B"""

FINAL_PROMPT_TEMPLATE = """Combine these timestamp segments into a coherent timeline of the episode.
Ensure topics flow naturally and remove any redundant entries.

Segments to combine:
{segments}

Create a unified timeline with 5-minute intervals."""

def parse_srt_timestamp(timestamp: str) -> timedelta:
    """Convert SRT timestamp to timedelta"""
    time_pattern = r'(\d{2}):(\d{2}):(\d{2}),(\d{3})'
    match = re.match(time_pattern, timestamp)
    if not match:
        raise ValueError(f"Invalid timestamp format: {timestamp}")
    
    hours, minutes, seconds, milliseconds = map(int, match.groups())
    return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

def parse_srt_transcript(transcript_text: str) -> List[SRTEntry]:
    """Parse SRT formatted transcript into structured entries"""
    entries = []
    current_entry = None
    
    for line in transcript_text.strip().split('\n'):
        line = line.strip()
        if not line:
            if current_entry:
                entries.append(current_entry)
                current_entry = None
            continue
            
        if current_entry is None:
            try:
                index = int(line)
                current_entry = SRTEntry(index=index, start_time='', end_time='', text='')
            except ValueError:
                continue
        elif '-->' in line:
            start, end = line.split(' --> ')
            current_entry.start_time = start
            current_entry.end_time = end
        else:
            if current_entry.text:
                current_entry.text += ' ' + line
            else:
                current_entry.text = line
    
    if current_entry:
        entries.append(current_entry)
    
    return entries

def group_by_time_interval(entries: List[SRTEntry], interval_minutes: int = 5) -> List[Tuple[str, str]]:
    """Group transcript entries into time intervals"""
    interval_segments = []
    current_text = []
    interval_delta = timedelta(minutes=interval_minutes)
    current_interval = 0
    
    for entry in entries:
        entry_time = parse_srt_timestamp(entry.start_time)
        interval_index = int(entry_time.total_seconds() // (interval_minutes * 60))
        
        # If we've moved to a new interval
        if interval_index > current_interval:
            if current_text:
                # Format timestamp for current interval
                interval_time = f"{(current_interval * interval_minutes):02d}:00"
                interval_segments.append((interval_time, ' '.join(current_text)))
                current_text = []
            current_interval = interval_index
        
        current_text.append(entry.text)
    
    # Add the last segment
    if current_text:
        last_interval = f"{(current_interval * interval_minutes):02d}:00"
        interval_segments.append((last_interval, ' '.join(current_text)))
    
    return interval_segments

def process_timestamps(client, transcript_text: str) -> List[TimestampEntry]:
    """Process transcript to generate timestamped topic summaries"""
    # Parse SRT transcript
    entries = parse_srt_transcript(transcript_text)
    
    # Group into 5-minute intervals
    interval_segments = group_by_time_interval(entries)
    
    # Process each interval with GPT to summarize topics
    timestamp_entries = []
    for timestamp, segment_text in interval_segments:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Summarize the main topics discussed in this segment:\n{segment_text}"}
                ],
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
            timestamp_entries.append(TimestampEntry(time=timestamp, topic=summary))
        except Exception as e:
            print(f"Error processing segment at {timestamp}: {e}")
            continue
    
    return timestamp_entries

def format_timestamp_section(entries: List[TimestampEntry]) -> str:
    """Format timestamp entries into markdown"""
    if not entries:
        return "No timestamps available"
    
    markdown = "## Episode Timeline\n\n"
    for entry in entries:
        markdown += f"**{entry.time}** - {entry.topic}\n\n"
    
    return markdown

def extract_timestamps(client, transcript_text: str) -> str:
    """Main function to extract and format timestamps"""
    try:
        # Process transcript into timestamp entries
        entries = process_timestamps(client, transcript_text)
        
        # Format into markdown
        return format_timestamp_section(entries)
    except Exception as e:
        print(f"Error extracting timestamps: {e}")
        return "Error generating timestamps"