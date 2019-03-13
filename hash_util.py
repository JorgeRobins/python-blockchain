import hashlib as hl
import json

def hash_string_256(string):
    return hl.sha256(string).hexdigest()
    

def hash_block(block):
    """ Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    # sort_keys ensures the same order and therefore the same hash for the same input since block is a dictionary which is unordered
    return hash_string_256(json.dumps(block, sort_keys=True).encode())
    # OLD - return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()