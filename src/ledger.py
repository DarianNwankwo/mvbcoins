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
    self.blocks = [ Block.generate_block(block_difficulty, tx_per_block, 0, sha256(bytes("0", "ascii")).digest()) ] # array of block objects
    self.tx_per_block = tx_per_block
    self.block_difficulty = block_difficulty

    
  def _create_utxo_set(self):
    """ Creates NUM_OF_ACCOUNTS account ids by hashing the byte string of numbers in range(NUM_OF_ACCOUNTS). """
    utxo = {}
    for integer in range(NUM_OF_ACCOUNTS):
      account = sha256( bytes(str(integer), encoding="ascii") )
      utxo[account.hexdigest()] = INITIAL_PAYOUT
    return utxo


  def add_transaction_to_block(self, tx):
    """ Adds a transaction to the latest unmined block. """
    return self.blocks[ len(self.blocks) - 1 ].add_transaction( tx.raw_byte_array() )


  def add_transaction(self, tx):
    """ Initiate coin transfer and update history log via a Transaction object and returns true if we should broadcast. """
    if self.is_valid_transaction(tx):
      self.update_utxo(tx)
      self.update_tx_occurrence(tx)
      print("Adding tx...")
      block_is_mined = self.add_transaction_to_block(tx)
      if block_is_mined:
        # create a new block
        # print("Block mined: {}".format(self.blocks[ len(self.blocks) - 1 ]))
        # print("Adding a new block that is unmined...")
        prev_hash = self.get_prev_hash()
        self.blocks.append(
          Block.generate_block(self.block_difficulty, self.tx_per_block, len(self.blocks), prev_hash)
        )
        # print("Blocks in Ledger: {}".format(len(self.blocks)))
        # print("Previous Block Hash: {}".format(self.get_prev_hash().hex()))
      return True, block_is_mined
    else:
      # raise an error
      # print("\nSomeone is attempting to double spend...\n")
      return False, False


  def get_prev_hash(self):
    return self.blocks[ len(self.blocks) - 1 ].raw_byte_array()[65:97]


  def get_block(self, block_height):
    """ Return the byte array of a block at block_height. """
    if block_height <= len(self.blocks):
      return self.blocks[block_height]


  def is_valid_transaction(self, tx):
    """ Given a transaction object and UTXO set, returns true if the transaction is valid. """
    return self.user_has_funds(tx) and self.user_does_exist(tx) and not self.is_double_spending(tx)


  def show_utxo_status(self):
    """ (Debugging Purposes) Display all accounts and their money. """
    for account in self.utxo:
      print("Account #{}: {} MVBcoins".format(account, self.utxo[account]))


  def user_has_funds(self, tx):
    """ Returns true if the sender has enough coins to send. """
    return self.utxo[tx.sender] - tx.amount >= 0


  def user_does_exist(self, tx):
    """ Returns true if the sender and receiver exist. """
    return tx.sender in self.utxo and tx.receiver in self.utxo


  def is_double_spending(self, tx):
    """ Returns true if a transaction is an occurrence of double spending. """
    return tx.calculate_hash() in self.tx_occurrence


  def update_utxo(self, tx):
    """ Given a transaction and utxo set, update the utxo set. """
    self.utxo[tx.sender] = self.utxo[tx.sender] - tx.amount
    self.utxo[tx.receiver] = self.utxo[tx.receiver] + tx.amount


  def update_tx_occurrence(self, tx):
    """ Given a transaction and a dictionary mapping of transactions to true, update the mapping with a new transaction. """
    self.tx_occurrence[ tx.calculate_hash() ] = True
