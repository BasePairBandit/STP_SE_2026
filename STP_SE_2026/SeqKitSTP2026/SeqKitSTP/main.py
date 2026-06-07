import logging
import logging.config

from SeqKitSTP.settings import LOGGING_CONFIG
from SeqKitSTP.modules.blockify_sequence import blockify_seq
from SeqKitSTP.modules.genify_sequence import genify_seq
from SeqKitSTP.modules.transcriber import transcribe
from SeqKitSTP.modules.translater import translate

def main():
    print("""
    Welcome to SeqKitSTP!
    Select an option to proceed:
    1. Blockify and genify a DNA sequence
    2. Transcribe a DNA sequence to RNA
    3. Translate an RNA sequence to amino acids
    4. Exit
          """)
    try:
        while True:
            user_choice = input("Enter your choice (1, 2, 3, or 4): ")
            if user_choice == "1":

                """
                Blockify and genify a DNA sequence based on user input, and write the results to output files.
                """
            
                logger = logging.getLogger("SeqKitSTP")

                logger.info("Initiating blockifying the sequence")

                dna_sequence = input("Enter the DNA sequence: ")
                block_size = int(input("Enter the block size: "))

                blocked_result = blockify_seq(dna_sequence, block_size)

                output_file_blocked = "blocked_sequence.txt"
                logger.info(f"Writing to output file: {output_file_blocked}")

                with open(output_file_blocked, "w") as f:
                    f.write(blocked_result)

                logger.info("Initiating genifying the blocked sequence")

                genbank_result = genify_seq(blocked_result)

                output_file_genified = "genbank_sequence.txt"
                logger.info(f"Writing to output file: {output_file_genified}")

                with open(output_file_genified, "w") as f:
                    f.write(genbank_result)

                logger.info("Complete")
            
            elif user_choice == "2":
                """
                Transcribe a DNA sequence to RNA based on user input.
                """
                dna_sequence = input("Enter the DNA sequence: ")
                transcribe(dna_sequence)
            elif user_choice == "3":
                """
                Translate an RNA sequence to amino acids based on user input.
                """
                rna_sequence = input("Enter the RNA sequence: ").lower().replace(" ", "").replace("\n", "" )
                CDS_start = input("Enter the start codon (default is aug): ")
                if CDS_start == "":
                    CDS_start = "aug"
                CDS_end = input("Enter the stop codon (default is uga): ")
                if CDS_end == "":
                    CDS_end = "uga"
                translate(rna_sequence, CDS_start, CDS_end)

            elif user_choice == "4":
                print("Exiting SeqKitSTP. Goodbye!")
                logger = logging.getLogger("SeqKitSTP")
                logger.info("Exiting SeqKitSTP")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
    except Exception as e:
        logger = logging.getLogger("SeqKitSTP")
        logger.error("An error occurred: %s", str(e))
if __name__ == "__main__":
    #Activate logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)

    main()