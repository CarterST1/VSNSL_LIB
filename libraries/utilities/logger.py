import logging
from pathlib import Path

class VSNSLLogger:
    """Centralized logging configuration"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._configure_logging()
    
    def _configure_logging(self):
        logging.basicConfig(
            filename=f'{Path(__file__).parent.parent.parent}/resources/logs/activity.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding="utf-8"
        ) 