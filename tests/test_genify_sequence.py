import pytest
import logging
from SeqKitSTP.modules.genify_sequence import genify_seq

def test_sequence_regular_case(monkeypatch): #normal case
    blocked_sequence = "aaaaa aaaaa aaaaa aaaaa aaaaa aaaaa aaaaa aaaaa aaa"
    expected = '        1 aaaaa aaaaa aaaaa aaaaa aaaaa\n       26 aaaaa aaaaa aaaaa aaa'
    monkeypatch.setattr('builtins.input',lambda x:"5")#the test cannot get user input so it hangs, but using monkeypatch makes input return 5
    assert genify_seq(blocked_sequence) == expected

def test_blocked_sequence_empty(caplog): #if empty dna_sequence
    blocked_sequence =""
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        genify_seq(blocked_sequence)
    assert "Block size must be greater than 0" in caplog.text

def test_zero_gen_block_size(monkeypatch,caplog): #if a gen_block_size less than or equal to zero is entered
    blocked_sequence = "aaaa aaaa"
    monkeypatch.setattr('builtins.input',lambda x:"0")
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        genify_seq(blocked_sequence)
    assert "Block size must not be zero or negative" in caplog.text