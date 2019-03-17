import hashlib as hl
import json

def hash_string_256(string):
    """ Create a SHA256 hash for a given input string.
    
    Arguments:
        :string: The string which should be hashed.    
    """
    return hl.sha256(string).hexdigest()
    

def hash_block(block):
    """ Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    # modify the block to a dict so that it can be saved with json library
    # you must call copy in order to not change dict of older blocks in the future
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    # sort_keys ensures the same order and therefore the same hash for the same input since block is a dictionary which is unordered
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
    # OLD - return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()