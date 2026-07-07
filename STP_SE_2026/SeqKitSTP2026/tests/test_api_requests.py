import pytest
import logging
from SeqKitSTP.utils.api_requests import *
from unittest.mock import Mock

def test_validate_refseq_transcript_normal(): #normal case
    SequenceAPI._validate_refseq_transcript("NM_000546.5")

def test_validate_refseq_transcript_wrong_prefix(): #missing prefix case
    with pytest.raises(TranscriptIdError):
        SequenceAPI._validate_refseq_transcript("JK_000546.5")

def test_validate_refseq_transcript_missing_prefix(): #missing version case
    with pytest.raises(TranscriptIdError):
        SequenceAPI._validate_refseq_transcript("JK_000546")

def test_validate_ensembl_transcript_normal(): #normal case
    SequenceAPI._validate_ensembl_transcript("ENST_000546.5")

def test_validate_ensembl_transcript_missing_prefix(): #missing prefix case
    with pytest.raises(TranscriptIdError):
        SequenceAPI._validate_ensembl_transcript("000546.5")

def test_validate_ensembl_transcript_wrong_prefix(): #wrong prefix case
    with pytest.raises(TranscriptIdError):
        SequenceAPI._validate_ensembl_transcript("JKJK_000546.5")


def test_structure_ensembl_transcript(): #normal case
    api = SequenceAPI()
    record = {
        "metadata": {
            "id": "ENST00000367770",
            "display_name": "SCYL3",
            "Translation": {
                "start": 100,
                "end": 500,
            },
        },
        "sequence": {
            "seq": "ATGC"
        }
    }
    result = api.structure_ensembl_transcript(record)
    assert result["id"] == "ENST00000367770"
    assert result["name"] == "SCYL3"
    assert result["sequence"] == "ATGC"
    assert result["cds_start"] == 100
    assert result["cds_end"] == 500


def test_extract_mane():#mocking a response because I just want to test the function and not necessarily use a live API call that could be offline.
    api = SequenceAPI()
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "id": "ENST00000367770",
            "tag": ["MANE_Select"]
        }
    ]
    api._get = Mock(return_value=mock_response)
    record = {
        "metadata": {
            "Parent": "ENSG000001"
        }
    }
    result = api.extract_mane(record)
    assert result == "ENST00000367770"
