import os
from pathlib import Path

class FileManager:
    @staticmethod
    def get_file_size(file_path):
        """Get file size in MB"""
        size = os.path.getsize(file_path)
        return round(size / (1024 * 1024), 2)
    
    @staticmethod
    def get_file_extension(file_path):
        """Get file extension"""
        return Path(file_path).suffix.lower()
    
    @staticmethod
    def validate_file(file_path, max_size_mb=500):
        """Validate file before processing"""
        if not os.path.exists(file_path):
            return False, "File not found"
        
        file_size = FileManager.get_file_size(file_path)
        if file_size > max_size_mb:
            return False, f"File too large ({file_size}MB > {max_size_mb}MB)"
        
        return True, "File valid"
    
    @staticmethod
    def create_temp_directory():
        """Create temporary directory for file operations"""
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        return temp_dir
    
    @staticmethod
    def cleanup_temp_files():
        """Clean up temporary files"""
        import shutil
        temp_dir = Path("temp")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
