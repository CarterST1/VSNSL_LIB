# NOSL - A Simple Encoding and Decoding Library

NOSL is a Python library designed to encode and decode data using a character mapping dictionary. It provides a simple interface for transforming strings into encoded data and vice versa, using a specified encryption lock.

## Features

- **Encoding**: Convert strings into encoded data using a character mapping.
- **Decoding**: Revert encoded data back to its original string form.
- **Logging**: Comprehensive logging for tracking the encoding and decoding processes.

## Installation

To use NOSL, clone the repository and ensure you have the necessary dependencies installed.

```bash
git clone https://github.com/yourusername/nosl.git
cd nosl
pip install -r requirements.txt
```

## Usage

Here's a quick example of how to use the NOSL library:

```python
from NOSL import NOSL

# Initialize the NOSL class with an encryption lock
nosl = NOSL(encryptionLock=12345)

# Encode a string
encoded_data = nosl.encodeData("Hello, World!")
print(f"Encoded: {encoded_data}")

# Decode the encoded string
decoded_data = nosl.decodeData(encoded_data)
print(f"Decoded: {decoded_data}")
```

## Configuration

- **Charset File**: Ensure that the `charset.json` file is located in the `resources` directory. This file contains the character mapping used for encoding and decoding.
- **Logging**: Logs are stored in `resources/logs/activity.log`. You can adjust the logging level in the `NOSL.py` file.

## Troubleshooting

- **Charset File Not Found**: Ensure that the `charset.json` file is correctly placed in the `resources` directory.
- **Decryption Errors**: If you encounter errors during decryption, check the encryption lock and ensure the data is not corrupted.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue on the GitHub repository.