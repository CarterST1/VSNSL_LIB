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
    """
    VSNSL class for encoding and decoding data using a character mapping dictionary.

    .. versionadded:: v0.1.1

    This class was developed for a science fair project, and it offers advantages such as extreme security.

    Attributes:
        letters (dict): A dictionary mapping characters to numbers.
        encryptionLock (int): The encryption lock to use for encoding and decoding.

    .. literalinclude:: example.py
    """

    def __init__(self, encryptionLock: int):
        """
        .. versionadded:: v0.1.1

        Initializes the VSNSL class with the given encryption lock.

        This constructor sets up the character mapping and encryption lock for encoding and decoding operations.

        Args:
            encryptionLock (int): The encryption lock to use for encoding and decoding.
        
        Usage:
            .. code-block:: python

                vsnsl = VSNSL(1)
        """
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

        self.charset_offset = 100
        logger.info(f"Charset offset set to: {self.charset_offset}")

        for char, num in self.letters.items():
            self.letters[char] = int(num) + self.charset_offset
        logger.info("Character mapping initialized.")

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
        pairs = []
        for i in range(0, len(s) - 1, separator):
            pairs.append(s[i:i+separator])
        return pairs

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
        for key, value in dictObj.items():
            if value == pitchfork:
                return key
        return None

    def encodeData(self, data: object) -> str:
        """
        .. versionadded:: v0.1.1
            Was added to allow for encoding of data.

        Encodes the given data using the character mapping dictionary.

        This method converts strings into a secure numeric format based on the character mapping.

        Args:
            data (object): The data to encode.

        Returns:
            str: The encoded data as a string.
        
        Usage:
            .. code-block:: python

                encodedData = VSNSL.encodeData("abc")
                print(encodedData) # Returns: "101102103"
        """
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
        """
        .. versionadded:: v0.1.1
            Was added to allow for decoding of data.

        Decodes the given data using the character mapping dictionary.

        This method reverses the encoding process, converting numeric strings back to their original form.

        Args:
            data (str): The data to decode.

        Returns:
            str: The decoded data as a string.
        
        Usage:
            .. code-block:: python

                decodedData = VSNSL.decodeData("101102103")
                print(decodedData) # Returns: "abc"
        """
        returnText = ''
        unfound_count = 0
        threshold = 2  # Set a threshold for the number of unfound values

        logger.info(f"Starting decoding process for data: {data}")

        if isinstance(data, str):
            try:
                multiplied_data = str(int(data) * self.encryptionLock)
                logger.debug(f"Multiplied data: {multiplied_data}")
                pair_length = len(str(self.charset_offset))
                pairs = []
                for i in range(0, len(multiplied_data), pair_length):
                    pairs.append(multiplied_data[i:i+pair_length])
                logger.debug(f"Pairs: {pairs}")
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
                raise ValueError("Decryption failed due to too many unfound values. Please check the encryption lock.")

        if unfound_count > 0:
            logger.warning(f"{unfound_count} values not found in character mapping. This may indicate an incorrect encryption lock.")

        logger.info("Successfully decoded data.")
        return returnText
    
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
        logger.info(f"Converting data from {self.encryptionLock} to {newEncryptionLock}")
        try:
            oldEncryption = self.encryptionLock
            oldData = self.decodeData(data)
            self.encryptionLock = newEncryptionLock
            convertedData = self.encodeData(oldData)
            self.encryptionLock = oldEncryption
            return convertedData
        except Exception as e:
            logger.exception("Exception during data conversion")
            raise e
        
    def encodeBatch(self, data_list: list) -> list:
        """
        .. versionadded:: v0.1.2
            Was added to make encoding batches easier.

        .. note::
            Instances of None will be returned if an error occurs during encoding (If character isn't found in :attr:`self.letters`).

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
        encoded_list = []
        for data in data_list:
            try:
                encoded_list.append(self.encodeData(data))
            except Exception as e:
                logger.error(f"Failed to encode data: {data}. Error: {e}")
                encoded_list.append(None)  # Append None or handle the error as needed
        return encoded_list

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
        decoded_list = []
        for encoded in encoded_list:
            try:
                decoded_list.append(self.decodeData(encoded))
            except Exception as e:
                logger.error(f"Failed to decode data: {encoded}. Error: {e}")
                decoded_list.append(None)  # Append None or handle the error as needed
        return decoded_list
        
    

