import pytest
from libraries.VSNSL_LIB import VSNSL

TEST_ENCODED_DATA = "101102103"

# Constants for assertions
EXPECTED_ENCODED_DATA = "101102103"
EXPECTED_CONVERTED_DATA = "202204206"  # Assuming the encoding with lock 2 gives this result
EXPECTED_BATCH_ENCODED_LIST = [EXPECTED_ENCODED_DATA, EXPECTED_ENCODED_DATA]  # Assuming these are the expected results
EXPECTED_BATCH_DECODED_LIST = ["abc", "abc"]  # Assuming these are the expected results
EXPECTED_MLT_ENCODED_DATA = "387381387387381393387381399"  # Replace with the expected result after encoding

def test_encryptionLock_default_value():
    vsnsl = VSNSL(0)
    assert vsnsl.encryptionLock != 0

def test_encryptionLock_set_to_1_on_zero_input():
    vsnsl = VSNSL(0)
    assert vsnsl.encryptionLock == 1

def test_encode_data_abc():
    vsnsl = VSNSL(1)
    data = vsnsl.encodeData("abc")
    assert data == EXPECTED_ENCODED_DATA

def test_decode_data_abc():
    vsnsl = VSNSL(1)
    data = vsnsl.decodeData("101102103")
    assert data == "abc"

# New tests for additional functions
def test_convert_data():
    vsnsl = VSNSL(1)
    converted_data = vsnsl.convertData(2, TEST_ENCODED_DATA)
    assert converted_data == EXPECTED_CONVERTED_DATA

def test_encode_batch():
    vsnsl = VSNSL(1)
    data_list = ["abc", "abc"]
    encoded_list = vsnsl.encodeBatch(data_list)
    assert encoded_list == EXPECTED_BATCH_ENCODED_LIST

def test_decode_batch():
    vsnsl = VSNSL(1)
    encoded_list = EXPECTED_BATCH_ENCODED_LIST
    decoded_list = vsnsl.decodeBatch(encoded_list)
    assert decoded_list == EXPECTED_BATCH_DECODED_LIST

def test_mlt_encode():
    vsnsl = VSNSL(1)
    encoded_data = vsnsl.mltEncode([2, 3], "abc")
    assert encoded_data == EXPECTED_MLT_ENCODED_DATA

def test_mlt_decode():
    vsnsl = VSNSL(1)
    decoded_data = vsnsl.mltDecode([2, 3], "387381387387381393387381399")
    assert decoded_data == "abc"  # Replace with the expected original value

def test_alt_encode_data_abc():
    vsnsl = VSNSL(1)
    data = vsnsl.encode("abc")
    assert data == EXPECTED_ENCODED_DATA

def test_alt_decode_data_abc():
    vsnsl = VSNSL(1)
    data = vsnsl.decode("101102103")
    assert data == "abc"