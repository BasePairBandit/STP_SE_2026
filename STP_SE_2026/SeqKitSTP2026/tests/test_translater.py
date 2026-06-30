import pytest
import logging
from SeqKitSTP.modules.translater import translate

@pytest.fixture
def sample_rna():
    return "acguaugcggccuaugggugaaacccgggagagcugauag"
@pytest.fixture
def uppercase_rna():
    return "AUGGCUUAA"

def test_translate_normal_case(sample_rna):
    expected_RNA_sequence = "MRPMGETRES*"
    assert translate(sample_rna, "aug", "uga") == expected_RNA_sequence

def test_translate_default_case(sample_rna):
    expected_RNA_sequence = "MRPMGETRES*"
    assert translate(sample_rna,"","")== expected_RNA_sequence

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

def test_translate_wrong_stop_codon_case(caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        translate("augaugggg","aug","aaa")
    assert "Invalid stop codon entered" in caplog.text

def test_translate_more_than_one_stop_codon_case():
    expected_RNA_sequence = "MA*"
    assert translate("auggcuuaaggguag","","")== expected_RNA_sequence

def test_translate_start_codon_not_at_begining_case():
    expected_RNA_sequence = "MFG*"
    assert translate("cccauguuuggguaa","","")== expected_RNA_sequence

def test_translate_no_stop_codon_case(caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        translate("auggcuaaa","","")
    assert "Stop codon not found after start or invalid stop codon entered" in caplog.text

def test_translate_out_of_frame_stop_codon_case(caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        translate("augaguaaccc","","")
    assert "Stop codon not found after start or invalid stop codon entered" in caplog.text

def test_invalid_RNA_character_case(caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        translate("auggctuaa","","")
    assert "RNA input contains invalid characters" in caplog.text

def test_uppercase_RNA_case(uppercase_rna,caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        translate(uppercase_rna,"","")
    assert "RNA input contains uppercase characters" in caplog.text
