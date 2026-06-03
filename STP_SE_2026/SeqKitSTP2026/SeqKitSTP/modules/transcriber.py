import logging
import datetime
logger = logging.getLogger("SeqKitSTP")


def transcribe(dna_sequence: str) -> str:

    if len(dna_sequence) <= 0:
        logger.error("User input is empty")
        raise ValueError("You have not entered anything")
    
    rna_sequence = dna_sequence.lower().replace("t", "u")

    with open("transcribed_sequence.txt", "a") as f:
        f.write(rna_sequence + " | " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        logger.info("Transcribed sequence written to transcribed_sequence.txt")
    
    logger.info("Transcription complete")
    return rna_sequence
