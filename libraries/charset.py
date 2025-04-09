from typing import Union, Any
from pathlib import Path
import json, getpass, sys
from jsonschema import validate, ValidationError
from datetime import datetime
from .utilities.logger import vsnsl_logger as logger

class Charset:
    def __init__(self) -> None:
        """Initialize the Charset object with default values."""
        logger.debug("Initializing new Charset instance")
        self.author = ""
        self.timestamp = 0
        self.charset = {}  # Initialize an empty charset dictionary
        self.priority = 1

        self.CHARSET_SCHEMA = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Charset File",
            "type": "object",
            "properties": {
                "author": { "type": "string" },
                "timestamp": { "type": "number" },
                "mapping": {
                    "type": "object",
                    "additionalProperties": { "type": "integer" }
                }
            },
            "required": ["author", "timestamp", "mapping"]
        }

    def _get_max_value(self) -> int:
        """Helper function to get the maximum integer value in the charset."""
        logger.debug("Calculating maximum charset value")
        int_values = [value for value in self.charset.values() if isinstance(value, int)]
        max_val = max(int_values, default=-1)
        logger.debug(f"Max charset value: {max_val}")
        return max_val

    def addKey(self, keyName: str) -> int:
        """Add a new key to the charset with a value that is one more than the current maximum value.

        Args:
            keyName (str): The name of the key to be added.

        Returns:
            int: 1 if the key was added successfully, 0 otherwise.
        """
        logger.debug(f"Attempting to add key: {keyName}")
        if isinstance(keyName, str):
            max_value = self._get_max_value()
            new_value = max_value + 1 if max_value != -1 else 0
            self.charset[keyName] = new_value
            logger.info(f"Added key '{keyName}' with value {new_value}")
            return 1
        else:
            logger.error(f"Invalid key type: {type(keyName).__name__}, expected str")
            return 0

    def rmvKey(self, keyName: str) -> int:
        """Remove a key from the charset.

        Args:
            keyName (str): The name of the key to be removed.

        Returns:
            int: 1 if the key was removed successfully, 0 if the key was not found.
        """
        logger.debug(f"Attempting to remove key: {keyName}")
        if keyName in self.charset:
            del self.charset[keyName]
            logger.info(f"Removed key '{keyName}'")
            return 1
        else:
            logger.warning(f"Key '{keyName}' not found during removal")
            return 0

    def load_charset(self, obj: Union[Path, dict]) -> int:
        """Load charset data from a file path or dictionary.

        Args:
            obj (Union[Path, dict]): The path to the JSON file or a dictionary containing charset data.

        Returns:
            int: 1 if loading was successful, 0 otherwise.
        """
        logger.info(f"Loading charset from {type(obj).__name__}")
        path_json = None
        
        if isinstance(obj, dict):
            logger.debug("Loading from dictionary input")
            path_json = obj
        elif obj and obj.is_file():
            try:
                logger.debug(f"Reading charset file: {obj}")
                path_json = json.loads(obj.read_text())
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode failed: {e.msg}")
                return 0
        elif isinstance(obj, Path):
            logger.error(f"Invalid path: {obj} - not a file or doesn't exist")
            return 0
        
        if not path_json or not isinstance(path_json, dict):
            logger.error("Invalid or empty charset data")
            return 0
        
        try:
            logger.debug("Validating charset schema")
            validate(instance=path_json, schema=self.CHARSET_SCHEMA)
        except ValidationError as e:
            logger.error(f"Schema validation failed: {e.message}")
            return 0
        
        author_default = getpass.getuser() if sys.platform == "win32" else "User"
        now = datetime.now()
        self.author = path_json.get("author", author_default)
        self.timestamp = path_json.get("timestamp", now.timestamp())
        
        logger.info(f"Loading charset authored by {self.author}")
        self.charset = {}
        
        for key, value in path_json["mapping"].items():
            if not isinstance(key, str):
                logger.error(f"Invalid key type in mapping: {type(key).__name__}")
                return 0
            if isinstance(value, int):
                value += 100
            self.charset[key] = value
            logger.debug(f"Added mapping: {key} => {value}")
        
        logger.info(f"Successfully loaded {len(self.charset)} charset entries")
        return 1

    def display_charset(self) -> None:
        """Display the current charset in a readable format."""
        logger.debug("Displaying charset contents")
        print("Current Charset:")
        for key, value in self.charset.items():
            print(f"  {key}: {value}")

    def get_charset(self) -> dict:
        """Retrieve the current charset.

        Returns:
            dict: The current charset dictionary.
        """
        return self.charset

    def override_charset(self, newCharset: Union['Charset', list[dict]]):
        """Override the current charset with a new charset.

        Args:
            newCharset (Union[Charset, list[dict]]): The new charset to set.
        """
        logger.warning("Overriding current charset")
        if isinstance(newCharset, Charset):
            logger.info(f"New charset from: {newCharset.author} (timestamp: {newCharset.timestamp})")
            self.author = newCharset.author
            self.timestamp = newCharset.timestamp
            self.charset = newCharset.charset
        else:
            logger.error("Invalid charset type for override")

    def __truediv__(self, other: Union['Charset', Any]):
        """Define the behavior of the division operator for Charset objects."""
        logger.debug("Using division operator for charset override")
        if isinstance(other, Charset):
            self.override_charset(other)
            return self
        logger.warning("Invalid type for charset division operation")

    def __mul__(self, other: Union['Charset', Any]):
        """Define the behavior of the multiplication operator for Charset objects."""
        logger.debug("Using multiplication operator for charset override")
        if isinstance(other, Charset):
            other.override_charset(self)
            return other
        logger.warning("Invalid type for charset multiplication operation")

    def merge(self, *other_charsets: Union['Charset', list[dict]]) -> 'Charset':
        """Merge multiple charsets into the current charset.

        Args:
            *other_charsets (Union[Charset, list[dict]]): Other charsets to merge.

        Returns:
            Charset: The updated charset after merging.
        """
        logger.info(f"Merging {len(other_charsets)} charsets")
        merge_count = 0
        
        for charset in other_charsets:
            if isinstance(charset, Charset):
                merge_count += len(charset.charset)
                for key, value in charset.charset.items():
                    if key not in self.charset:
                        self.charset[key] = value
            elif isinstance(charset, list):
                for item in charset:
                    merge_count += len(item)
                    for key, value in item.items():
                        if key not in self.charset:
                            self.charset[key] = value
            else:
                logger.warning(f"Invalid charset type for merge: {type(charset).__name__}")
        
        logger.info(f"Merged {merge_count} new entries")
        return self