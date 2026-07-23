import logging
logger = logging.getLogger("SeqKitSTP")


def genify_seq(blocked_sequence: str) -> str:

    logger.info("Formatting GenBank output")
    if len(blocked_sequence) <= 0:
        logger.error("Block size must be greater than 0")
        raise ValueError("Block size must be greater than 0")

    blocks = blocked_sequence.split()

    gen_block_size = input("Enter block size for genbank file output:")
    try:
        gen_block_size = int(gen_block_size)
    except ValueError:
        logger.error("Block size must be numerical")
        raise ValueError("Block size must be numerical")
    if gen_block_size <= 0:
        logger.error("Block size must not be zero or negative")
        raise ValueError("Block size must not be zero or negative") 

    lines = []
    position = 1

    for i in range(0, len(blocks), gen_block_size):
        line_blocks = blocks[i:i + gen_block_size]
        
        sequence_line = " ".join(line_blocks)

        line = f"{position:>9} {sequence_line}"
        lines.append(line)

        position += len("".join(line_blocks))

    return "\n".join(lines)

