import logging
logger = logging.getLogger("SeqKitSTP")
valid_bases = ["a","c","t","g"]

def blockify_seq(dna_sequence: str, block_size: int) -> str:
    # Remove spaces,newlines and uppercase
    
    if block_size <= 0:
        logger.error("Block size must be greater than 0")
        raise ValueError("Block size must be greater than 0")

    if any(base not in valid_bases for base in dna_sequence.lower()):
        logger.error("Invalid base entered in the dna sequence")
        raise TypeError("DNA sequence must only contain these letters: [a] [c] [t] [g]")

    if block_size > len(dna_sequence):
        logger.error("Invalid block size, block size must not exceed the length of the DNA sequence")
        raise ValueError("Invalid block size, block size must not exceed the length of the DNA sequence")
    sequence = dna_sequence.replace("\n", "").replace(" ", "").lower()

    blocks = []

    # Loop through the sequence in steps of block_size
    for i in range(0, len(sequence), block_size):
        block = sequence[i:i + block_size]
        blocks.append(block)

    # Join blocks with spaces
    return " ".join(blocks)

