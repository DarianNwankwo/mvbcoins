from hashlib import sha256
from constants import INIT_PAYOUT

def create_utxo_set():
  utxo = {}
  for integer in range(100):
    account = sha256( bytes(str(integer), encoding="ascii") )
    utxo[account.hexdigest()] = INIT_PAYOUT
  return utxo


UTXO = create_utxo_set()