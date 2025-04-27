from pathlib import Path
from libraries.charset import Charset

CHARSET_PATH = Path(__file__).parent.parent / "libraries/resources/charsets/charset.json"
BUILT_CHARSET = Charset(); BUILT_CHARSET.load_charset(CHARSET_PATH); BUILT_CHARSET.priority = 2
BLANK_CHARSET = Charset()
CHARSET_DICT = {
    "author": "CarterST1",
    "timestamp": 0,
    "mapping": {
        "key1": 0,
        "key2": 1,
        "key3": 2
    }
}
CHARSET_DICT_CONVERTED = {
    "author": "CarterST1",
    "timestamp": 0,
    "mapping": {
        "key1": 100,
        "key2": 101,
        "key3": 102
    }
}

def test_charset_default_values():
    assert BLANK_CHARSET.author == ""
    assert BLANK_CHARSET.timestamp == 0
    assert BLANK_CHARSET.charset == {}
    assert BLANK_CHARSET.priority == 1

def test_charset_not_default():
    assert BLANK_CHARSET.author != BUILT_CHARSET.author
    assert BLANK_CHARSET.timestamp != BUILT_CHARSET.timestamp
    assert BLANK_CHARSET.charset != BUILT_CHARSET.charset
    assert BLANK_CHARSET.priority != BUILT_CHARSET.priority

def test_charset_addkey_invalid_type():
    charset = Charset()
    assert charset.addKey(123) == 0
    assert "123" not in charset.get_charset()

def test_charset_get_max_value_empty():
    charset = Charset()
    assert charset._get_max_value() == -1

def test_charset_addkey_valid():
    charset = Charset()
    assert charset.addKey("testKey") == 1
    assert "testKey" in charset.get_charset()
    assert charset.get_charset()["testKey"] == 0

def test_charset_rmvkey_valid():
    charset = Charset()
    charset.addKey("testKey")
    assert charset.rmvKey("testKey") == 1
    assert "testKey" not in charset.get_charset()

def test_charset_load_charset_dict():
    charset = Charset()
    charset.load_charset(CHARSET_DICT)
    assert charset.get_charset() == CHARSET_DICT_CONVERTED['mapping']