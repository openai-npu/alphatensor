"""
test_verify.py

Unit tests for evaluation.verify.
"""

import pytest
from evaluation.verify import verify_triples

def test_empty_triples():
    assert not verify_triples([])

def test_valid_triples():
    # TODO: Add a valid set of triples for 4x4 matmul
    pass
