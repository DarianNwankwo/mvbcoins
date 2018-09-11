"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Server class for handling socket operations
"""
import socket

from block import Block
from ledger import Ledger
from transaction import Transaction

WAITING_FOR_CONNECTION = True
RECEIVING_DATA = True
BYTES = 1
PAYLOAD = 4096 * BYTES # in bytes
TRANSACTION_OPCODE = "0"
CLOSE_OPCODE = "1"
BLOCK_OPCODE = "2"
GET_BLOCK_OPCODE = "3"
NUM_OF_CONNECT_REQUEST = 5

class Server(object):
  """ Handles opening sockets and lisening for information and broadcasting information. """

  def __init__(self, config):
    """ Open the socket for information retrieval at port <port>.
    
    Arguments:
    config -- a Config object that contains the configuration for the node
    """
    self._unpack(config)
    self.msg_size_mapping = self._create_msg_mapping()
    self.socket = self._create_socket_server()
    self.ledger = Ledger()


  def _unpack(self, config):
    """ Unpacks the config object and creates instance variables. """
    self.node_ip = config.node_ip
    self.port = int(config.port)
    self.peers = [int(peer) for peer in config.peers]
    self.tx_per_block = int(config.tx_per_block)
    self.difficulty = int(config.difficulty)
    self.num_of_cores = int(config.num_of_cores)


  def _create_msg_mapping(self):
    """ Returns an array such that if indexed with the opcode of a message it returns the message size in bytes. """
    return [
      128*BYTES,
      0*BYTES,
      (160 + (128 * self.tx_per_block))*BYTES,
      32*BYTES
    ]


  def _create_socket_server(self):
    """ Opens the server at node_ip as a TCP/IP socket server for receiving messages. """
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_socket.bind( (self.node_ip, self.port) )
    node_socket.listen(NUM_OF_CONNECT_REQUEST)
    return node_socket


  def _still_handling_data(self, data):
    """ Return true if data is still being received. """
    return data != b""


  def _listen(self):
    """ Listens for a connection and corresponding raw bytes. """
    while WAITING_FOR_CONNECTION:
      # Helper variables
      msg_end_ndx = 0
      data = b""
      is_first = True
      print("Waiting for a connection...")
      connection, client_address = self.socket.accept()
      try:
        # When msg_start_ndx == msg_end_ndx this returns an empty byte (b"")
        while is_first or self._still_handling_data( data[msg_start_ndx : msg_end_ndx] ):
          print("looping...")
          is_first = False
          data += connection.recv(PAYLOAD) # buffered data
          if data:
            print("Data received: {}".format(data))
            cur_opcode = chr(int(data[0:1].hex(), 16)) # bytearray -> hex -> int -> ascii
            msg_start_ndx = 1
            msg_end_ndx = msg_start_ndx + self.msg_size_mapping[ int(cur_opcode) ]
            if cur_opcode == TRANSACTION_OPCODE:
              tx = Transaction(data[msg_start_ndx : msg_end_ndx])
              self.ledger.process_transaction(tx)
            elif cur_opcode == CLOSE_OPCODE:
              # handle close
              self.terminate_server()
              break
            elif cur_opcode == BLOCK_OPCODE:
              # handle block
              block = Block(data[msg_start_ndx : msg_end_ndx], self.difficulty)
              self.ledger.process_block(block)
            elif cur_opcode == GET_BLOCK_OPCODE:
              # handle get block
              # get_block = self.ledger.get_block(block_height)
              self.ledger.process_get_block(data[msg_start_ndx : msg_end_ndx])
            data = data[msg_end_ndx:] # dump processed data from buffer
          else:
            break
      finally:
        # end connection with client
        self.ledger.show_utxo_status()
        connection.close()

  def terminate_server(self):
    """ Stop receiving data on port (terminate socket). """
    self.socket.close()


  def _echo_message_to(self, peers, data):
    """ Echo valid messages to peer nodes. """
    for peer in peers:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect( ("localhost", int(peer)) )
      sock.sendall(data)
      sock.close()


  def broadcast_transaction(self):
    pass

  
  def broadcast_block(self):
    pass


  def run(self):
    """ Creeate and run server instance. """
    self._listen()