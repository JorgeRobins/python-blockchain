# External Imports
from functools import reduce
import hashlib as hl
import json
import pickle
import requests

# Internal Imports
from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

# The reward we give to miners (for creating a new block)
MINING_REWARD = 50


class Blockchain:
    def __init__(self, public_key, node_id):
        # Our starting block for the blockchain
        GENESIS_BLOCK = Block(0, '', [], 100, 0)
        # Initializing our blockchain with the genesis block
        self.chain = [GENESIS_BLOCK]
        # Unhandled transactions
        self.__open_transactions = []
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.resolve_conflicts = False
        # Keep load_data() at the end so you don't overwrite loaded data
        self.load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        """ Initialize blockchain and open transactions data from a file """
        # with open('blockchain.p', mode='rb') as f:
        #     file_content = pickle.loads(f.read())
        #     blockchain = file_content['chain']
        #     open_transactions = file_content['ot']

        # OrderedDict of blocks and transactions must be taken into account
        # otherwise the POW check will error
        try:
            with open('data/blockchain-{}.txt'
                      .format(self.node_id), mode='r') as f:
                file_content = f.readlines()
                # loads method in json library used to deserialize the string
                # to return python object
                # [:-1] removes \n character which isn't converted as
                # it isn't valid json
                blockchain = json.loads(file_content[0][:-1])
                # We need to convert the loaded data because transactions
                # should use OrderedDict
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['signature'],
                        tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_tx, block['proof'],
                        block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                # We need to convert the loaded data because transactions
                # should use OrderedDict
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'],
                                                      tx['recipient'],
                                                      tx['signature'],
                                                      tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        # except case specifying IO errors (no file) and Index error
        # (empty file)
        except (IOError, IndexError):
            print('Handled exception...')
        # finally always runs, whether there was a success or failure
        finally:
            print('Cleanup')

    def save_data(self):
        """ Save blockchain and open transactions snapshot to a file """
        # Pickle version: requires mode='wb' for binary
        # and file extension .p can be used
        # with open('blockchain.p', mode='wb') as f:
        #     save_data = {
        #         'chain': blockchain,
        #         'ot': open_transactions
        #     }
        #     f.write(pickle.dumps(save_data))
        # dumps method in json library used to
        # convert python objects to strings
        try:
            with open('data/blockchain-{}.txt'
                      .format(self.node_id), mode='w') as f:
                # modify each block to a dict so that it can be saved
                # with json library
                saveable_chain = [
                    block.__dict__ for block in
                    [
                        Block(block_el.index,
                              block_el.previous_hash,
                              [tx.__dict__ for tx in block_el.transactions],
                              block_el.proof,
                              block_el.timestamp) for block_el in self.__chain
                    ]
                ]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        """ Generate a proof of work for the open transactions and the hash of
        the last block """
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        # Try different PoW numbers and return the first valid one
        while not Verification.valid_proof(self.__open_transactions,
                                           last_hash,
                                           proof):
            proof += 1
        return proof

    def get_balance(self, sender=None):
        """ Calculate the amount of coins sent for the participant """
        if sender is None:
            if self.public_key is None:
                return None
            participant = self.public_key
        else:
            participant = sender
        # Fetch a list of all sent coin amounts for the given person
        # (empty lists are acceptable)
        # This fetches sent amounts of transactions that were
        # already included in block
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        # Fetch a list of all sent coin amounts for the given person
        # (empty lists are acceptable)
        # This fetches sent amounts of open transactions
        # (to avoid double spending)
        open_tx_sender = [tx.amount for tx in self.__open_transactions
                          if tx.sender == participant]
        # Add the amount spent in open transactions
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        # Reduce function sums elements and passes into the tx_sum of
        # the lambda arguments and continues to add
        # the sum of tx_amt until empty. This replaces the for loop.
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                             if len(tx_amt) > 0 else tx_sum, tx_sender, 0)
        # This fetches received coin amounts of transactions that were
        # already in the blockchain
        # We ignore open transactions here because you shouldn't
        # be able to spend them
        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant]
                        for block in self.__chain]
        # Reduce function sums elements and passes into the tx_sum of the
        # lambda arguments and continues to add the sum of tx_amt until empty.
        # This replaces the for loop.
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                                 if len(tx_amt) > 0
                                 else tx_sum, tx_recipient, 0)
        # Calculate the total balance of coins for the participant
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain """
        if len(self.__chain) < 1:
            return None
        # Implicit else so no else line required
        return self.__chain[-1]

    # This function accepts two arguments.
    # One required one (transaction_amount) and
    # one optional one (last_transaction)
    # The optional one is optional becuase it has a default value => [1]
    def add_transaction(self,
                        sender,
                        recipient,
                        signature,
                        amount=1.0,
                        is_receiving=False):
        """ Add a new transaction to the list of open transactions

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :signature: The signature of the transaction.
            :amount: The amount of coins sent with the transaction
                     (default = 1.0)
        """
        # if self.public_key == None:
        #     return False
        # OrderedDict remembers the order in which its contents are added
        transaction = Transaction(sender, recipient, signature, amount)
        # If the sender has sufficient balance to send the amount in
        # the transaction, then add to the transaction to mempool
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            # Also inform our peer nodes
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={
                            'sender': sender,
                            'recipient': recipient,
                            'amount': amount,
                            'signature': signature
                        })
                        if (response.status_code == 400 or
                                response.status_code == 500):
                            print('Transaction declined, needs resolving')
                            return False
                    # Continue for the other nodes if there is an error
                    # Don't return False and end the whole set
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        """ Create a new block and add open transactions to it."""
        if self.public_key is None:
            return None
        # Fetch the current last block of the blockchain
        last_block = self.__chain[-1]
        # Hash the last block
        # (=> to be able to compare it to the stroed has value)
        hashed_block = hash_block(last_block)
        # Calculate the proof of work
        proof = self.proof_of_work()
        # Miners should be rewarded, so let's create a reward transaction
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        # OrderedDict remembers the order in which its contents are added
        reward_transaction = Transaction('MINING',
                                         self.public_key,
                                         '',
                                         MINING_REWARD)
        # Copy the open transactions to a new List, instead of manipulating
        # the original open_transactions
        copied_transactions = self.__open_transactions[:]
        # Ensure we are manipulating a local list of transactions
        # not a global one.
        # This ensures that if for some reason the mining should fail,
        # we don't have extra reward transactions included across all nodes
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                # Currently this just prevents mining the block
                # Instead you could remove the invalid transaction from
                # the transaction set and mine the remaining ones
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain),
                      hashed_block,
                      copied_transactions,
                      proof)
        self.__chain.append(block)
        # Reset the open transactions back to empty (clear mempool)
        self.__open_transactions = []
        # Call save data here not inside mine block so open transactions
        # are empty in the file
        self.save_data()
        for node in self.__peer_nodes:
            url = 'http://{}/broadcast-block'.format(node)
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [tx.__dict__ for tx in
                                               converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block):
        transactions = [Transaction(
            tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
            for tx in block['transactions']]
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(block['index'],
                                block['previous_hash'],
                                transactions,
                                block['proof'],
                                block['timestamp'])
        self.__chain.append(converted_block)
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if (opentx.sender == itx['sender'] and
                        opentx.recipient == itx['recipient'] and
                        opentx.amount == itx['amount'] and
                        opentx.signature == itx['signature']):
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was already removed')
        self.save_data()
        return True

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(block['index'],
                                    block['previous_hash'],
                                    [Transaction(tx['sender'],
                                                 tx['recipient'],
                                                 tx['signature'],
                                                 tx['amount'])
                                    for tx in block['transactions']],
                                    block['proof'],
                                    block['timestamp'])
                              for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                if node_chain_length > (local_chain_length and
                                        Verification.verify_chain(node_chain)):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        """ Adds a new node to the peer node set.

        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """ Removes a node from the peer node set.

        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """ Return a list of all connected peer nodes. """
        return list(self.__peer_nodes)
