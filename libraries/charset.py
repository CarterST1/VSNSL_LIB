from typing import Union, Any
from pathlib import Path
import json, getpass, sys
from datetime import datetime

class Charset:
    def __init__(self) -> None:
        """Initialize the Charset object with default values."""
        self.author = ""
        self.timestamp = 0
        self.charset = {}  # Initialize an empty charset dictionary
        self.priority = 1

    def _get_max_value(self) -> int:
        """Helper function to get the maximum integer value in the charset."""
        # Filter to only consider integer values
        int_values = [value for value in self.charset.values() if isinstance(value, int)]
        return max(int_values, default=-1)  # Get the maximum value or -1 if empty

    def addKey(self, keyName: str) -> int:
        """Add a new key to the charset with a value that is one more than the current maximum value.

        Args:
            keyName (str): The name of the key to be added.

        Returns:
            int: 1 if the key was added successfully, 0 otherwise.
        """
        if isinstance(keyName, str):
            max_value = self._get_max_value()  # Use the helper function to get the max value
            self.charset[keyName] = max_value + 1 if max_value != -1 else 0
            return 1
        else:
            return 0

    def rmvKey(self, keyName: str) -> int:
        """Remove a key from the charset.

        Args:
            keyName (str): The name of the key to be removed.

        Returns:
            int: 1 if the key was removed successfully, 0 if the key was not found.
        """
        if keyName in self.charset:
            del self.charset[keyName]
            return 1
        else:
            return 0

    def load_charset(self, path: Path) -> int:
        """Load charset data from a specified file path or JSON string.

        Args:
            path (Path): The path to the JSON file containing charset data.

        Returns:
            int: 1 if loading was successful, 0 otherwise.
        """
        if path and path.is_file():
            try:
                path_json: dict = json.loads(path.read_text())
            except json.JSONDecodeError as e:
                print(f"JSON decode operation failed. Err: {e.msg}")
                return 0
            else:
                if not path_json.get("mapping", None):
                    raise Exception("Mapping must be provided")
                author_default = getpass.getuser() if sys.platform == "win32" else "User"
                now = datetime.now()
                self.author = path_json.get("author", author_default)
                self.timestamp = path_json.get("timestamp", now.timestamp())
                
                # Load the mapping and adjust values
                self.charset = {}
                for key, value in path_json["mapping"].items():
                    if isinstance(value, int):  # Ensure value is an integer
                        value += 100  # Adjust the value
                    self.charset[key] = value  # Store the adjusted value

                return 1
        return 0  # Return failure status if no path is provided

    def display_charset(self) -> None:
        """Display the current charset in a readable format."""
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
        if isinstance(newCharset, Charset):
            newAuthor = newCharset.author
            newTimestamp = newCharset.timestamp
            newCharset = newCharset.charset  # Extract charset from another Charset object

            self.author = newAuthor
            self.timestamp = newTimestamp
            self.charset = newCharset  # Set the new charset

    def __truediv__(self, other: Union['Charset', Any]):
        """Define the behavior of the division operator for Charset objects."""
        if isinstance(other, Charset):  # Use the actual Charset class here
            self.override_charset(other)  # Override current charset with another Charset's charset
            return self

    def __mul__(self, other: Union['Charset', Any]):
        """Define the behavior of the multiplication operator for Charset objects."""
        if isinstance(other, Charset):
            other.override_charset(self)
            return other

    def merge(self, *other_charsets: Union['Charset', list[dict]]) -> 'Charset':
        """Merge multiple charsets into the current charset.

        Args:
            *other_charsets (Union[Charset, list[dict]]): Other charsets to merge.

        Returns:
            Charset: The updated charset after merging.
        """
        for charset in other_charsets:
            if isinstance(charset, Charset):
                for key, value in charset.charset.items():
                    if key not in self.charset:
                        self.charset[key] = value
            elif isinstance(charset, list):
                for item in charset:
                    for key, value in item.items():
                        if key not in self.charset:
                            self.charset[key] = value
        return self