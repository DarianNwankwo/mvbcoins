import argparse
import socket

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


def is_double_spending(tx):
  """ Returns true if a transaction is an occurrence of double spending. """
  tx_hash = sha256(tx.bytify()).hexdigest()
  return tx_hash in TRANSACTION_OCCURRENCE


def log_transaction(tx):
  """ Stores transaction. """
  TRANSACTION_OCCURRENCE[ sha256(tx.bytify()).hexdigest() ] = True
  TRANSACTION_HISTORY.append(tx.byte_array)


def handle_transaction(tx):
  """ Initiate coin transfer and update history log. """
  if not is_double_spending(tx):
    UTXO[tx.sender], UTXO[tx.receiver] = UTXO[tx.sender] - tx.amount, UTXO[tx.receiver] + tx.amount
    return True
  else:
    # don't handle transaction
    print("\n\Double Spending has occurred!\n\n")
    return False
    

def show_utxo_status():
  """ (Debugging Purposes) Display all accounts and their money. """
  # print("Size of UTXO: {}".format(len(UTXO)))
  for account in UTXO:
    print("Account #{}: {} MVBcoins".format(account, UTXO[account]))


def echo_message_to(peers, data):
  """ Echo valid messages to peer nodes. """
  msg = data
  for peer in peers:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", int(peer)))
    sock.sendall(msg)
    sock.close()
  
