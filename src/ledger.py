"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Ledger class for handling utxo operations and keeping track of the history
"""

from hashlib import sha256
from constants import INIT_PAYOUT

class Ledger(object):

  def __init__(self):
    self.utxo = self.create_utxo_set()
    self.tx_occurrence = {} # dict{str: bool}
    self.tx_history = [] # array of raw bytes

  def create_utxo_set(self):
    utxo = {}
    for integer in range(100):
      account = sha256( bytes(str(integer), encoding="ascii") )
      utxo[account.hexdigest()] = INIT_PAYOUT
    return utxo


UTXO = create_utxo_set()