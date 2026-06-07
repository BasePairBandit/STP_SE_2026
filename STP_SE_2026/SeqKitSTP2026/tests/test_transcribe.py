import pytest
import logging
from SeqKitSTP.modules.transcriber import transcribe

def test_transcribe_normal_case():
    dna_sequence = "ATCG"
    expected_RNA_sequence = "aucg"
    assert transcribe(dna_sequence) == expected_RNA_sequence

def test_transcribe_illegal_character_letter(caplog):
    dna_sequence = "SATCG"
    caplog.set_level(logging.ERROR)
    with pytest.raises(TypeError):
        transcribe(dna_sequence)
    assert "DNA input contains invalid characters" in caplog.text

def test_transcribe_empty_case(caplog):
    dna_sequence = ""
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        transcribe(dna_sequence)
    assert "User input is empty" in caplog.text

def test_transcribe_space_case():
    dna_sequence = "AC GT"
    expected_RNA_sequence = "acgu"
    assert transcribe(dna_sequence)==expected_RNA_sequence