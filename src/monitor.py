import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from transcriber import WhisperTranscriber

class AudioFileHandler(FileSystemEventHandler):
    def __init__(self, transcriber):
        self.transcriber = transcriber

    def on_created(self, event):
        if event.is_directory:
            return
        
        # Check if the file is an M4A file
        if event.src_path.lower().endswith('.m4a'):
            print(f"Detected new M4A file: {event.src_path}")
            try:
                self.transcriber.transcribe(event.src_path)
            except Exception as e:
                print(f"Error processing file {event.src_path}: {str(e)}")

class PodcastMonitor:
    def __init__(self, watch_path):
        self.watch_path = watch_path
        self.observer = Observer()
        self.transcriber = WhisperTranscriber()

    def start(self):
        event_handler = AudioFileHandler(self.transcriber)
        self.observer.schedule(event_handler, self.watch_path, recursive=False)
        self.observer.start()
        print(f"Started monitoring {self.watch_path} for new M4A files...")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Monitoring stopped")
        
        self.observer.join()

if __name__ == "__main__":
    # Get the absolute path to the podcasts directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    watch_dir = os.path.join(base_dir, "podcasts")
    
    # Create the podcasts directory if it doesn't exist
    if not os.path.exists(watch_dir):
        os.makedirs(watch_dir)
    
    monitor = PodcastMonitor(watch_dir)
    monitor.start()