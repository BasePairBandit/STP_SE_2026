from pdb import main

from numpy import full
import requests
import xmltodict
import logging

logger = logging.getLogger(__name__)


class TranscriptIdError(Exception):
    """
    Raised when a transcript identifier is invalid.
    """
    pass

class SequenceAPI:
    """
    Interface to external sequence databases.

    Current support
    ---------------
    - GenBank / RefSeq
    - Ensembl 
    - HGNC (planned)
    - UniProt (planned)
    - ClinVar (planned)
    """

    def __init__(self, timeout=30):
        """
        Initialise the API interface.
        """
        self.timeout = timeout
        self.session = requests.Session() #More efficient than creating a new connection for every request.

        self._genbank_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self._ensembl_url = "https://rest.ensembl.org"
        self._ensembl_37_url = "https://grch37.rest.ensembl.org"
        self._hgnc_url = "https://rest.genenames.org"
        self._uniprot_url = "https://rest.uniprot.org"
        self._clinvar_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    # ------------------------------------------------------------------
    # Internal HTTP methods
    # ------------------------------------------------------------------

    def _get(self, base_url, endpoint="", params=None, headers=None):
        """
        Generic HTTP GET helper.
        """

        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response

        except requests.exceptions.RequestException:
            logger.exception(f"Failed GET request: {url}")
            raise

    @staticmethod
    def _validate_refseq_transcript(transcript_id):
        """
        Validate a RefSeq transcript accession.
        """

        if not transcript_id.startswith(("NM_", "NR_")):
            logger.exception("User input doesn't start with 'NM-' or 'NR_")
            raise TranscriptIdError(
                f"{transcript_id} is not a supported RefSeq transcript."
            )

        if "." not in transcript_id:
            logger.exception("Version number not included in user input")
            raise TranscriptIdError(
                f"{transcript_id} must include a version number."
            )


    @staticmethod
    def _validate_ensembl_transcript(transcript_id):
        """
        Validate a RefSeq transcript accession.
        """

        if not transcript_id.startswith(("ENST")):
            raise TranscriptIdError(
                f"{transcript_id} is not a supported Ensembl transcript."
            )

        #if "." not in transcript_id:
            #raise TranscriptIdError(
                #f"{transcript_id} must include a version number."
            #)

    @staticmethod
    def _validate_hgnc_transcript(HGNC_ID):
        """
        Validate a hgnc transcript.
        """

        if not HGNC_ID.startswith(("HGNC:")):
            raise TranscriptIdError(
                f"{HGNC_ID} is not a supported HGNC ID."
            )

    # ------------------------------------------------------------------
    # GenBank
    # ------------------------------------------------------------------

    def fetch_genbank_transcript(self, transcript_id):
        """
        Fetch a RefSeq transcript from GenBank.
        """

        self._validate_refseq_transcript(transcript_id)

        response = self._get(
            self._genbank_url,
            "efetch.fcgi",
            params={
                "db": "nucleotide",
                "id": transcript_id,
                "retmode": "xml",
            },
        )

        return xmltodict.parse(response.text)["GBSet"]["GBSeq"]

    # ------------------------------------------------------------------
    # Ensembl - GRCh38
    # ------------------------------------------------------------------

    def fetch_ensembl_38_transcript(self, user_transcript_id):
        """
        Fetch Ensembl transcript information.

        Because default is current version and I have not found a work around to deal with specific versions, 
        I added a disclaimer if the version the user enters is not a match with the latest. It seems like I 
        would need to know the exact release for a particular version which seems a bit complex so leaving it out for now.
        """
        self._validate_ensembl_transcript(user_transcript_id)

        meta_response = self._get(
            self._ensembl_url,
            f"lookup/id/{user_transcript_id}",
            params={"content-type": "application/json","expand": 1,},
            headers={}
        )        

        sequence_response = self._get(
            self._ensembl_url,
            f"sequence/id/{user_transcript_id}",
            headers={"content-type":"application/json"}
        )

        return{
            "metadata":meta_response.json(),
            "sequence": sequence_response.json(),
        }

    # ------------------------------------------------------------------
    # Ensembl - GRCh37
    # ------------------------------------------------------------------

    def fetch_ensembl_37_transcript(self, user_transcript_id):
        """
        Fetch Ensembl transcript information for GRCh37
        
        Because default is current version and I have not found a work around to deal with specific versions, 
        I will add a disclaimer if the version the user enters is not a match with the latest. It seems like I
        would need to know the exact release for a particular version which seems a bit complex so leaving it out for now.

        GRCh37 doesn't support mane select?
        """
        self._validate_ensembl_transcript(user_transcript_id)

        meta_response = self._get(
            self._ensembl_37_url,
            f"lookup/id/{user_transcript_id}",
            params={"content-type": "application/json","expand": 1,},
            headers={}
        )        

        sequence_response = self._get(
            self._ensembl_37_url,
            f"sequence/id/{user_transcript_id}",
            headers={"content-type":"application/json"}
        )

        return{
            "metadata":meta_response.json(),
            "sequence": sequence_response.json(),
        }

    # ------------------------------------------------------------------
    # HGNC
    # ------------------------------------------------------------------

    def fetch_hgnc_gene(self, HGNC_ID):
        """
        Fetch HGNC gene information.

        Placeholder.
        """
        self._validate_hgnc_transcript(HGNC_ID)

        meta_response = self._get(
            self._hgnc_url,
            f"/fetch/hgnc_id/{HGNC_ID}",
            headers={"Accept": "application/json"},
        )    
        return{
            "metadata":meta_response.json(),
        }


    # ------------------------------------------------------------------
    # UniProt
    # ------------------------------------------------------------------

    def fetch_uniprot_protein(self, accession):
        """
        Fetch a UniProt protein.

        Placeholder.
        """

        raise NotImplementedError()

    # ------------------------------------------------------------------
    # ClinVar
    # ------------------------------------------------------------------

    def fetch_clinvar_record(self, accession):
        """
        Fetch a ClinVar record.

        Placeholder.
        """

        raise NotImplementedError()

    # ------------------------------------------------------------------
    # Extract MANE select
    # ------------------------------------------------------------------

    def extract_mane(self, record):
        metadata = record["metadata"]
        gene_id = metadata["Parent"]

        tx_response = self._get(
            self._ensembl_url,
            f"overlap/id/{gene_id}?feature=transcript",
            params={"content-type": "application/json","expand": 1,},
            headers={}
        )
        transcripts = tx_response.json()
        
        for tx in transcripts:
            if "tag" in tx and "MANE_Select" in tx["tag"]:
                return tx["id"]
        return None

    # ------------------------------------------------------------------
    # Structure Ensembl API data into a dictionary
    # ------------------------------------------------------------------

    def structure_ensembl_transcript(self,record):
        metadata = record["metadata"]

        transcript_id = f"{metadata['id']}"
        transcript_name = metadata['display_name']
        transcript_sequence = record["sequence"]["seq"]
        translation_start = record["metadata"]["Translation"]["start"]
        translation_end = record["metadata"]["Translation"]["end"]
        return{
            "id": transcript_id,
            "name": transcript_name,
            "sequence": transcript_sequence,
            "cds_start":translation_start,
            "cds_end" : translation_end,
        }
    # ------------------------------------------------------------------
    # Structure HGNC API data into a dictionary
    # ------------------------------------------------------------------


    def structure_HGNC_transcript(self,record): # This function is missing sequence and CDS info.

        doc = record["metadata"]["response"]["docs"][0]

        return{
            "HGNC_id": doc["hgnc_id"],
            "symbol": doc["symbol"],
            "ensembl_gene_id": doc.get("ensembl_gene_id"),
            "mane_select" : doc.get("mane_select"),
        }
    
    # Examples to test code : ENST00000367770.8 (SCYL3), ENST00000420246.5 (TP53 alternative), HGNC:613(APOE).
