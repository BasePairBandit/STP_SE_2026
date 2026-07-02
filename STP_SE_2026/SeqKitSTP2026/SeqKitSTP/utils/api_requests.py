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
        self.session = requests.Session()

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
            raise TranscriptIdError(
                f"{transcript_id} is not a supported RefSeq transcript."
            )
        logger.exception("User input doesn't start with 'NM-' or 'NR_")

        if "." not in transcript_id:
            raise TranscriptIdError(
                f"{transcript_id} must include a version number."
            )
        logger.exception("Version number not included in user input")

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

        Because default is current version and I have not found a work around to deal with specific versions, I will add a disclaimer if the version the user
        enters is not a match with the latest. It seems like I would need to know the exact release for a particular version which seems a bit complex so leaving it out for now.
        """
        self._validate_ensembl_transcript(full_user_transcript_id)

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
        
        Because default is current version and I have not found a work around to deal with specific versions, I will add a disclaimer if the version the user
        enters is not a match with the latest. It seems like I would need to know the exact release for a particular version which seems a bit complex so leaving it out for now.

        GRCh37 doesn't support mane select?
        """
        self._validate_ensembl_transcript(full_user_transcript_id)

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

    def fetch_hgnc_gene(self, gene_symbol):
        """
        Fetch HGNC gene information.

        Placeholder.
        """

        raise NotImplementedError()

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
        Sequence = record["sequence"]

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
    

if __name__ == "__main__":
    #Perhaps better to place this block in main.py? Need to also find a way no not over expand the menu. Maybe look into dispatch table.
    print("""
    Welcome to SeqKitSTP!
    Select an option to proceed:
    1. Genbank
    2. Ensembl (GRCh38)
    3. Ensembl (GRCh37)
    4. Exit
          """)
    
    # Examples to test code : ENST00000367770.8 (SCYL3), ENST00000420246.5 (TP53 alternative)

    try:
        while True:
            api = SequenceAPI()
            user_choice = input("Enter your choice (1, 2, 3, or 4): ")
            if user_choice == "4":
                print("Exiting SeqKitSTP. Goodbye!")
                break
            full_user_transcript_id = input("Enter transcript ID (including version) :")
            split_user_transcript_id = full_user_transcript_id.split(".")
            if len(split_user_transcript_id) != 2:
                raise TranscriptIdError(

                "Please enter a transcript ID with a version, eg. ENST00000252486.9"                )
            user_transcript_id = split_user_transcript_id[0]
            user_transcript_version = split_user_transcript_id[1]

            if user_choice == "1":
                record = api.fetch_genbank_transcript(str(full_user_transcript_id))
                print(f"Accession: {record["GBSeq_accession-version"]}")
                print(f"Name: {record["GBSeq_definition"]}")
                print(f"KeyWords: {record["GBSeq_keywords"]}")
                print(f"Sequence: {record["GBSeq_sequence"].upper()}")
                for feature in record["GBSeq_feature-table"]["GBFeature"]:
                    if feature["GBFeature_key"] == "gene":
                        print(f"GeneSymbol: {feature["GBFeature_quals"]["GBQualifier"][0]["GBQualifier_value"]}")
                    elif feature["GBFeature_key"] == "CDS":
                        print(f"CDS_Start: {feature["GBFeature_intervals"]["GBInterval"]["GBInterval_from"]}")
                        print(f"CDS_End: {feature["GBFeature_intervals"]["GBInterval"]["GBInterval_to"]}")

            elif user_choice == "2":
                record = api.fetch_ensembl_38_transcript(user_transcript_id)
                latest_version = record["metadata"]["version"]
                latest_full_id = f"{record['metadata']['id']}.{latest_version}"

                if int(user_transcript_version) != int(latest_version):
                    print(
                        f"The Ensembl REST API returns the current version for this stable ID "
                        f"which is {latest_full_id}. To retrieve a specific version, you would "
                        f"need the relevant Ensembl archive release."
    )
                structured_record = api.structure_ensembl_transcript(record)

                print(f"Transcript_ID : {structured_record['id']}")
                print(f"Transcript_name : {structured_record['name']}")
                mane = api.extract_mane(record)
                if mane:
                    print(f"MANE Select transcript : {mane}")
                else:
                    print("No MANE select found")
                print(f"Sequence : {structured_record['sequence']}")
                print(f"CDS start : {structured_record['cds_start']}")
                print(f"CDS end : {structured_record['cds_end']}")
            elif user_choice == "3":
                record = api.fetch_ensembl_37_transcript(user_transcript_id)
                latest_version = record["metadata"]["version"]
                latest_full_id = f"{record['metadata']['id']}.{latest_version}"

                if int(user_transcript_version) != int(latest_version):
                    print(
                        f"The Ensembl REST API returns the current version for this stable ID "
                        f"which is {latest_full_id}. To retrieve a specific version, you would "
                        f"need the relevant Ensembl archive release."
                    )

                structured_record = api.structure_ensembl_transcript(record)

                print(f"Transcript_ID : {structured_record['id']}")
                print(f"Transcript_name : {structured_record['name']}")
                mane = api.extract_mane(record)
                if mane:
                    print(f"MANE Select transcript : {mane}")
                else:
                    print("No MANE select found")
                print(f"Sequence : {structured_record['sequence']}")
                print(f"CDS start : {structured_record['cds_start']}")
                print(f"CDS end : {structured_record['cds_end']}")
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

    except Exception as e:
        logger = logging.getLogger("SeqKitSTP")
        logger.error("An error occurred: %s", str(e))

