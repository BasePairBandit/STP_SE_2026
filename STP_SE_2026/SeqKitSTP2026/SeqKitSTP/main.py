import logging
import logging.config

from SeqKitSTP.settings import LOGGING_CONFIG
from SeqKitSTP.modules.blockify_sequence import blockify_seq
from SeqKitSTP.modules.genify_sequence import genify_seq


def main():
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


if __name__ == "__main__":
    #Activate logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)

    main()