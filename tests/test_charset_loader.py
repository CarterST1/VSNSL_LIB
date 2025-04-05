import pytest
from pathlib import Path
from libraries.charset import Charset
from libraries.charset_loader import CharsetLoader

def test_load_charset_from_dir(tmp_path):
    # Create test charset files
    test_file = tmp_path / "test_charset.json"
    test_file.write_text('{"mapping": {"x": 100, "y": 200}}')
    
    charset = Charset()
    loader = CharsetLoader(charset)
    loader.load_from_directory(tmp_path)
    
    assert charset.charset == {'x': 200, 'y': 300}  # 100+100=200, 200+100=300

def test_load_invalid_charset_file(tmp_path):
    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid json}")
    
    charset = Charset()
    loader = CharsetLoader(charset)
    
    with pytest.raises(Exception):
        loader.load_from_directory(tmp_path) 