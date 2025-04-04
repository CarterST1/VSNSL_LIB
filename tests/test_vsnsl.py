import pytest
from libraries.VSNSL_LIB import VSNSL

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

def test_decode_data_abc():
    vsnsl = VSNSL(1)
    data = vsnsl.decodeData("101102103")
    assert data == "abc"