import pytest
import logging
from SeqKitSTP.modules.translater import translate

@pytest.fixture
def sample_rna():
    return "acguaugcggccuaugggugaaacccgggagagcugauag"

def test_translate_normal_case(sample_rna):
    expected_RNA_sequence = "MRPMGETRES*"
    assert translate(sample_rna, "aug", "uga") == expected_RNA_sequence

def test_translate_empty_case(caplog):
    rna_sequence = ""
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        translate(rna_sequence, "aug", "uga")
    assert "RNA input is empty" in caplog.text

def test_translate_uppercase_case(caplog):
    rna_sequence = "Acgaugauguga"
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        translate(rna_sequence,"aug","uga")
    assert "RNA input contains uppercase characters" in caplog.text

def test_translate_wrong_stop_codon_case(sample_rna, caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        translate(sample_rna,"aug","aaa")
    assert "Stop codon not found after start or invalid stop codon entered" in caplog.text
    