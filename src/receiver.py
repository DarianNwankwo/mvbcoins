"""
Author: Darian Osahar Nwankwo
Date: September 5, 2018
Description: A minimally viable implementation of bitcoin. The current implementation sets
up a server and receives messages using sockets.
"""
import socket

from transaction import Transaction
from utxo import UTXO

from constants import *
from helper import *


NODE_PORT, PEER_NODE_PORTS = parse_arguments()

def create_socket_server(node_ip, port):
  """ Opens the server at node_ip as a TCP/IP socket server for receiving messages. """
  node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  node_socket.bind( (node_ip, port) ) # Bind the socket to port
  node_socket.listen(NUM_OF_CONNECT_REQUEST)
  return node_socket


def listen(sock):
  """ Listens for a connection and corresponding raw bytes"""
  while True:
    print("Waiting for a connection...")
    connection, client_address = sock.accept()
    try:
      while True:
        data = connection.recv(129) # data received as raw bytearray
        # Do something only if we've recevied data
        if data:
          tx = Transaction(data)
          if tx.close(): break
          valid = handle_transaction(tx) # consider having a ledger class handle this
          if valid:
            # print(PEER_NODE_PORTS)
            log_transaction(tx)
            echo_message_to(PEER_NODE_PORTS, data)
        else:
          break
    finally:
      show_utxo_status()
      connection.close()


def main():
  # print("Node: {} -- Peer Nodes: {}".format(NODE_PORT, PEER_NODE_PORTS))
  node_socket = create_socket_server('localhost', NODE_PORT)
  listen(node_socket)
    
if __name__ == "__main__":
  main()
