import requests
import xmltodict
import logging

logger = logging.getLogger(__name__)


class TranscriptIdError(Exception):
    """
    Raised when a transcript identifier is invalid.
    """
    pass

# ------------------------------------------------------------------
# Python classes and objects
#
# A class is a blueprint for creating objects. An object groups together
# related data (attributes) and functions (methods) into a single unit.
#
# In this example we create a SequenceAPI object because all of the
# functionality relates to interacting with biological sequence
# databases. The object stores information shared by every request,
# such as the HTTP session, timeout value and API URLs, while its
# methods perform specific tasks such as retrieving transcripts from
# GenBank or Ensembl.
#
# Organising the code this way keeps related functionality together,
# reduces duplication and makes it easy to add support for additional
# APIs in the future.
# ------------------------------------------------------------------
class SequenceAPI:
    """
    Interface to external sequence databases.

    Current support
    ---------------
    - GenBank / RefSeq
    - Ensembl (planned)
    - HGNC (planned)
    - UniProt (planned)
    - ClinVar (planned)
    """

    def __init__(self, timeout=30):
        """
        Initialise the API interface.
        """

        # Session configuration
        self.timeout = timeout

        # Create a persistent HTTP session.
        # Unlike requests.get(), a Session reuses TCP connections across multiple
        # requests (connection pooling), making repeated API calls more efficient.
        # It also provides a central place to configure headers, authentication,
        # cookies and retry behaviour if required in the future.
        self.session = requests.Session()

        # API endpoints.
        #
        # These URLs identify the web services used by SeqToolkit to retrieve
        # biological data.
        #
        # The leading underscore (_) is a Python naming convention indicating
        # that these attributes are intended for internal use within the class.
        # Unlike some programming languages, Python does not enforce private
        # variables. Instead, it relies on naming conventions:
        #
        #     public_attribute      Intended for anyone to use.
        #     _internal_attribute   Intended for use inside the class only
        #                           (a convention, not enforced).
        #     __private_attribute   Name-mangled by Python to make accidental
        #                           access more difficult.
        #
        # The public methods of this class (e.g. fetch_genbank_transcript())
        # use these endpoint URLs internally when communicating with each
        # external database.

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

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # @staticmethod tells Python that this method does not need access
    # to the object itself (self).
    #
    # Normally, methods inside a class receive the current object as their
    # first argument:
    #
    #     def my_method(self):
    #
    # However, this validation function only examines the transcript ID
    # passed to it. It doesn't read or modify any attributes of the
    # SequenceAPI object.
    #
    # Using @staticmethod tells Python that this function behaves like a
    # regular function, but we keep it inside the class because it is
    # closely related to the SequenceAPI.
    # ------------------------------------------------------------------
    @staticmethod
    def _validate_refseq_transcript(transcript_id):
        """
        Validate a RefSeq transcript accession.
        """

        if not transcript_id.startswith(("NM_", "NR_")):
            raise TranscriptIdError(
                f"{transcript_id} is not a supported RefSeq transcript."
            )

        if "." not in transcript_id:
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

    def fetch_ensembl_38_transcript(self, full_user_transcript_id):
        """
        Fetch Ensembl transcript information.

        Because default is current version and I have nto found a work around to deal with specific versions, I will add a disclaimer if the version the user
        enters is not a match with the latest. It seems like I would need to know the exact release for a particular version which seems a bit complex.
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
        
        Because default is current version and I have nto found a work around to deal with specific versions, I will add a disclaimer if the version the user
        enters is not a match with the latest. It seems like I would need to know the exact release for a particular version which seems a bit complex.

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
    
    print("""
    Welcome to SeqKitSTP!
    Select an option to proceed:
    1. Genbank
    2. Ensembl (GRCh38)
    3. Ensembl (GRCh37)
    4. Exit
          """)
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

                "Please enter a transcript ID with a version, eg. ENST00000288602.6"                )
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
<<<<<<< HEAD
                if int(user_transcript_version) != int(latest_version):
                        print(f"Ensembl REST API returns the current version for this stable ID which is {latest_full_id}. To retrieve an specific version, you would need the relevant "
=======

                if int(user_transcript_version) != int(record["metadata"]["version"]):
                        print(f"The Ensembl REST API returns the current version for this stable ID which is {latest_full_id}. To retrieve an specific version, you would need the relevant "
>>>>>>> 623824e (no major changes)
                                f"Ensembl archive release.")

                structured_record = api.structure_ensembl_transcript(record)

                print(f"Transcript_ID : {structured_record['id']}")
                print(f"Transcript_name : {structured_record['name']}")
                print(f"Sequence : {structured_record['sequence']}")
                print(f"CDS start : {structured_record['cds_start']}")
                print(f"CDS end : {structured_record['cds_end']}")
            elif user_choice == "3":
                record = api.fetch_ensembl_37_transcript(user_transcript_id)
                latest_version = record["metadata"]["version"]
                latest_full_id = f"{record['metadata']['id']}.{latest_version}"
<<<<<<< HEAD
                if int(user_transcript_version) != int(latest_version):
                        print(f"Ensembl REST API returns the current version for this stable ID which is {latest_full_id}. To retrieve an specific version, you would need the relevant "
                                f"Ensembl archive release.")


=======
                if int(user_transcript_version) != int(record["metadata"]["version"]):
                        print(f"The Ensembl REST API returns the current version for this stable ID which is {latest_full_id}. To retrieve a specific version, you would need the relevant "
                                f"Ensembl archive release.")
                        
>>>>>>> 623824e (no major changes)
                structured_record = api.structure_ensembl_transcript(record)

                print(f"Transcript_ID : {structured_record['id']}")
                print(f"Transcript_name : {structured_record['name']}")
                print(f"Sequence : {structured_record['sequence']}")
                print(f"CDS start : {structured_record['cds_start']}")
                print(f"CDS end : {structured_record['cds_end']}")
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

    except Exception as e:
        logger = logging.getLogger("SeqKitSTP")
        logger.error("An error occurred: %s", str(e))

