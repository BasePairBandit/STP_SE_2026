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

def test_fetch_hgnc_gene_via_name_and_refseq_wrong_MANE_ID():#mane select doesnt pass validation because it doesn't start with NM or NR).
    api = SequenceAPI()
    mock_hgnc_response = Mock()
    mock_hgnc_response.json.return_value = {
        "response":{
            "docs":[
                {
                    "hgnc_id":"HGNC:1234",
                    "symbol":"Test",
                    "mane_select":[
                        "ENST000001234.5",
                    ]
                }
            ]
        }
    }
    api._get = Mock(return_value=mock_hgnc_response)
    with pytest.raises(
        TranscriptIdError,
        match = "No MANE select found",
    ):
        api.fetch_hgnc_gene_via_name_and_refseq(
            "Test",
            ""
        )

def test_fetch_hgnc_gene_via_name_and_refseq_correct_MANE_ID():
    api = SequenceAPI()
    mock_hgnc_response = Mock()
    mock_hgnc_response.json.return_value = {
        "response":{
            "docs":[
                {
                    "hgnc_id":"HGNC:1234",
                    "symbol":"Test",
                    "mane_select":[
                        "NM_001234.5",
                    ],
                    "transcript_id":"1234.5",
                    "transcript_sequence":"ACTG",
                    "cds_start":"1",
                    "cds_end":"4",
                }
            ]
        }
    }
    mock_genbank_record = {
                "GBSeq_accession-version": "NM_001234.5",
                "GBSeq_sequence": "ACTG",
    }
    api._get = Mock(return_value=mock_hgnc_response)
    api.fetch_genbank_transcript = Mock(
        return_value=mock_genbank_record
    )
    result = api.fetch_hgnc_gene_via_name_and_refseq(
        "Test",
        "",
    )
    assert result["selected_refseq"] == "NM_001234.5"
    assert result["metadata"]["response"]["docs"][0]["symbol"] == "Test"
    assert result["sequence"] ["GBSeq_sequence"]=="ACTG"

    api.fetch_genbank_transcript.assert_called_once_with(
        "NM_001234.5"
    )
