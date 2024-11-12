import json
import logging
from pathlib import Path
import sys

# Get the logger for the current module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Explicitly set the logger level to INFO

# Configure logging
logging.basicConfig(
    filename=f'{Path(__file__).parent}/resources/logs/activity.log',
    level=logging.INFO,  # This should already be set to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class VSNSL:
    def __init__(self, encryptionLock: int):
        """Sets up the class with the encryption lock and the character mapping dictionary."""
        logger.info(f"Initializing {self.__class__.__name__} class ({hex(id(self))})")
        charsetPath = Path(f'{Path(__file__).parent}/resources/charset.json')
        if not charsetPath.exists():
            logger.error("Charset file not found.")
            raise Exception("Charset file not found. Make sure you installed it correctly and run the script again.")
        else:
            self.letters = json.loads(charsetPath.read_text())
            logger.info("Charset loaded successfully.")

        self.encryptionLock = encryptionLock
        logger.info(f"Encryption lock set to: {self.encryptionLock}")

        for char, num in self.letters.items():
            self.letters[char] = int(num) + 100
        logger.info("Character mapping initialized.")

    def get_pairs(self, s):
        """Splits the string into chunks of 3 characters."""
        pairs = []
        for i in range(0, len(s) - 1, 3):
            pairs.append(s[i:i+3])
        return pairs

    def get_key(self, dictObj: dict, pitchfork: object) -> object:
        """Returns the key of the given value in the dictionary."""
        for key, value in dictObj.items():
            if value == pitchfork:
                return key
        return None

    def encodeData(self, data: object) -> str:
        """Encodes the given data using the character mapping dictionary."""
        returnText = ''
        if isinstance(data, str):
            for letter in data:
                try:
                    returnText += str(self.letters[letter])
                    logger.debug(f"Encoded {letter} to {self.letters[letter]}")
                except Exception as e:
                    logger.exception("Exception during encoding")
            if len(returnText) > 640:
                sys.set_int_max_str_digits(len(returnText))
            encoded_result = str(int(returnText) // self.encryptionLock)
            logger.info("Successfully encoded data.")
            return encoded_result

    def decodeData(self, data: str) -> str:
        """Decodes the given data using the character mapping dictionary."""
        returnText = ''
        unfound_count = 0
        threshold = 5  # Set a threshold for the number of unfound values

        logger.info(f"Starting decoding process for data: {data}")

        if isinstance(data, str):
            try:
                multiplied_data = str(int(data) * self.encryptionLock)
                pairs = self.get_pairs(multiplied_data)
            except ValueError as e:
                logger.error(f"Data format error: {e}")
                raise ValueError("Decryption failed due to data format error.")

            for item in pairs:
                try:
                    key = self.get_key(self.letters, int(item))
                    if key is not None:
                        returnText += key
                        logger.debug(f"Decoded {item} to {key}")
                    else:
                        unfound_count += 1
                        logger.warning(f"Value {item} not found in character mapping.")
                except ValueError as e:
                    logger.error(f"Error converting pair to integer: {e}")
                    raise ValueError("Decryption failed due to data conversion error.")

            if unfound_count > threshold:
                logger.error(f"Too many unfound values ({unfound_count}). Possible issues: incorrect encryption lock, data corruption, or charset mismatch.")
                raise ValueError("Decryption failed due to too many unfound values.")

        if unfound_count > 0:
            logger.warning(f"{unfound_count} values not found in character mapping.")

        logger.info("Successfully decoded data.")
        return returnText