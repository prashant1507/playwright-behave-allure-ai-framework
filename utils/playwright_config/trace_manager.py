import os
import shutil

from helpers.constants.framework_constants import TRACES_DIR, TRACES_VIDEOS_DIR
from utils.logger import log_info


class TraceManager:
    def __init__(self, enable_tracing):
        self.traces_dir = TRACES_DIR
        if enable_tracing:
            self.ensure_traces_directory()

    def ensure_traces_directory(self):
        directories = [
            self.traces_dir,
            TRACES_VIDEOS_DIR,
            f"{self.traces_dir}/har",
            f"{self.traces_dir}/archived"
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def archive_old_traces(self, days_to_keep=7):
        """Archive traces older than specified days"""
        import time
        current_time = time.time()
        cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)

        for filename in os.listdir(self.traces_dir):
            if filename.endswith('.zip'):
                file_path = os.path.join(self.traces_dir, filename)
                if os.path.getmtime(file_path) < cutoff_time:
                    archive_path = os.path.join(f"{self.traces_dir}/archived", filename)
                    shutil.move(file_path, archive_path)
                    log_info(f"Archived old trace: {filename}")

    def cleanup_empty_directories(self):
        """Remove empty trace directories"""
        for root, dirs, files in os.walk(self.traces_dir, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    log_info(f"Removed empty directory: {dir_path}")

    def get_trace_summary(self):
        trace_files = [f for f in os.listdir(self.traces_dir) if f.endswith('.zip')]
        video_files = [f for f in os.listdir(f"{self.traces_dir}/videos") if f.endswith('.webm')]
        har_files = [f for f in os.listdir(f"{self.traces_dir}/har") if f.endswith('.har')]

        return {
            'trace_files': len(trace_files),
            'video_files': len(video_files),
            'har_files': len(har_files),
            'total_size_mb': get_directory_size_mb(self.traces_dir)
        }

def get_directory_size_mb(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return round(total_size / (1024 * 1024), 2)