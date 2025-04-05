from pathlib import Path
import json
from .charset import Charset
from .utilities.logger import VSNSLLogger

class CharsetLoader:
    """Handles charset loading operations"""
    def __init__(self, charset: Charset):
        self.logger = VSNSLLogger().logger
        self.charset = charset

    def load_from_directory(self, charset_dir: Path):
        """Load charsets from a directory"""
        charset_files = list(charset_dir.rglob('*'))
        
        if not charset_files:
            self.logger.error("No charset files found")
            raise FileNotFoundError("Charset directory is empty")
            
        for path in charset_files:
            self._load_single_file(path)

    def _load_single_file(self, path: Path):
        """Load individual charset file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                charset_data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self.logger.error(f"Invalid file format: {path.name} - {str(e)}")
            return

        if 'mapping' not in charset_data:
            self.logger.error(f"Missing mapping in {path.name}")
            return

        for char, value in charset_data['mapping'].items():
            self.charset.charset[char] = value + 100  # Maintain original adjustment 