from SeqKitSTP.utils.api_requests import SequenceAPI, TranscriptIdError
from SeqKitSTP.modules.transcriber import transcribe
from SeqKitSTP.modules.translater import translate
from SeqKitSTP.modules.blockify_sequence import blockify_seq
from SeqKitSTP.modules.genify_sequence import genify_seq
import logging
logger = logging.getLogger(__name__)

api = SequenceAPI()

def run_api_menu():
    try:
        while True:
            print(r"""
                Welcome to API lookup!
                
                    -. .-.   .-. .-.   .-. .-.   .  
                    ||\|||\ /|||\|||\ /|||\|||\ /|
                    |/ \|||\|||/ \|||\|||/ \|||\||
                    ~   `-~ `-`   `-~ `-`   `-~ `-

                    Select an option to proceed:
                    1. Genbank
                    2. Ensembl (GRCh38)
                    3. Ensembl (GRCh37)
                    4. HGNC (ID)
                    5. HGNC (gene name)
                    6. Main menu (Back)
                        """)
            user_choice = input("Enter your choice (1, 2, 3, 4 or 5): ")
            if user_choice == "6":
                print("Exiting SeqKitSTP. Goodbye!")
                break
            if user_choice == "4":
                HGNC_ID = input("Enter HGNC_ID:")
                record = api.fetch_hgnc_gene(HGNC_ID)
                structured_record = api.structure_HGNC_transcript(record)
                print(f"HGNC_ID : {structured_record['HGNC_id']}")
                print(f"Symbol : {structured_record['symbol']}")
                print(f"ensembl_gene_id : {structured_record['ensembl_gene_id']}")
                print(f"mane_select : {structured_record['mane_select']}")
                continue
            if user_choice == "5":
                HGNC_gene_name = input("Enter gene name:")
                record = api.fetch_hgnc_gene_by_name(HGNC_gene_name)
                structured_record = api.structure_HGNC_gene_by_name(record)
                print(f"HGNC_ID : {structured_record['HGNC_id']}")
                print(f"Symbol : {structured_record['symbol']}")
                print(f"ensembl_gene_id : {structured_record['ensembl_gene_id']}")
                print(f"mane_select : {structured_record['mane_select']}")
                continue
            full_user_transcript_id = input("Enter transcript ID (including version) :")
            split_user_transcript_id = full_user_transcript_id.split(".")
            if len(split_user_transcript_id) != 2:
                raise TranscriptIdError("Please enter a transcript ID with a version, eg. ENST00000252486.9")

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
                sequence = structured_record['sequence']
                rna_sequence = transcribe(sequence)
                translate(rna_sequence,"","") 
                #using default here for now but would be better to slice out the codons based on CDS_start and CDS end.
                #Because at the moment it is just stopping at the first uga?

                blocked_sequence = blockify_seq(sequence,5)
                output_file_blocked = "blocked_sequence.txt"
                with open(output_file_blocked, "w") as f: # Repeating from sequencing_menu as the blockify function doesn't have this save to file option.
                                    f.write(blocked_sequence)
                genified_sequence = genify_seq(blocked_sequence)
                output_file_genified = "genbank_sequence.txt"
                with open(output_file_genified, "w") as f:
                     f.write(genified_sequence)

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