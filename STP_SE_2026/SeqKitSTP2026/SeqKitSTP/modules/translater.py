import logging
import datetime
logger = logging.getLogger("SeqKitSTP")

codon_table = {
    "uuu": "F", "uuc": "F",
    "uua": "L", "uug": "L", "cuu": "L", "cuc": "L", "cua": "L", "cug": "L",
    "auu": "I", "auc": "I", "aua": "I",
    "aug": "M",
    "guu": "V", "guc": "V", "gua": "V", "gug": "V",
    "ucu": "S", "ucc": "S", "uca": "S", "ucg": "S",
    "agu": "S", "agc": "S",
    "ccu": "P", "ccc": "P", "cca": "P", "ccg": "P",
    "acu": "T", "acc": "T", "aca": "T", "acg": "T",
    "gcu": "A", "gcc": "A", "gca": "A", "gcg": "A",
    "ugu": "C", "ugc": "C",
    "ugg": "W",
    "cgu": "R", "cgc": "R", "cga": "R", "cgg": "R", "aga": "R", "agg": "R",
    "ggu": "G", "ggc": "G", "gga": "G", "ggg": "G",
    "uau": "Y", "uac": "Y",
    "cau": "H", "cac": "H",
    "caa": "Q", "cag": "Q",
    "aau": "N", "aac": "N",
    "aaa": "K", "aag": "K",
    "gau": "D", "gac": "D",
    "gaa": "E", "gag": "E",
    "uaa": "*", "uag": "*", "uga": "*"
}

stop_codons = {"uaa", "uga", "uag"}

def translate(rna_sequence: str, CDS_start: str, CDS_end: str) -> str:

    if len(rna_sequence) <= 0:
        logger.error("RNA input is empty")
        raise ValueError("RNE sequence is empty")
    if rna_sequence != rna_sequence.lower():
        logger.error("RNA input contains uppercase characters")
        raise ValueError("RNA sequence contains uppercase characters. Please check the sequence and enter in lowercase.")

    for nucleotide in rna_sequence:
        if nucleotide not in "acgu":
            logger.error("RNA input contains invalid characters")
            raise ValueError("RNA sequence contains invalid characters. Only a, c, g, u are allowed.")

    CDS_start = CDS_start.lower() if CDS_start else "aug"
    CDS_end = CDS_end.lower() if CDS_end else None

    start_index = rna_sequence.find(CDS_start)
    if start_index == -1:
        logger.error("Start codon not found")
        raise ValueError(f"Start codon not found")

    stop_index = None
    for i in range(start_index + 3, len(rna_sequence) - 2, 3):
        codon = rna_sequence[i:i + 3]
        if CDS_end:
            if codon == CDS_end:
                stop_index = i
                break
        else:
            if codon in stop_codons:
                stop_index = i
                break        
    
    if stop_index is None:
        logger.error("Stop codon not found after start or invalid stop codon entered")
        raise ValueError("Stop codon not found after start or invalid stop codon entered")

    CDS_rna_sequence = rna_sequence[start_index: stop_index + len(CDS_end)]

    if len(CDS_rna_sequence) % 3 != 0:
        logger.error("CDS sequence is not divisible by 3")
        raise ValueError("CDS sequence is not divisible by 3. Please check the start and end codon positions.")

    blocks = [CDS_rna_sequence[i:i + 3] for i in range(0, len(CDS_rna_sequence), 3)]

    amino_acid_sequence = ""
    for codon in blocks:
        if codon not in codon_table:
            logger.error("Invalid codon encountered: %s", codon)
            raise ValueError(f"Invalid codon in CDS sequence: {codon}")
        amino_acid_sequence += codon_table[codon]

    with open("translated_sequence.txt", "a") as f:
        f.write(amino_acid_sequence + " | " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        logger.info("Translated sequence written to translated_sequence.txt")
    
    logger.info("Translation complete")
    return amino_acid_sequence
