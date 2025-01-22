import os
import shutil
from datetime import datetime
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileOrganizer:
    def __init__(self, path):
        self.path = path
        # Define category mappings
        self.categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xlsx', '.csv'],
            'Audio': ['.mp3', '.wav', '.flac', '.m4a', '.aac'],
            'Video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.php']
        }
        
    def create_folders(self):
        """Create category folders if they don't exist"""
        for category in self.categories:
            folder_path = os.path.join(self.path, category)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def organize_file(self, file_path):
        """Organize a single file into appropriate category folder"""
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # Find the category for the file
            for category, extensions in self.categories.items():
                if file_extension in extensions:
                    destination_folder = os.path.join(self.path, category)
                    file_name = os.path.basename(file_path)
                    destination_path = os.path.join(destination_folder, file_name)
                    
                    # Handle duplicate files
                    if os.path.exists(destination_path):
                        base_name = os.path.splitext(file_name)[0]
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        new_name = f"{base_name}_{timestamp}{file_extension}"
                        destination_path = os.path.join(destination_folder, new_name)
                    
                    try:
                        shutil.move(file_path, destination_path)
                        print(f"Moved {file_name} to {category}")
                    except Exception as e:
                        print(f"Error moving {file_name}: {str(e)}")
                    break

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, organizer):
        self.organizer = organizer

    def on_created(self, event):
        if not event.is_directory:
            self.organizer.organize_file(event.src_path)

def main():
    # Set the path to monitor (current directory by default)
    path = os.getcwd()
    
    # Create and setup the file organizer
    organizer = FileOrganizer(path)
    organizer.create_folders()
    
    # Set up file system monitoring
    event_handler = FileEventHandler(organizer)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    
    print(f"Started monitoring {path}")
    print("Press Ctrl+C to stop")
    
    try:
        # Organize existing files
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            organizer.organize_file(file_path)
            
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped monitoring")
    observer.join()

if __name__ == "__main__":
    main() 