import re
from pathlib import Path
import os

class PodcastFolderManager:
    def __init__(self):
        self.processed_folders = set()
    
    def rename_folder(self, folder_path):
        """Rename folder with pattern: Guest Name - Topic - YYYY-MM-DD"""
        # Convert to Path object if string
        folder_path = Path(folder_path)
        
        # Skip if already processed
        if str(folder_path) in self.processed_folders:
            return
        
        # Extract info
        info = self._extract_episode_info(folder_path)
        if not info:
            print(f"Could not extract episode info from {folder_path}")
            return
        
        date = self._extract_date(folder_path)
        if not date:
            print(f"Could not extract date from folder name: {folder_path.name}")
            return
            
        guest, topic = info['guest'], info['topic']
        new_name = self._generate_folder_name(guest, topic, date)
        success = self._perform_rename(folder_path, new_name)
        
        if success:
            self.processed_folders.add(str(folder_path))
            print(f"Successfully renamed folder to: {new_name}")
        
    def _extract_episode_info(self, folder_path):
        """Extract guest and topic from episode_info.md"""
        info_path = folder_path / 'episode_info.md'
        if not info_path.exists():
            print(f"No episode_info.md found in {folder_path}")
            return None
            
        try:
            with open(info_path, 'r') as f:
                content = f.read()
                
            # Extract guest name and topic using regex
            guest_match = re.search(r'Guest:\s*(.+?)(?:\n|$)', content)
            topic_match = re.search(r'Topic:\s*(.+?)(?:\n|$)', content)
            
            if not guest_match:
                print("Could not find guest name in episode_info.md")
                return None
                
            if not topic_match:
                print("Could not find topic in episode_info.md")
                return None
            
            return {
                'guest': guest_match.group(1).strip(),
                'topic': topic_match.group(1).strip()
            }
        except Exception as e:
            print(f"Error reading episode info: {e}")
            return None
        
    def _extract_date(self, folder_path):
        """Extract date from folder name"""
        # Look for YYYY-MM-DD pattern in folder name
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', folder_path.name)
        if date_match:
            return date_match.group(1)
        return None
        
    def _generate_folder_name(self, guest, topic, date):
        """Generate new folder name"""
        # If guest is "Unknown Speaker", use topic instead
        primary_name = topic if guest == "Unknown Speaker" else guest
        # Clean the components to make them safe for filenames
        primary_name = self._clean_name(primary_name)
        return f"{primary_name} - {date}"
        
    def _clean_name(self, name):
        """Clean a name to make it safe for filenames"""
        # Replace potentially problematic characters
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        # Replace multiple spaces with single space
        name = re.sub(r'\s+', ' ', name)
        return name.strip()
        
    def _perform_rename(self, old_path, new_name):
        """Safely rename the folder"""
        try:
            new_path = old_path.parent / new_name
            
            # Check if target already exists
            if new_path.exists():
                print(f"Cannot rename: {new_name} already exists")
                return False
            
            # Perform the rename
            old_path.rename(new_path)
            
            # Add the NEW path to processed_folders, not the old one
            self.processed_folders.add(str(new_path))
            return True
            
        except Exception as e:
            print(f"Error renaming folder: {e}")
            return False