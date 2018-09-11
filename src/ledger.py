"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Ledger class for handling utxo operations and keeping track of the history. Functionally
equivalent to what is know as a 'blockchain.'
"""
from hashlib import sha256

NUM_OF_ACCOUNTS = 100
INITIAL_PAYOUT = int("100,000".replace(",", ""))

class Ledger(object):
  """ Handles verifying transaction and keeping a history of each transaction. """

  def __init__(self):
    self.utxo = self._create_utxo_set()
    self.tx_occurrence = {} # dict{str: bool}
    self.tx_history = [] # array of raw bytes
    self.blocks = []


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


  def process_transaction(self, tx):
    """ Initiate coin transfer and update history log via a Transaction object. """
    if not self.is_double_spending(tx):
      self.utxo[tx.sender] = self.utxo[tx.sender] - tx.amount
      self.utxo[tx.receiver] = self.utxo[tx.receiver] + tx.amount
      self.log_transaction(tx)
      return True
    else:
      # raise an error
      print("\nSomeone is attempting to double spend...\n")
      return False

  
  def process_block(self, block):
    """ Initiate block proof-of-work (mining) and update history log via a Block object. """
    self.log_block(block)


  def process_get_block(self, block_height):
    """ Return the byte array of a block at block_height. """
    return self.blocks[block_height]


  def get_block(self, block_height):
    if block_height <= len(self.blocks):
      return self.blocks[block_height - 1]


  def show_utxo_status(self):
    """ (Debugging Purposes) Display all accounts and their money. """
    for account in self.utxo:
      print("Account #{}: {} MVBcoins".format(account, self.utxo[account]))