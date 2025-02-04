import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

class WhisperTranscriber:
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB in bytes
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.output_dir = os.path.join(self.base_dir, "output")
        self.temp_dir = os.path.join(self.base_dir, "temp")
        
        # Create necessary directories
        for directory in [self.output_dir, self.temp_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def compress_audio(self, input_file, max_size_mb=25):
        """Compress audio file to meet size requirements"""
        # Change the output extension to .mp3
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(
            self.temp_dir,
            f"compressed_{base_name}.mp3"
        )
        
        try:
            print("Compressing audio file...")
            # First attempt with initial settings
            bitrates = ['32k', '24k', '16k']  # Try progressively lower bitrates
            
            for bitrate in bitrates:
                command = [
                    'ffmpeg',
                    '-i', input_file,
                    '-acodec', 'libmp3lame',
                    '-b:a', bitrate,       # Variable bitrate
                    '-ac', '1',            # Mono audio
                    '-ar', '22050',        # Lower sampling rate
                    '-y',                  # Overwrite output
                    output_file
                ]
                
                # Run ffmpeg
                result = subprocess.run(
                    command,
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                if os.path.exists(output_file):
                    new_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
                    print(f"Compressed file size with {bitrate} bitrate: {new_size:.2f}MB")
                    
                    # If file is under the limit, we're done
                    if new_size < max_size_mb:
                        return output_file
                    else:
                        print(f"File still too large with {bitrate}, trying lower bitrate...")
                        continue
            
            # If we get here, even the lowest bitrate didn't work
            raise Exception("Could not compress file enough to meet size limit")
        except subprocess.CalledProcessError as e:
            print(f"Error compressing file: {str(e)}")
            raise

    def format_timestamp(self, seconds):
        """Convert seconds to MM:SS format"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def transcribe(self, audio_file_path):
        """
        Transcribe the given audio file using OpenAI's Whisper API with timestamps
        """
        print(f"Starting transcription of {audio_file_path}")
        
        try:
            # Check file size
            file_size = os.path.getsize(audio_file_path)
            
            # If file is too large, compress it
            if file_size > self.MAX_FILE_SIZE:
                print(f"File size ({file_size/1024/1024:.2f}MB) exceeds limit. Compressing...")
                audio_file_path = self.compress_audio(audio_file_path)
                print(f"Compressed file created at: {audio_file_path}")
            
            with open(audio_file_path, "rb") as audio_file:
                # Using srt format to get timestamps
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="srt"
                )

            # Create folder name based on input filename
            original_name = os.path.splitext(os.path.basename(audio_file_path))[0]
            if original_name.startswith('compressed_'):
                original_name = original_name[len('compressed_'):]
            
            # Create folder path and ensure it exists
            folder_path = os.path.join(self.output_dir, original_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Create markdown file path inside the new folder
            output_file = os.path.join(folder_path, "transcription.md")

            # Write the transcript with timestamps
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("# Transcription with Timestamps\n\n")
                # SRT format is returned as a string, we'll write it directly
                f.write(transcript)

            print(f"Transcription completed and saved to {output_file}")
            
            # Clean up temporary compressed file if it exists
            if audio_file_path.startswith(self.temp_dir):
                os.remove(audio_file_path)
                print("Cleaned up temporary compressed file")
            
            return output_file

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error during compression:")
            print(f"Command output: {e.output}")
            print(f"Error output: {e.stderr}")
            raise
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            # Clean up any temporary files if they exist
            if 'audio_file_path' in locals() and audio_file_path.startswith(self.temp_dir):
                try:
                    os.remove(audio_file_path)
                    print("Cleaned up temporary compressed file")
                except:
                    pass
            raise