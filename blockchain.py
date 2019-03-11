# Initializing our (empty) blockchain list
MINING_REWARD = 10

GENESIS_BLOCK = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [GENESIS_BLOCK]
open_transactions = []
owner = 'Jorge'
participants = {'Jorge'}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participant):
    # Calculate the amount of coins sent for the participant
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] ==  participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    # Add the amount spent in open transactions
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    # Calculate the amount of coins received for the participant
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] ==  participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]

    # Calculate the balance of coins for the participant
    return amount_received - amount_sent


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    # Implicit else so no else line required
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    # Returns Boolean 
    return sender_balance >= transaction['amount']


# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional becuase it has a default value => [1]
def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add a new transaction to the list of open transactions

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: The amount of coins sent with the transaction (default = 1.0)

    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    # If the sender has sufficient balance to send the amount in the transaction, then add to the transaction to mempool
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        # Add sender and recipient to list of blockchain participants
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    # Copy the open transactions to a new List
    copied_transactions = open_transactions[:]
    # Ensure we are manipulating a local list of transactions not a global one e.g. mining reward can be accepted/rejected
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    # Get the user input, transform it from a string to a float and store in
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    """ Verify the current blockchain and return True if its valid, False otherwise. """
    for (index, block) in enumerate(blockchain):
        if index == 0:
            # Genesis block cannot be modified since the hash is confirmed in the first block
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain values')
    print('4: Output the blockchain participants')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data= get_transaction_value()
        recipient, amount = tx_data
        # Add the transaction to the blockchain
        if add_transaction(recipient, amount=amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            # Reset the open transactions back to empty (clear mempool)
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'h':
        # Make sure that you don't try to "hack" the blockchain if it's empty
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Jorge', 'amount': 100.0}]
            }
    elif user_choice == 'q':
        # This will lead the loop to exit because its running condition is no longer true
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        # Break out of the loop
        break
    print(get_balance('Jorge'))
else:
    print('User left!')
      
print('Done!')