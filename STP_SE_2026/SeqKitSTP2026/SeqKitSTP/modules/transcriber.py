import logging
import datetime
logger = logging.getLogger("SeqKitSTP")
valid_bases = ["A","T","C","G"]


def transcribe(dna_sequence: str) -> str:

    cleaned_rna_sequence = dna_sequence.replace(" ","")
    
    if len(cleaned_rna_sequence) <= 0:
        logger.error("User input is empty")
        raise ValueError("You have not entered anything")

    if any(base not in valid_bases for base in cleaned_rna_sequence):
        logger.error("DNA input contains invalid characters")
        raise TypeError("DNA sequence must only contain these letters: [A] [C] [T] [G]")
    
    rna_sequence = cleaned_rna_sequence.lower().replace("t", "u")

    with open("transcribed_sequence.txt", "a") as f:
        f.write(rna_sequence + " | " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        logger.info("Transcribed sequence written to transcribed_sequence.txt")
    
    logger.info("Transcription complete")
    return rna_sequence
