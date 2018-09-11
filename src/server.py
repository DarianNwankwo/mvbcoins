"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Server class for handling socket operations
"""
import socket

from block import Block
from ledger import Ledger
from transaction import Transaction
from constants import NUM_OF_CONNECT_REQUEST

WAITING_FOR_CONNECTION = True
RECEIVING_DATA = True
PAYLOAD = 4096 # in bytes


class Server(object):
  """ Handles opening sockets and lisening for information and broadcasting information. """


  def __init__(self, config):
    """ Open the socket for information retrieval at port <port>.
    
    Arguments:
    config -- a Config object that contains the configuration for the node
    """
    self.config = config
    self.socket = self._create_socket_server()
    self.cur_opcode_ndx = 0
    self.utxo = Ledger()


  def _create_socket_server(self):
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_socket.bind( (self.node_ip, self.port) )
    node_socket.listen(NUM_OF_CONNECT_REQUEST)
    return node_socket


  def _listen(self):
    """ Listens for a connection and corresponding raw bytes. """
    while WAITING_FOR_CONNECTION:
      print("Waiting for a connection...")
      try:
        while RECEIVING_DATA:
          data = connection.recv(PAYLOAD)
          print("Data received: {}".format(data))

  
  def _process_transaction(self):
    pass


  def _process_block(self):
    pass


  def _terminate_server(self):
    pass

  
  def _get_block(self, ):
    pass


  def run(self):
    pass