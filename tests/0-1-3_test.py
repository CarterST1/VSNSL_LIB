import pytest
from libraries.VSNSL_LIB import VSNSL
from libraries.charset import Charset

def test_encryptionLock_default_value():
    vsnsl = VSNSL(0)
    assert vsnsl.encryptionLock != 0

def test_encryptionLock_set_to_1_on_zero_input():
    vsnsl = VSNSL(0)
    assert vsnsl.encryptionLock == 1

def test_encode_data_abc():
    vsnsl = VSNSL(1)
    data = vsnsl.encodeData("abc")
    assert data == "101102103"

def test_default_charset_author():
    charset = Charset()
    assert charset.author == ""

def test_default_charset_timestamp():
    charset = Charset()
    assert charset.timestamp == 0

def test_default_charset_charset():
    charset = Charset()
    assert charset.charset == {}

def test_default_charset_priority():
    charset = Charset()
    assert charset.priority == 1