import time
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver  # More reliable for network filesystems
from watchdog.events import FileSystemEventHandler
import os
from pathlib import Path
from transcriber import WhisperTranscriber
from folder_manager import PodcastFolderManager

class ZoomFolderHandler(FileSystemEventHandler):
    def __init__(self, base_path):
        self.base_path = base_path
        self.processed_m4a = set()  # Track M4A files we've already processed
        self.transcriber = WhisperTranscriber()  # Initialize transcriber
        self.folder_manager = PodcastFolderManager()  # Initialize folder manager
        print(f"Monitoring for new recordings in: {self.base_path}")
        
    def on_moved(self, event):
        # Skip if the path contains the renamed format (guest name followed by date)
        if any(self.folder_manager.processed_folders):
            for processed in self.folder_manager.processed_folders:
                if processed in event.dest_path:
                    return
                
        if event.dest_path.endswith('.m4a') and not 'Audio Record' in event.dest_path:
            self._process_m4a(event.dest_path)
            
    def _process_m4a(self, file_path):
        if file_path in self.processed_m4a:
            return
            
        self.processed_m4a.add(file_path)
        folder_name = Path(file_path).parent.name
        print(f"\n📁 New recording detected: {folder_name}")
        print(f"🎤 Processing audio file...")
        
        # Wait for the file to be fully written
        if self._wait_for_file_ready(file_path):
            print(f"✅ Audio file ready for transcription")
            try:
                # Get the folder containing the M4A file
                output_folder = str(Path(file_path).parent)
                # Transcribe and save to the same folder
                transcript_path = self.transcriber.transcribe(file_path, output_folder)
                print(f"✅ Transcription saved to: {transcript_path}")
                
                # After successful transcription, try to rename the folder
                self.folder_manager.rename_folder(output_folder)
                return True
            except Exception as e:
                print(f"❌ Transcription failed: {str(e)}")
                # Remove from processed files to allow retry
                self.processed_m4a.remove(file_path)
                return False
        return False
            
    def _wait_for_file_ready(self, file_path, check_interval=5, timeout=3600):
        """Wait for the file to stop changing size"""
        previous_size = -1
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                current_size = os.path.getsize(file_path)
                if current_size == previous_size and previous_size > 0:
                    return True
                previous_size = current_size
                if previous_size > 0:  # Only show progress for actual file content
                    print(f"⏳ Waiting for file conversion... ({current_size} bytes)", end='\r')
            time.sleep(check_interval)
        return False
        if event.is_directory:
            folder_path = event.src_path
            print(f"New folder detected: {folder_path}")
            
            # Create a new observer for this specific folder
            folder_observer = Observer()
            folder_handler = M4AFileHandler(folder_path)
            folder_observer.schedule(folder_handler, folder_path, recursive=False)
            folder_observer.start()
            
            # Store the observer so we can stop it later if needed
            self.folder_observers[folder_path] = folder_observer

class M4AFileHandler(FileSystemEventHandler):
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.m4a_detected = False
        self.processed_files = set()
        
    def _wait_for_file_ready(self, file_path, check_interval=5, timeout=3600):
        """Wait for the file to stop changing size"""
        previous_size = -1
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                current_size = os.path.getsize(file_path)
                if current_size == previous_size and previous_size > 0:
                    print(f"✅ Audio file ready for transcription")
                    return True
                previous_size = current_size
                if previous_size > 0:  # Only show progress for actual file content
                    print(f"⏳ Waiting for file conversion... ({current_size} bytes)", end='\r')
            time.sleep(check_interval)
            
        return False
    
    def _wait_for_file_ready(self, file_path, check_interval=5, timeout=3600):
        """
        Wait for the file to stop changing size, indicating it's fully written.
        
        Args:
            file_path: Path to the file
            check_interval: Seconds between size checks
            timeout: Maximum seconds to wait
        """
        previous_size = -1
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                current_size = os.path.getsize(file_path)
                if current_size == previous_size and previous_size > 0:
                    print(f"File size stabilized at {current_size} bytes")
                    return True
                previous_size = current_size
            time.sleep(check_interval)
            
        return False
    
    def _verify_file_complete(self, file_path):
        """
        Verify that the M4A file is complete and valid.
        """
        try:
            # Basic check: file exists and has size > 0
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                return True
            return False
        except Exception as e:
            print(f"Error verifying file: {e}")
            return False

def start_monitoring(path):
    base_path = Path(path).resolve()
    event_handler = ZoomFolderHandler(base_path)
    observer = PollingObserver()
    observer.schedule(event_handler, str(base_path), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        # Stop any folder-specific observers
        for folder_observer in event_handler.folder_observers.values():
            folder_observer.stop()
    
    observer.join()
    # Join any folder-specific observers
    for folder_observer in event_handler.folder_observers.values():
        folder_observer.join()

if __name__ == "__main__":
    WATCH_PATH = "/Users/stewartalsop/Dropbox/Crazy Wisdom/Beautifully Broken/Test for Transcription"
    try:
        start_monitoring(WATCH_PATH)
    except Exception as e:
        print(f"Error starting monitor: {e}")
