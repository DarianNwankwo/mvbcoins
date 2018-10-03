"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Ledger class for handling utxo operations and keeping track of the history. Functionally
equivalent to what is know as a 'blockchain.'
"""
from hashlib import sha256


from block import Block
from helper import is_valid_transaction, update_utxo, update_tx_occurrence, update_tx_history, create_genesis_block

NUM_OF_ACCOUNTS = 100
INITIAL_PAYOUT = int("100,000".replace(",", ""))


class Ledger(object):
  """ Handles verifying transaction and keeping a history of each transaction. """

  def __init__(self, tx_per_block, block_difficulty):
    self.utxo = self._create_utxo_set()
    self.tx_occurrence = {} # dict{str: bool}
    self.tx_history = [] # array of raw bytes
    self.blocks = [ create_genesis_block() ] # array of block objects
    self.tx_per_block = tx_per_block
    self.block_difficulty = block_difficulty
    self.blocks = [ ]
    # self.blocks = [  ]

    


  def _create_utxo_set(self):
    """ Creates NUM_OF_ACCOUNTS account ids by hashing the byte string of numbers in range(NUM_OF_ACCOUNTS). """
    utxo = {}
    for integer in range(NUM_OF_ACCOUNTS):
      account = sha256( bytes(str(integer), encoding="ascii") )
      utxo[account.hexdigest()] = INITIAL_PAYOUT
    return utxo


  def log_block(self, block):
    """ Stores block. """
    # self.block_occurrence[ block.calculate_hash() ] = True
    # print("\n\nUpdating blocks\n\n")
    self.blocks.append( block )


  def process_transaction(self, tx):
    """ Initiate coin transfer and update history log via a Transaction object and returns true if we should broadcast. """
    if is_valid_transaction(tx, self.utxo, self.tx_occurrence):
      self.utxo = update_utxo(tx, self.utxo)
      self.tx_occurrence = update_tx_occurrence(tx, self.tx_occurrence)
      self.tx_history = update_tx_history(tx, self.tx_history)
      # Mine a block
      if len(self.tx_history) == self.tx_per_block:
        block_to_broadcast = self.mine()
        self.log_block(block_to_broadcast)
        del self.tx_history
        self.tx_history = []
        return True, block_to_broadcast
      return True, None
    else:
      # raise an error
      # print("\nSomeone is attempting to double spend...\n")
      return False, None


  def mine(self):
    """ Mine a new block. """
    # Create a new block by concatenating tx history together and pass that to the block constructor along with difficulty
    # A Block contains a nonce, prior hash, blockheight, miner-address, and blockdata
    if (len(self.blocks) == 0):
      prior_hash = sha256(bytes("0", "ascii")).digest()
    else:
      prior_hash = bytes.fromhex(self.blocks[ len(self.blocks) - 1 ].hash)
    nonce = self._add_byte_padding( bytes("1", "ascii"), 32 )
    cur_hash = self._add_byte_padding(bytes([0]), 32)
    # print(len(self.blocks))
    # blockheight = self._add_byte_padding( bytes([ len(self.blocks) ]), 32 )
    blockheight = self._add_byte_padding( bytes( str( len( self.blocks ) ), "ascii" ), 32 )
    miner_addr = self._add_byte_padding( bytes("don4", encoding="ascii"), 32 )
    blockdata = b"".join(self.tx_history) # concatenates raw byte history
    data = nonce + prior_hash + cur_hash + blockheight + miner_addr + blockdata
    new_block = Block(data, self.block_difficulty, self.tx_per_block)
    new_block.mine_block()
    # print("Newly Created Block: {}Newly Created Block (bytes): {}\n".format(new_block, new_block.raw_byte_array()))
    return new_block



  def _add_byte_padding(self, byte_val, width):
    """ Adds padding to a bytearray to fit message size. """
    # print((width - len(bytes(byte_val))))
    # print(bytes(byte_val))
    return (width - len(bytes(byte_val))) * bytes("0", "ascii") + bytes(byte_val)


  def process_block(self, block):
    """ Initiate block proof-of-work (mining) and update history log via a Block object. """
    # print("\nCalling process_block\n")
    self.log_block(block)
    return True


  def process_get_block(self, block_height):
    """ Return the byte array of a block at block_height. """
    print(self.get_block(block_height))
    return self.get_block(block_height)


  def process_close(self):
    """ Returns true. """
    return True

  def get_block(self, block_height):
    if block_height <= len(self.blocks):
      return self.blocks[block_height]


  def show_utxo_status(self):
    """ (Debugging Purposes) Display all accounts and their money. """
    for account in self.utxo:
      print("Account #{}: {} MVBcoins".format(account, self.utxo[account]))