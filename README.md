# VSNSL - A Simple Encoding and Decoding Library

VSNSL (stands for Very Simple Number Storage Language) is a Python library designed to encode and decode data using a character mapping dictionary. It provides a simple interface for transforming strings into encoded data and vice versa, using a specified encryption lock.

## Features

- **Encoding**: Convert strings into encoded data using a character mapping.
- **Decoding**: Revert encoded data back to its original string form.
- **Batch Processing**: Encode and decode lists of strings in batch.
- **Logging**: Comprehensive logging for tracking the encoding and decoding processes.

## Installation

To use VSNSL, clone the repository:

```bash
git clone https://github.com/CarterST1/VSNSL_LIB.git
cd VSNSL_LIB
```

## Usage

Here's a quick example of how to use the VSNSL library:

```python

from .VSNSL_LIB import VSNSL  # Use relative import if in the same package

vsnsl: VSNSL = VSNSL(1)

print(vsnsl.encodeData("abc"))
# Returns: "101102103"

print(vsnsl.decodeData("101102103"))
# Returns: "abc"

print(vsnsl.encodeBatch(["abc", "def", "ghi"]))
# Returns: ["101102103", "104105106", "107108109"]

print(vsnsl.decodeBatch(["101102103", "104105106", "107108109"]))
# Returns: ["abc", "def", "ghi"]

encryptedLocks = [1,2,3]
encrypted = vsnsl.mltEncode(encryptedLocks, "hi")
print(encrypted)
print(vsnsl.mltDecode(encryptedLocks, encrypted))
```

## Configuration

- **Charset File**: Ensure that the `charset.json` file is located in the `resources` directory. This file contains the character mapping used for encoding and decoding.
- **Logging**: Logs are stored in `resources/logs/activity.log`. You can adjust the logging level in the `VSNSL.py` file.

## Troubleshooting

- **Charset File Not Found**: Ensure that the `charset.json` file is correctly placed in the `resources` directory.
- **Decryption Errors**: If you encounter errors during decryption, check the encryption lock and ensure the data is not corrupted.

## Changelog

- **v0.1.1**: Initial release with basic encoding and decoding features.
- **v0.1.2**: Added batch processing methods for encoding and decoding lists of strings.
- **v0.1.3**: This update introduces mltEncode and mltDecode for streamlined multi-encoding and decoding on a single line, alongside improvements to data encoding/decoding processes to reduce errors.
- **v0.1.4**: This update will features major refactoring.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](license.md) file for details.

## Contact

For questions or support, please open an issue on the GitHub repository.
