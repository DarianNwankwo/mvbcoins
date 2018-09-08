import argparse

from hashlib import sha256

from transaction import Transaction
from utxo import UTXO

TRANSACTION_OCCURRENCE = {str:True}
TRANSACTION_HISTORY = [] # list of transactions

def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("--port", help="Port your node is listening on", required=True)
  parser.add_argument("--peers", help="A comma separated list of peer ports your node will broadcast transactions received to", required=True)
  args = parser.parse_args()
  port, peers = (args.port, args.peers.split(","))
  port, peers = (int(port), [int(peer) for peer in peers])
  return (port, peers)


def parse_ascii_byte_array(ascii_string):
    val = ""
    for i in range(len(ascii_string)//2):
        val += chr(int(ascii_string[ 2*i : 2*i + 2 ], 16))
    
    return int(val)


def parse_transaction(data_as_hex):
  opcode = parse_ascii_byte_array(data_as_hex[0:2])
  sender = data_as_hex[2:66]
  receiver = data_as_hex[66:130]
  amount = parse_ascii_byte_array(data_as_hex[130:194])
  timestamp = parse_ascii_byte_array(data_as_hex[194:258])
  tx = Transaction(opcode, sender, receiver, amount, timestamp)
  print(tx)
  return tx


def is_double_spending(tx):
  """ Returns true if a transaction is an occurrence of double spending. """
  tx_hash = sha256(tx.bytify()).hexdigest()
  return tx_hash in TRANSACTION_OCCURRENCE


def log_transaction(tx):
  """ Stores transaction. """
  TRANSACTION_OCCURRENCE[ sha256(tx.bytify()).hexdigest() ] = True
  TRANSACTION_HISTORY.append(tx)


def handle_transaction(tx):
  """ Initiate coin transfer and update history log. """
  if not is_double_spending(tx):
    UTXO[tx.sender], UTXO[tx.receiver] = UTXO[tx.sender] - tx.amount, UTXO[tx.receiver] + tx.amount
    log_transaction(tx)
    return True
  else:
    # don't handle transaction
    print("\n\Double Spending has occurred!\n\n")
    return False
    

def show_utxo_status():
  # print("Size of UTXO: {}".format(len(UTXO)))
  for account in UTXO:
    print("Account #{}: {} MVBcoins".format(account, UTXO[account]))


def echo_message_to(peers, sock):
  """ Echo valid messages to peer nodes. """
  