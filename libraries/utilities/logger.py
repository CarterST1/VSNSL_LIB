import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

class Logger:
    _instance = None
    
    def __new__(cls, name='VSNSL', log_level=logging.INFO, 
                log_file='resources/logs/activity.log', 
                max_bytes=5*1024*1024, backup_count=5):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, name='VSNSL', log_level=logging.INFO,
                 log_file='resources/logs/activity.log',
                 max_bytes=5*1024*1024, backup_count=5):
        if self._initialized:
            return
            
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize default formatters with filename
        self.file_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        self.console_formatter = logging.Formatter('[%(levelname)s]: %(message)s')
        
        # File handler with rotation
        self.file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, 
            backupCount=backup_count, encoding='utf-8'
        )
        self.file_handler.setFormatter(self.file_formatter)
        
        # Console handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.console_formatter)
        
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        self._initialized = True

    def set_file_formatter(self, fmt: str):
        """Set custom format for file logs"""
        self.file_formatter = logging.Formatter(fmt)
        self.file_handler.setFormatter(self.file_formatter)

    def set_console_formatter(self, fmt: str):
        """Set custom format for console logs"""
        self.console_formatter = logging.Formatter(fmt)
        self.console_handler.setFormatter(self.console_formatter)

    def debug(self, message):
        self.logger.debug(message)
        
    def info(self, message):
        self.logger.info(message)
        
    def warning(self, message):
        self.logger.warning(message)
        
    def error(self, message):
        self.logger.error(message)
        
    def critical(self, message):
        self.logger.critical(message)
        
    def log(self, level, message):
        self.logger.log(level, message)

# Create a default instance for easy import
vsnsl_logger = Logger()
