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
NUM_OF_CONNECT_REQUEST = 10
OPCODE_OFFSET = 1
SECONDS = 1

def from_byte_to_char(byte_val):
  """ Returns the char representation of a byte object. """
  return chr(int(byte_val.hex(), 16)) # bytearray -> hex -> int -> char(ascii)


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
    self.ledger = Ledger(self.tx_per_block, self.difficulty)


  def _unpack(self, config):
    """ Unpacks the config object and creates instance variables. """
    self.node_ip = config.node_ip
    self.port = int(config.port)
    self.peers = [int(peer) for peer in config.peers]
    self.tx_per_block = int(config.tx_per_block)
    self.difficulty = int(config.difficulty)
    # self.num_of_cores = int(config.num_of_cores)


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


  def _receive_from(self, connection, address):
    """ Receive data from a connection until all data has been received. """
    incoming = connection.recv(PAYLOAD)
    data = b""
    while incoming:
      data += incoming
      incoming = connection.recv(PAYLOAD)
    return data


  def _handle_transaction(self, data):
    """ Handles a bytearray and processes it as a transaction message. Returns true if it is valid. """
    tx = Transaction(data) # ignores opcode
    print(tx)
    broadcast, block = self.ledger.process_transaction(tx)
    return broadcast, block


  def _handle_close(self, data):
    """ Handles a bytearray and processes it as a close message. Returns true if it is valid. """
    return self.ledger.process_close(), None


  def _handle_block(self, data):
    """ Handles a bytearray and processes it as a block message. Returns true if it is valid. """
    block = Block(data, self.difficulty, self.tx_per_block)
    broadcast = self.ledger.process_block(block)
    return broadcast, None


  def _handle_get_block(self, data):
    """ Handles a bytearray and processes it as a get block message. Returns false since the message does not need to be broadcast. """
    self.ledger.process_get_block(data[OPCODE_OFFSET : msg_end_ndx])
    return False, None


  def _get_message(self, data, opcode):
    """ Returns the messages (bytes) given a data buffer (bytearray) and opcode. """
    msg_end_ndx = OPCODE_OFFSET + self.msg_size_mapping[ int(opcode) ]
    return data[OPCODE_OFFSET : msg_end_ndx], msg_end_ndx


  def _handle_data(self, data, opcode):
    """ Returns true if given message is valid. """
    if opcode == TRANSACTION_OPCODE:
      return self._handle_transaction(data)
    elif opcode == CLOSE_OPCODE:
      return self._handle_close(data)
    elif opcode == BLOCK_OPCODE:
      return self._handle_block(data)
    elif opcode == GET_BLOCK_OPCODE:
      return self._handle_get_block(data)

  
  def _handle_data_from_connection(self, connection, address):
    """ Receive data from a connection until all data has been received. """
    data = self._receive_from(connection, address)
    should_broadcast = False
    while len(data) > 0:
      cur_opcode = from_byte_to_char(data[0:1])
      msg, msg_end_ndx = self._get_message(data, cur_opcode)      
      # print("Message and Opcode: {} -- {}".format(msg, cur_opcode))
      should_broadcast, block_data = self._handle_data(msg, cur_opcode)
      if should_broadcast and block_data:
        self._broadcast_to_peers(msg)
        self._broadcast_to_peers(block_data.raw_byte_array())
      elif should_broadcast:
        self._broadcast_to_peers(msg)
      if cur_opcode == CLOSE_OPCODE:
        # print("Closing connection...")
        connection.close()
        exit() 
      data = data[msg_end_ndx:] # dump processed data from buffer


  def _listen(self):
    """ Listens for a connection and corresponding raw bytes. """
    while WAITING_FOR_CONNECTION:
      print("Waiting for a connection...")
      connection, addr = self.socket.accept()
      # print("Connection: {}\n".format(connection))
      connection.settimeout(60 * SECONDS)
      self._handle_data_from_connection(connection, addr)
      # self.ledger.show_utxo_status()


  def _broadcast_to_peers(self, data):
    """ Echo valid messages to peer nodes. """
    for peer in self.peers:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect( ("localhost", int(peer)) )
      sock.sendall(data)
    sock.close()


  def start(self):
    """ Creeate and run server instance. """
    self._listen()
