import json
import logging
from pathlib import Path
import sys
from typing import List
from .charset import Charset, BASE_CHARSET
from .charset_loader import CharsetLoader
from .core_operations import CoreOperations
from .batch_processor import BatchProcessor
from .multi_lock import MultiLockProcessor

# Configure logging
logging.basicConfig(
    filename=f'{Path(__file__).parent}/resources/logs/activity.log',
    level=logging.INFO,  # This should already be set to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding="utf-8"
)

class VSNSL:
    """
    VSNSL class for encoding and decoding data using a character mapping dictionary.

    .. versionadded:: v0.1.1

    This class was developed for a science fair project, and it offers advantages such as extreme security.

    Attributes:
        charset (Charset): An instance of the Charset class for managing character mappings.
        encryptionLock (int): The encryption lock to use for encoding and decoding.

    .. literalinclude:: example.py
    """

    def __init__(self, encryption_lock: int, charset: Charset = None):
        """
        .. versionadded:: v0.1.1

        Initializes the VSNSL class with the given encryption lock.

        This constructor sets up the character mapping and encryption lock for encoding and decoding operations.

        Args:
            encryption_lock (int): The encryption lock to use for encoding and decoding.
        
        Usage:
            .. code-block:: python

                vsnsl = VSNSL(1)
        """

        self.logger = logging.getLogger(__name__)

        self.logger.info(f"Initializing {self.__class__.__name__} class ({hex(id(self))})")
        
        self.charset = charset or BASE_CHARSET
        self.loader = CharsetLoader(self.charset)
        self.core = CoreOperations(self.charset, encryption_lock)
        self.batch = BatchProcessor(self.core)
        self.multilock = MultiLockProcessor(self.core)
        
        self.encryptionLock = encryption_lock if encryption_lock != 0 else 1  # Set the encryption lock
        self.logger.debug(f"Encryption lock set to: {self.encryptionLock}")

        # Load character mappings from charset files
        self._load_charsets()

    def _load_charsets(self):
        """Load character mappings from charset files into the Charset instance."""
        charset_dir = Path(f'{Path(__file__).parent}/resources/charsets')
        self.loader.load_from_directory(charset_dir)

    #---
    
    def get_pairs(self, s: str, separator: int = 3) -> list:
        """
        .. versionadded:: v0.1.1
        .. deprecated:: v0.1.2
            This method is deprecated as it is no longer used. Not used in the current version of the VSNSL class.

        Splits the string into chunks of the given separator.

        This method is useful for breaking down encoded strings into manageable parts.

        Args:
            s (str): The string to split.
            separator (int): The number of characters to split the string into.

        Returns:
            list: A list of the split strings.

        Usage:
            .. code-block:: python

                pairs = VSNSL.get_pairs("101102103", 3)
                print(pairs) # Returns: ["101", "102", "103"]
        """
        pairs = []  # Initialize a list to hold the pairs
        
        pairs.extend(s[i:i+separator] for i in range(0, len(s) - 1, separator))
        
        return pairs

    #---
    
    def get_key(self, dictObj: dict, pitchfork: object) -> object:
        """
        .. versionadded:: v0.1.1

        Returns the key of the given value in the dictionary.

        This method helps in reverse mapping from values to keys in the character dictionary.

        Args:
            dictObj (dict): The dictionary to search through.
            pitchfork (object): The value to search for in the dictionary.

        Returns:
            object: The key of the given value.

        Usage:
            .. code-block:: python

                key = VSNSL.get_key(VSNSL.letters, 101)
                print(key) # Returns: "a"
        """
        return next((key for key, value in dictObj.items() if value == pitchfork), None)

    #---
    
    def encodeData(self, data: str) -> str:
        """
        .. versionadded:: v0.1.1
            Was added to allow for encoding of data.

        Encodes the given data using the character mapping dictionary.

        This method converts strings into a secure numeric format based on the character mapping.

        Args:
            data (str): The data to encode.

        Returns:
            str: The encoded data as a string.
        
        Raises:
            ValueError: If no valid characters are found for encoding.
        """
        return self.core.encode_data(data)

    #---

    def encode(self, data: object) -> str:
        """An alternative of encodeData"""
        return self.encodeData(data)

    #---
    
    def decodeData(self, data: str) -> str:
        """
        .. versionadded:: v0.1.1
            Was added to allow for decoding of data.

        Decodes the given data using the character mapping dictionary.

        This method reverses the encoding process, converting numeric strings back to their original form.

        Args:
            data (str): The data to decode.

        Returns:
            str: The decoded data as a string.
        
        Raises:
            ValueError: If decryption fails due to data format error or too many unfound values.
        """
        return self.core.decode_data(data)

    #---

    def decode(self, data: object) -> str:
        """An alternative of decodeData"""
        return self.decodeData(data)

    #---
    
    def convertData(self, newEncryptionLock: int, data: str) -> str:
        """
        .. versionadded:: v0.0.1
            Was added to make converting data between encryption locks easier.

        Converts the data from the current encryption lock to the new encryption lock.

        This method facilitates the transition of data between different encryption locks.

        Args:
            newEncryptionLock (int): The new encryption lock.
            data (str): The data to convert.

        Returns:
            str: The converted data.

        Usage:
            .. code-block:: python

                convertedData = VSNSL.convertData(2, "101102103")
                print(convertedData) # Returns: "201202203"
        """
        self.logger.info(f"Converting data from {self.encryptionLock} to {newEncryptionLock}")

        try:
            return self._extracted_from_convertData_26(data, newEncryptionLock)
        except Exception as e:
            self.logger.exception("Exception during data conversion")
            raise e  # Raise the exception if any error occurs

    # TODO Rename this here and in `convertData`
    def _extracted_from_convertData_26(self, data, newEncryptionLock):
        oldEncryption = self.encryptionLock  # Store the current encryption lock
        oldData = self.decodeData(data)  # Decode the data with the current lock
        self.encryptionLock = newEncryptionLock  # Update to the new encryption lock
        convertedData = self.encodeData(oldData)  # Encode the data with the new lock
        self.encryptionLock = oldEncryption  # Restore the old encryption lock
        return convertedData  # Return the converted data

    #---
    
    def encodeBatch(self, data_list: list) -> list:
        """
        .. versionadded:: v0.1.2
            Was added to make encoding batches easier.

        .. note::
            Instances of None will be returned if an error occurs during encoding (If character isn't found in :attr:`self.charset.charset`).

            Example:
                .. code-block:: python

                    vsnsl = VSNSL(1)
                    decoded_list = vsnsl.encodeBatch(["abc", "def", "😁"])
                    encoded_list = vsnsl.encode_batch(encoded_list)
                    print(encoded_list) # returns: ["101102103", "104105106", None]

        .. caution::
            Encoding a large batch of data may cause significant performance issues.

        This method allows batch processing of multiple strings for encoding.

        Args:
            data_list (list): A list of strings to encode.

        Returns:
            list: A list of encoded strings.

        Usage:
            .. code-block:: python

                vsnsl = VSNSL(1)
                data_list = ["abc", "def", "ghi"]
                encoded_list = vsnsl.encode_batch(data_list)
                print(encoded_list) # returns: ["101102103", "104105106", "107108109"]
        """
        return self.batch.encode_batch(data_list)

    #---
    
    def decodeBatch(self, encoded_list: list) -> list:
        """
        .. versionadded:: v0.1.2
            Was added to make decoding batches easier.

        .. note::
            Instances of None will be returned if an error occurs during decoding.

            Example:
                .. code-block:: python

                    vsnsl = VSNSL(1)
                    encoded_list = ["101102103", "104105106", "107108205"]
                    decoded_list = vsnsl.decode_batch(encoded_list)
                    print(decoded_list) # returns: ["abc", "def", None]

        .. caution::
            Decoding a large batch of data may cause significant performance issues.

        This method allows batch processing of multiple encoded strings for decoding.

        Args:
            encoded_list (list): A list of encoded strings to decode.

        Returns:
            list: A list of decoded strings.

        Usage:
            .. code-block:: python

                vsnsl = VSNSL(1)
                encoded_list = ["101102103", "104105106", "107108109"]
                decoded_list = vsnsl.decode_batch(encoded_list)
                print(decoded_list) # returns: ["abc", "def", "ghi"]
        """
        return self.batch.decode_batch(encoded_list)

    #---
    
    def mEncode(self, locks: list, data: str) -> str:
        """
        .. versionadded:: v0.1.3
            Was added to allow encoding of data using multiple encryption locks.

        Encodes a string using a series of encryption locks in sequence.

        This method takes a list of encryption locks and encodes the provided string with each lock in the order they are given. The output of each encoding becomes the input for the next.

        Args:
            locks (list): A list of encryption locks to use for encoding.
            data (str): The string to encode.

        Returns:
            str: The final encoded string after applying all encryption locks.

        Usage:
            .. code-block:: python

                vsnsl = VSNSL(1)
                encoded_data = vsnsl.mEncode([2, 3], "abc")
                print(encoded_data)  # Encodes "abc" first with lock 2, then with lock 3.
        """
        return self.multilock.multi_encode(locks, data)

    #---
    
    def mDecode(self, locks: list, data: str) -> str:
        """
        .. versionadded:: v0.1.3
            Was added to allow decoding of data using multiple encryption locks.

        Decodes a string using a series of encryption locks in sequence.

        This method takes a list of encryption locks and decodes the provided string with each lock in the order they are given. The output of each decoding becomes the input for the next.

        Args:
            locks (list): A list of encryption locks to use for decoding.
            data (str): The string to decode.

        Returns:
            str: The final decoded string after applying all encryption locks.

        Usage:
            .. code-block:: python

                vsnsl = VSNSL(1)
                decoded_data = vsnsl.mDecode([1, 2], "387396399387396393387402381387396399387396393387402387")
                print(decoded_data)  # Decodes the string first with lock 2, then with lock 3.
        """
        return self.multilock.multi_decode(locks, data)

    @property
    def encryptionLock(self):
        return self.core.encryption_lock
    
    @encryptionLock.setter 
    def encryptionLock(self, value):
        self.core.encryption_lock = value if value != 0 else 1