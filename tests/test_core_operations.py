import pytest
from libraries.charset import Charset
from libraries.core_operations import CoreOperations

@pytest.fixture
def base_charset():
    charset = Charset()
    charset.charset = {'a': 101, 'b': 102, 'c': 103}
    return charset

def test_core_operations_init(base_charset):
    core = CoreOperations(base_charset, 1)
    assert core.encryption_lock == 1
    assert core.charset.charset['a'] == 101

def test_encode_data_success(base_charset):
    core = CoreOperations(base_charset, 1)
    assert core.encode_data("abc") == "101102103"

def test_encode_data_invalid_char(base_charset):
    core = CoreOperations(base_charset, 1)
    with pytest.raises(ValueError):
        core.encode_data("x")

def test_decode_data_success(base_charset):
    core = CoreOperations(base_charset, 1)
    assert core.decode_data("101102103") == "abc"

def test_decode_data_invalid_pair(base_charset):
    core = CoreOperations(base_charset, 1)
    with pytest.raises(ValueError):
        core.decode_data("999") 