"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Ledger class for handling utxo operations and keeping track of the history. Functionally
equivalent to what is know as a 'blockchain.'
"""
from hashlib import sha256


from block import Block


NUM_OF_ACCOUNTS = 100
INITIAL_PAYOUT = int("100,000".replace(",", ""))


class Ledger(object):
  """ Handles verifying transaction and keeping a history of each transaction. """

  def __init__(self, tx_per_block, block_difficulty):
    self.utxo = self._create_utxo_set()
    self.tx_occurrence = {} # dict{str: bool}
    self.tx_history = [] # array of raw bytes
    self.blocks = [ Block.create_genesis_block() ]
    self.tx_per_block = tx_per_block
    self.block_difficulty = block_difficulty


  def _create_utxo_set(self):
    """ Creates NUM_OF_ACCOUNTS account ids by hashing the byte string of numbers in range(NUM_OF_ACCOUNTS). """
    utxo = {}
    for integer in range(NUM_OF_ACCOUNTS):
      account = sha256( bytes(str(integer), encoding="ascii") )
      utxo[account.hexdigest()] = INITIAL_PAYOUT
    return utxo


  def is_double_spending(self, tx):
    """ Returns true if a transaction is an occurrence of double spending. """
    return tx.calculate_hash() in self.tx_occurrence
  

  def log_transaction(self, tx):
    """ Stores transaction. """
    self.tx_occurrence[ tx.calculate_hash() ] = True
    self.tx_history.append( tx.raw_byte_array() )


  def log_block(self, block):
    """ Stores block. """
    # self.block_occurrence[ block.calculate_hash() ] = True
    self.block_history.append( block.raw_byte_array() )


  def _user_does_exist(self, tx):
    """ Returns true if the user exists. """
    return tx.sender in self.utxo and tx.receiver in self.utxo


  def _user_has_funds(self, tx):
    """ Returns true if the sender has enough coins to send, """
    return self.utxo[tx.sender] - tx.amount >= 0


  def process_transaction(self, tx):
    """ Initiate coin transfer and update history log via a Transaction object and returns true if we should broadcast. """
    if not self.is_double_spending(tx) and self._user_does_exist(tx) and self._user_has_funds(tx):
      self.utxo[tx.sender] = self.utxo[tx.sender] - tx.amount
      self.utxo[tx.receiver] = self.utxo[tx.receiver] + tx.amount
      self.log_transaction(tx)
      # Mine a block
      if len(self.tx_history) == self.tx_per_block:
        block_to_broadcast = self.mine()
        del self.tx_history
        self.tx_history = []
        return True, block_to_broadcast
      return True, None
    else:
      # raise an error
      print("\nSomeone is attempting to double spend...\n")
      return False, None


  def mine(self):
    """ Mine a new block. """
    # Create a new block by concatenating tx history together and pass that to the block constructor along with difficulty
    # A Block contains a nonce, prior hash, blockheight, miner-address, and blockdata
    nonce = self._add_byte_padding( bytes([1]), 32 )
    prior_hash = bytes.fromhex(self.blocks[ len(self.blocks) - 1 ].hash)
    blockheight = self._add_byte_padding( bytes([ len(self.blocks) ]), 32 )
    miner_addr = self._add_byte_padding( bytes("don4", encoding="ascii"), 32 )
    blockdata = b"".join(self.tx_history)
    print("Type: {}".format(type(nonce)))
    print("Type: {}".format(type(prior_hash)))
    print("Type: {}".format(type(blockheight)))
    print("Type: {}".format(type(miner_addr)))
    print("Type: {}".format(type(blockdata)))
    data = nonce + prior_hash + blockheight + miner_addr + blockdata
    new_block = Block(data, self.block_difficulty, self.tx_per_block)
    new_block.mine_block()
    return new_block


  def _add_byte_padding(self, byte_val, width):
    """ Adds padding to a bytearray to fit message size. """
    return (width - len(bytes(byte_val))) * bytes([0]) + bytes(byte_val)


  def process_block(self, block):
    """ Initiate block proof-of-work (mining) and update history log via a Block object. """
    self.log_block(block)
    return True


  def process_get_block(self, block_height):
    """ Return the byte array of a block at block_height. """
    return self.blocks[block_height]


  def process_close(self):
    """ Returns true. """
    return True

  def get_block(self, block_height):
    if block_height <= len(self.blocks):
      return self.blocks[block_height - 1]


  def show_utxo_status(self):
    """ (Debugging Purposes) Display all accounts and their money. """
    for account in self.utxo:
      print("Account #{}: {} MVBcoins".format(account, self.utxo[account]))