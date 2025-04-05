import pytest
from libraries.charset import Charset
from libraries.core_operations import CoreOperations
from libraries.multi_lock import MultiLockProcessor

@pytest.fixture
def multi_lock_processor():
    charset = Charset()
    charset.charset = {'a': 1, 'b': 2, 'c': 3}
    core = CoreOperations(charset, 1)
    return MultiLockProcessor(core)

def test_multi_encode(multi_lock_processor):
    result = multi_lock_processor.multi_encode([2, 3], "abc")
    assert result == "246"  # (1*2=2, 2*2=4, 3*2=6) then (2*3=6, 4*3=12, 6*3=18) → "61218"

def test_multi_decode(multi_lock_processor):
    encoded = "61218"  # After locks [2,3]
    result = multi_lock_processor.multi_decode([2, 3], encoded)
    assert result == "abc" 