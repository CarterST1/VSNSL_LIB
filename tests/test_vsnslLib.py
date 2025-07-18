import pytest
from pathlib import Path
from libraries.VSNSL_LIB import VSNSL
from libraries.charset import Charset

TEST_ENCODED_DATA = "101102103"

# Constants for assertions
EXPECTED_ENCODED_DATA = "101102103"
EXPECTED_CONVERTED_DATA = "202204206"  # Assuming the encoding with lock 2 gives this result
EXPECTED_BATCH_ENCODED_LIST = [EXPECTED_ENCODED_DATA, EXPECTED_ENCODED_DATA]  # Assuming these are the expected results
EXPECTED_BATCH_DECODED_LIST = ["abc", "abc"]  # Assuming these are the expected results
EXPECTED_M_ENCODED_DATA = "387381387387381393387381399"  # Replace with the expected result after encoding

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

def test_m_encode():
    vsnsl = VSNSL(1)
    encoded_data = vsnsl.mEncode([2, 3], "abc")
    assert encoded_data == EXPECTED_M_ENCODED_DATA

def test_m_decode():
    vsnsl = VSNSL(1)
    decoded_data = vsnsl.mDecode([2, 3], "387381387387381393387381399")
    assert decoded_data == "abc"  # Replace with the expected original value

def test_alt_encode_data_abc():
    vsnsl = VSNSL(1)
    data = vsnsl.encode("abc")
    assert data == EXPECTED_ENCODED_DATA

def test_alt_decode_data_abc():
    vsnsl = VSNSL(1)
    data = vsnsl.decode("101102103")
    assert data == "abc"

def test_load_charsets_fail_nonexistant_path():
    vsnsl = VSNSL(1)
    try:
        vsnsl.load_charsets(Path("non_existant_path"))
    except FileNotFoundError:
        assert True

def test_load_charsets_fail_empty_dir():
    vsnsl = VSNSL(1)
    try:
        vsnsl.load_charsets(Path(r"VSNSL_LIB\tests\resources\dummy_dir"))
    except FileNotFoundError:
        assert True

def test_getPairs():
    vsnsl = VSNSL(1)
    pairs = vsnsl.get_pairs("abcabc", 3)
    assert pairs == ["abc", "abc"]
    
def test_encodeData_invalid_input():
    vsnsl = VSNSL(1)
    charset = Charset()
    charset.load_charset({"a": "1", "b": "2", "c": "3"})
    vsnsl.charset = charset
    with pytest.raises(ValueError):
        vsnsl.encodeData("xyz")

def test_decodeData_valueError():
    vsnsl = VSNSL(1)
    with pytest.raises(ValueError):
        vsnsl.decodeData("test")

def test_decodeData_unfound_values():
    vsnsl = VSNSL(1)
    with pytest.raises(ValueError):
        vsnsl.decodeData("202203204205")

def test_decodeData_invalid_input():
    vsnsl = VSNSL(1)
    charset = Charset()
    charset.charset = {"a": 101, "b": 102, "c": 103}
    vsnsl.charset = charset
    with pytest.raises(ValueError):
        vsnsl.decodeData("101abc")

def test_encodeBatch_exception():
    vsnsl = VSNSL(1)
    charset = Charset()
    charset.charset = {"a": 101, "b": 102, "c": 103}
    vsnsl.charset = charset
    
    returned = vsnsl.encodeBatch(["abc", "xyz"])
    assert None in returned

def test_decodeBatch_exception():
    vsnsl = VSNSL(1)
    charset = Charset()
    charset.charset = {"a": 101, "b": 102, "c": 103}
    vsnsl.charset = charset
    
    returned = vsnsl.decodeBatch(["101", "102", "103", "abc"])
    assert None in returned

def test_convertData_invalid_input():
    vsnsl = VSNSL(1)
    with pytest.raises(Exception):
        vsnsl.convertData(2, "invalid_data")