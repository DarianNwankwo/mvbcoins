"""
Author: Darian Osahar Nwankwo
Date: October 3, 2018
Description: Helper methods for node
"""
def ascii_to_int(ascii_string):
  """ Returns the integer representation of an ascii string that has been decoded into a hex string.
  
  ex: b"1010" (raw bytes) ==> "31303130" (hex, ascii_string) ==> "1010" (str) ==> 1010
  """
  val = ""
  length = len(ascii_string) // 2
  for i in range(length):
      start, end = 2*i, 2*i + 2
      # Grabs two characters since ascii to hex takes 2B to represent the ascii value
      val += chr( int( ascii_string[start:end], 16 ) )
  return int(val)

def is_valid_transaction(tx, utxo, tx_occurrence):
  """ Given a transaction object and UTXO set, returns true if the transaction is valid. """
  return user_has_funds(tx, utxo) and user_does_exist(tx, utxo) and not is_double_spending(tx, tx_occurrence)


def user_has_funds(tx, utxo):
  """ Returns true if the sender has enough coins to send. """
  print(utxo)
  for account in utxo:
      print("Account #{}: {} MVBcoins".format(account, self.utxo[account]))
  return utxo[tx.sender] - tx.amount >= 0


def user_does_exist(tx, utxo):
  """ Returns true if the sender and receiver exist. """
  return tx.sender in utxo and tx.recevier in utxo


def is_double_spending(tx, tx_occurrence):
  """ Returns true if a transaction is an occurrence of double spending. """
  return tx.calculate_hash() in tx_occurrence


def update_utxo(tx, utxo):
  """ Given a transaction and utxo set, update the utxo set. """
  print(utxo)
  utxo[tx.sender] = utxo[tx.sender] - tx.amount
  utxo[tx.receiver] = utxo[tx.receiver] + tx.amount
  return utxo


def update_tx_occurrence(tx, tx_occurrence):
  """ Given a transaction and a dictionary mapping of transactions to true, update the mapping with a new transaction. """
  tx_occurrence[ tx.calculate_hash() ] = True
  return tx_occurrence


def update_tx_history(tx, tx_history):
  """ Given a transaction and transaction history list, add the transaction to the history. """
  tx_history.append( tx.raw_byte_array() )
  return tx_history


def block_data_exist(block_bytes, block_data_start):
  """ Returns true if the bytes representing a block has transactions. """
  return len(block_bytes) > block_data_start


def block_has_structure(block_bytes, block_data_start):
  """ Returns true if the block has the prereqs to be a block besides block data. """
  return len(block_bytes) == block_data_start