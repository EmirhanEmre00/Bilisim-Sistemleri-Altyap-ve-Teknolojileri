import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime

LOG_FILE = '/home/ubuntu/bsm/logs/changes.json'
WATCHED_DIR = '/home/ubuntu/bsm/test'

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return  # Dizin değişikliklerini göz ardı et

        change = {
            'event_type': event.event_type,
            'path': event.src_path,
            'timestamp': datetime.now().isoformat()
        }
        self.log_change(change)

    def log_change(self, change):
        # Log dosyasına yazmadan önce mevcut veriyi okuyun
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Yeni değişikliği ekleyin
        data.append(change)

        # JSON dosyasına yazın
        with open(LOG_FILE, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCHED_DIR, recursive=True)
    observer.start()
    print(f"Monitoring changes in {WATCHED_DIR}. Logging to {LOG_FILE}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
