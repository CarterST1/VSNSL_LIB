import pytest
from pathlib import Path
from libraries.charset import Charset

CHARSET_PATH = Path(__file__).parent.parent / "libraries/resources/charsets/charset.json"
BUILT_CHARSET = Charset(); BUILT_CHARSET.load_charset(CHARSET_PATH); BUILT_CHARSET.priority = 2
BLANK_CHARSET = Charset()

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
