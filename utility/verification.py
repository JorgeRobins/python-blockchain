""" Provides verification helper methods """

# External

# Internal
from wallet import Wallet
from utility.hash_util import hash_string_256, hash_block

# Verification is a "container" or "helper" class
# We do not use it to create objects (from a class blueprint)
# We are simply "verifying"

class Verification:
    """ A helper class which offers various static and class-based verification methods """
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """ Validate a proof of work number and see if it solves the puzzle algorithm

        Arguments:
            :transactions: The transactions of the block for which the proof is being calculated
            :last_hash: The previous block's hash which will be stored in the current block
            :proof: The proof number we're testing
        """
        # Create a string with all the hash inputs
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        print(guess)
        # Hash the string
        # IMPORTANT: This is NOT the same hash as will be stored in the previous_block
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        # Only a hash (which is based on the above inputs) which meets the requirements is considered valid
        # In this case it is 2 leading zeroes
        return guess_hash[0:2] == '00'
    

    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and return True if its valid, False otherwise. """
        for (index, block) in enumerate(blockchain):
            if index == 0:
                # Genesis block cannot be modified since the hash is confirmed in the first block
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            # Use the transactions except the reward transaction by specifying :-1
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        return True


    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        """ Verify a transaction by checking whether the sender has sufficient coins

        Arguments:
            :transaction: The transaction that should be verified.
        """
        if check_funds:
            sender_balance = get_balance()
            # Returns Boolean 
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)


    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """ Verifies all open transactions """
        # all function used on Boolean verify_transaction(tx) so all tx must be verified as valid in order to return True
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions])