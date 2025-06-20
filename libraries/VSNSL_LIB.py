import json
import logging
from pathlib import Path
import sys
from typing import List, Optional
from .charset import Charset  # Ensure Charset is imported
from .utilities.logger import vsnsl_logger as logger

# Configure logging
logging.basicConfig(
    filename=f'{Path(__file__).parent}/resources/logs/activity.log',
    level=logging.INFO,  # This should already be set to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding="utf-8"
)

BASE_CHARSET = Charset()

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

    def __init__(self, encryptionLock: int, charset: Optional[Charset] = None):
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
        
        self.charset = charset if charset else BASE_CHARSET
        self.encryptionLock = encryptionLock if encryptionLock != 0 else 1  # Set the encryption lock
        logger.debug(f"Encryption lock set to: {self.encryptionLock}")

        self.MAX_BATCH_SIZE = 1000  # Maximum batch size for encoding/decoding
        logger.debug(f"Setting maximum batch size to: {self.MAX_BATCH_SIZE}")

        # Load character mappings from charset files
        self.load_charsets()

    def load_charsets(self, charsetPath: Optional[Path] = None):
        """
        Load character mappings from charset files into the Charset instance.

        Args:
            charsetPath (Path, optional): The path to the charset directory. If not provided, 
                                          the default path will be used.
        """
        if charsetPath is None:
            # Use the default path if no path is provided
            charsetPath = Path(f'{Path(__file__).parent}/resources/charsets')

        if not charsetPath.exists() or not charsetPath.is_dir():
            logger.error("Charset files not found.")
            raise FileNotFoundError("Charset files not found. Make sure you installed it correctly and run the script again.")

        charsetPaths = list(charsetPath.rglob('*'))
        if not charsetPaths:
            logger.error("No charset files found in the directory.")
            raise FileNotFoundError("No charset files found in the directory.")

        for path in charsetPaths:
            self.charset.load_charset(path)

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
        
        Raises:
            ValueError: If no valid characters are found for encoding.
        """
        logger.debug(f"Starting encoding of data: {data}")
        if isinstance(data, str):  # Check if the data is a string
            returnText = ''  # Initialize the return text
            for letter in data:
                try:
                    # Use the Charset instance to encode each letter
                    returnText += str(self.charset.charset[letter])  # Encode each letter
                    logger.debug(f"Encoded {letter} to {self.charset.charset[letter]}")
                except KeyError:
                    logger.warning(f"Character '{letter}' not found in mapping.")  # Log a warning if the character is not found
                    
            if returnText == '':
                logger.error("No valid characters found for encoding.")
                raise ValueError("No valid characters found for encoding.")  # Raise an error if no valid characters were found
                
            # Ensure the encoded result is correctly adjusted by the encryption lock
            encoded_result = str(int(returnText) * self.encryptionLock)  # Change to multiplication
            logger.info("Encoding completed successfully")
            return encoded_result  # Return the encoded result
        else:
            logger.error("Input data must be a string.")
            raise ValueError("Input data must be a string.")  # Raise an error if the input is not a string

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
        returnText = ''  # Initialize the return text

        logger.info(f"Starting decoding process for data: {data}")

        unfound_count = 0  # Counter for unfound values
        if isinstance(data, str):  # Check if the data is a string
            try:
                multiplied_data = str(int(data) // self.encryptionLock)  # Change to division
                logger.debug(f"Multiplied data: {multiplied_data}")
                pair_length = 3
                pairs = [multiplied_data[i:i+pair_length] for i in range(0, len(multiplied_data), pair_length)]  # Create pairs
                logger.debug(f"Pairs: {pairs}")

                for item in pairs:
                    key = self.get_key(self.charset.charset, int(item))
                    if key is not None:
                        returnText += str(key)  # Append the decoded character to returnText
                        logger.debug(f"Decoded {item} to {key}")
                    else:
                        unfound_count += 1  # Increment unfound count if key is None
                        logger.warning(f"Value {item} not found in character mapping.")

            except ValueError as e:
                logger.error(f"Error during decoding process: {e}")
                raise ValueError("Decryption failed due to data format or conversion error.") from e

            threshold = 2  # Set a threshold for the number of unfound values

            if unfound_count > threshold:
                logger.error(f"Too many unfound values ({unfound_count}). Possible issues: incorrect encryption lock, data corruption, or charset mismatch.")
                raise ValueError("Decryption failed due to too many unfound values. Please check the encryption lock.")

        logger.info("Successfully decoded data.")
        return returnText  # Return the decoded text

    #---

    def decode(self, data: object) -> str:
        """An alternative of decodeData"""
        if not isinstance(data, str):
            raise TypeError("The 'data' parameter must be of type 'str'.")
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
        logger.info(f"Converting data from {self.encryptionLock} to {newEncryptionLock}")

        try:
            return self._extracted_from_convertData_26(data, newEncryptionLock)
        except Exception as e:
            logger.error("Exception during data conversion")
            raise e  # Raise the exception if any error occurs

    # TODO Rename this here and in `convertData`
    def _extracted_from_convertData_26(self, data, newEncryptionLock):
        oldEncryption = self.encryptionLock 
        oldData = self.decodeData(data)
        self.encryptionLock = newEncryptionLock 
        convertedData = self.encodeData(oldData)
        self.encryptionLock = oldEncryption
        return convertedData

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
        encoded_list = []  # Initialize a list to hold encoded results
        
        if len(data_list) > self.MAX_BATCH_SIZE:
            logger.error(f"Batch size {len(data_list)} exceeds maximum allowed size {self.MAX_BATCH_SIZE}. Processing canceled.")
            return []

        for data in data_list:
            try:
                encoded_list.append(self.encodeData(data))  # Encode each data item and append to the list
            except Exception as e:
                logger.error(f"Failed to encode data: {data}. Error: {e}")
                encoded_list.append(None)  # Append None if encoding fails
                
        return encoded_list  # Return the list of encoded results

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
        decoded_list = []  # Initialize a list to hold decoded results

        if len(encoded_list) > self.MAX_BATCH_SIZE:
            logger.error(f"Batch size {len(encoded_list)} exceeds maximum allowed size {self.MAX_BATCH_SIZE}. Processing canceled.")
            return []
        
        for encoded in encoded_list:
            try:
                decoded_list.append(self.decodeData(encoded))  # Decode each encoded item and append to the list
            except Exception as e:
                logger.error(f"Failed to decode data: {encoded}. Error: {e}")
                decoded_list.append(None)  # Append None if decoding fails
                
        return decoded_list  # Return the list of decoded results

    #---
    
    def mEncode(self, encryptionLocks: List[int], stringToEncode: str):
        """
        .. versionadded:: v0.1.3
            Was added to allow encoding of data using multiple encryption locks.

        Encodes a string using a series of encryption locks in sequence.

        This method takes a list of encryption locks and encodes the provided string with each lock in the order they are given. The output of each encoding becomes the input for the next.

        Args:
            encryptionLocks (List[int]): A list of encryption locks to use for encoding.
            stringToEncode (str): The string to encode.

        Returns:
            str: The final encoded string after applying all encryption locks.

        Usage:
            .. code-block:: python

                vsnsl = VSNSL(1)
                encoded_data = vsnsl.mEncode([2, 3], "abc")
                print(encoded_data)  # Encodes "abc" first with lock 2, then with lock 3.
        """
        firstEncryptionLock = self.encryptionLock  # Store the initial encryption lock
        data = stringToEncode  # Set the initial data to encode
        
        for item in encryptionLocks:
            self.encryptionLock = item  # Update to the current encryption lock
            encoded_value = self.encodeData(data)  # Encode the data
            data = encoded_value  # Update data to the newly encoded value
            
        self.encryptionLock = firstEncryptionLock  # Restore the original encryption lock
        return data  # Return the final encoded data

    #---
    
    def mDecode(self, encryptionLocks: List[int], stringToDecode: str):
        """
        .. versionadded:: v0.1.3
            Was added to allow decoding of data using multiple encryption locks.

        Decodes a string using a series of encryption locks in sequence.

        This method takes a list of encryption locks and decodes the provided string with each lock in the order they are given. The output of each decoding becomes the input for the next.

        Args:
            encryptionLocks (List[int]): A list of encryption locks to use for decoding.
            stringToDecode (str): The string to decode.

        Returns:
            str: The final decoded string after applying all encryption locks.

        Usage:
            .. code-block:: python

                vsnsl = VSNSL(1)
                decoded_data = vsnsl.mDecode([1, 2], "387396399387396393387402381387396399387396393387402387")
                print(decoded_data)  # Decodes the string first with lock 2, then with lock 3.
        """
        firstEncryptionLock = self.encryptionLock  # Store the initial encryption lock
        data = stringToDecode  # Set the initial data to decode
        
        encryptionLocks.reverse()  # Reverse the list in place for decoding
        
        for item in encryptionLocks:  # Iterate over the reversed list
            self.encryptionLock = item  # Update to the current encryption lock
            decoded_value = self.decodeData(data)  # Decode the data
            data = decoded_value  # Update data to the newly decoded value
            
        self.encryptionLock = firstEncryptionLock  # Restore the original encryption lock
        return data  # Return the final decoded data