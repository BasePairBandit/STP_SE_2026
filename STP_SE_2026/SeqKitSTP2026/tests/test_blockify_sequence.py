import pytest
import logging
from SeqKitSTP.modules.blockify_sequence import blockify_seq

def test_sequence_regular_case(): #normal case
    dna_sequence = "aggagtaagcccttgcaactggaaatacacccattg"
    block_size = 5
    expected = 'aggag taagc ccttg caact ggaaa tacac ccatt g'
    assert blockify_seq(dna_sequence, block_size) == expected

def test_block_size_large_error_log(caplog): #when dna_sequence length is < block size
    dna_sequence = "aaa"
    block_size = 5
    caplog.set_level(logging.ERROR) #Tells pytest to capture error logs
    with pytest.raises(ValueError):
# blockify_seq raises a ValueError when block_size is too large,
# which would normally stop the test execution.
# pytest.raises is used to catch the exception so we can continue
# and verify that the error log message was recorded.
        blockify_seq(dna_sequence, block_size)
    assert "Invalid block size, block size must not exceed the length of the DNA sequence" in caplog.text

def test_convert_to_lowercase():#Checking if the .lower() is working
    dna_sequence = "AAAAAAAAAACCCGTGTGAAAAAAA"
    block_size = 3
    expected = 'aaa aaa aaa acc cgt gtg aaa aaa a'
    assert blockify_seq(dna_sequence, block_size) == expected

def test_valid_bases(caplog):#Checking if it can detect numerical/non-letters and raise the exception + log.
    """
    learning point, because originally I put the block size check before the valid bases 
    check in my blockify function, it was  failing the valid bases pytest (with block size being smaller than the dna_sequence), 
    therefore this raises a value error and it never reached the Type error test. 
    So I switched the order of the exceptions. Alternatively I could have also altered the block size 
    to a lower number.
    """
    dna_sequence = "AC2"
    block_size = 5
    caplog.set_level(logging.ERROR) #Tells pytest to capture error logs
    with pytest.raises(TypeError):
        blockify_seq(dna_sequence, block_size)
    assert "Invalid base entered in the dna sequence" in caplog.text

def test_empty_dna_sequence(caplog): #Same as test case on test_block_size_large_error_log but here the user doesn't enter anything.
    dna_sequence = ""
    block_size = 0
    caplog.set_level(logging.ERROR)
    with pytest.raises(ValueError):
        blockify_seq(dna_sequence, block_size)
    assert "Block size must be greater than 0" in caplog.text
