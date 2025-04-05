import pytest
from libraries.charset import Charset
from libraries.core_operations import CoreOperations
from libraries.batch_processor import BatchProcessor

@pytest.fixture
def batch_processor():
    charset = Charset()
    charset.charset = {'a': 101, 'b': 102, 'c': 103}
    core = CoreOperations(charset, 1)
    return BatchProcessor(core)

def test_batch_encode_success(batch_processor):
    results = batch_processor.encode_batch(["abc", "abc"])
    assert results == ["101102103", "101102103"]

def test_batch_encode_partial_failure(batch_processor):
    results = batch_processor.encode_batch(["abc", "invalid"])
    assert results == ["101102103", None]

def test_batch_decode_success(batch_processor):
    results = batch_processor.decode_batch(["101102103", "101102103"])
    assert results == ["abc", "abc"]

def test_batch_decode_partial_failure(batch_processor):
    results = batch_processor.decode_batch(["101102103", "999"])
    assert results == ["abc", None] 