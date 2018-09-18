"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Server class for handling socket operations
"""
import socket
import threading

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
    self.threads = []
    self.thread_lock = threading.Lock()


  def _unpack(self, config):
    """ Unpacks the config object and creates instance variables. """
    self.node_ip = config.node_ip
    self.port = int(config.port)
    self.peers = [int(peer) for peer in config.peers]
    # self.tx_per_block = int(config.tx_per_block)
    # self.difficulty = int(config.difficulty)
    # self.num_of_cores = int(config.num_of_cores)


  def _create_msg_mapping(self):
    """ Returns an array such that if indexed with the opcode of a message it returns the message size in bytes. """
    return [
      128*BYTES,
      0*BYTES,
      # (160 + (128 * self.tx_per_block))*BYTES,
      # 32*BYTES
    ]


  def _create_socket_server(self):
    """ Opens the server at node_ip as a TCP/IP socket server for receiving messages. """
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_socket.bind( (self.node_ip, self.port) )
    node_socket.listen(NUM_OF_CONNECT_REQUEST)
    return node_socket


  def _handle_data_from_connection(self, connection, address):
    """ Receive data from a connection until all data has been received. """
    self.thread_lock.acquire()
    data = self._receive_from(connection, address)
    # input("Size of Data and Counter: {}".format(len(data)))
    while len(data) > 0:
      cur_opcode = chr(int(data[0:1].hex(), 16)) # bytearray -> hex -> int -> char(ascii)
      msg_end_ndx = OPCODE_OFFSET + self.msg_size_mapping[ int(cur_opcode) ]
      if cur_opcode == TRANSACTION_OPCODE:
        tx = Transaction(data[OPCODE_OFFSET : msg_end_ndx]) # ignores opcode
        print(tx)
        broadcast = self.ledger.process_transaction(tx)
      elif cur_opcode == CLOSE_OPCODE:
        # handle close
        broadcast = True
      elif cur_opcode == BLOCK_OPCODE:
        # handle block
        block = Block(data[OPCODE_OFFSET : msg_end_ndx], self.difficulty)
        broadcast = self.ledger.process_block(block)
      elif cur_opcode == GET_BLOCK_OPCODE:
        # handle get block
        # get_block = self.ledger.get_block(block_height)
        self.ledger.process_get_block(data[OPCODE_OFFSET : msg_end_ndx])
      
      if broadcast:
        self._echo_message_to(data[0 : msg_end_ndx])
      print("\nData Buffer Before: {}\n".format(data))
      data = data[msg_end_ndx:] # dump processed data from buffer
      print("\nData Buffer After: {}\n".format(data))
      # input()
    self.ledger.show_utxo_status()
    self.thread_lock.release()

  def _receive_from(self, connection, address):
    """ Receive data from a connection until all data has been received. """
    incoming = connection.recv(PAYLOAD)
    data = b""
    while incoming:
      data += incoming
      incoming = connection.recv(PAYLOAD)
    return data


  def _listen(self):
    """ Listens for a connection and corresponding raw bytes. """
    while WAITING_FOR_CONNECTION:
      # Helper variables
      print("Waiting for a connection...")
      connection, addr = self.socket.accept()
      connection.settimeout(60*SECONDS)
      t = threading.Thread(target=self._handle_data_from_connection, args=(connection, addr,))
      self.threads.append(t)
      t.start()


  def _echo_message_to(self, data):
    """ Echo valid messages to peer nodes. """
    # print("\nBroadcast: {}\n".format(Transaction(data[1:])))
    print("Broadcast Data and Peers: {} and {}".format(data,
	self.peers))
    for peer in self.peers:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect( ("", int(peer)) )
      sock.send(data)
    sock.close()


  def broadcast_transaction(self):
    pass

  
  def broadcast_block(self):
    pass


  def run(self):
    """ Creeate and run server instance. """
    self._listen()
