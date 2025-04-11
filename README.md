# VSNSL - A Simple Encoding and Decoding Library

VSNSL (Very Simple Number Storage Language) is a Python library for encoding and decoding data using a character mapping dictionary. It provides an intuitive interface for transforming strings into encoded data and vice versa, with support for encryption locks and batch processing.

## Features

- **Encoding**: Convert strings into encoded data using a character mapping.
- **Decoding**: Revert encoded data back to its original string form.
- **Batch Processing**: Encode and decode lists of strings in batch.
- **Multi-Lock Encoding**: Support for multi-lock encoding and decoding for added security.
- **Logging**: Comprehensive logging for tracking encoding and decoding processes.

## Installation

To get started with VSNSL, clone the repository and navigate to the project directory:

```bash
git clone https://github.com/CarterST1/VSNSL_LIB.git
cd VSNSL_LIB
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Here’s a quick example of how to use the VSNSL library:

```python
from libraries.VSNSL_LIB import VSNSL

# Initialize the VSNSL object with an encryption lock
vsnsl = VSNSL(1)

# Encoding and decoding a single string
encoded = vsnsl.encodeData("abc")
print(encoded)  # Output: "101102103"

decoded = vsnsl.decodeData("101102103")
print(decoded)  # Output: "abc"

# Batch encoding and decoding
encoded_batch = vsnsl.encodeBatch(["abc", "def", "ghi"])
print(encoded_batch)  # Output: ["101102103", "104105106", "107108109"]

decoded_batch = vsnsl.decodeBatch(["101102103", "104105106", "107108109"])
print(decoded_batch)  # Output: ["abc", "def", "ghi"]

# Multi-lock encoding and decoding
encryption_locks = [1, 2, 3]
mlt_encoded = vsnsl.mEncode(encryption_locks, "hi")
print(mlt_encoded)

mlt_decoded = vsnsl.mDecode(encryption_locks, mlt_encoded)
print(mlt_decoded)  # Output: "hi"
```

## Configuration

- **Charset File**: Ensure the `charset.json` file is located in the `resources/charsets` directory. This file contains the character mapping used for encoding and decoding.
- **Logging**: Logs are stored in `resources/logs/activity.log`. You can adjust the logging level in the `VSNSL_LIB.py` file.

## Troubleshooting

- **Charset File Not Found**: Verify that the `charset.json` file is correctly placed in the `resources/charsets` directory.
- **Decryption Errors**: Ensure the encryption lock is correct and the data is not corrupted.

## Changelog

- **v0.1.1**: Initial release with basic encoding and decoding features.
- **v0.1.2**: Added batch processing methods for encoding and decoding lists of strings.
- **v0.1.3**: Introduced `mEncode` and `mDecode` for streamlined multi-lock encoding and decoding.
- **v0.1.4**: Major refactoring for improved performance and maintainability.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](license.md) file for details.

## Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/CarterST1/VSNSL_LIB).
