"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Server class for handling socket operations
"""
import socket
import time


from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock
from queue import Queue


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
BACKLOG = 5
NUM_OF_WORKERS = 4
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
    self.unpack(config)
    self.msg_size_mapping = self.create_msg_mapping()
    self.socket = self.create_socket_server()
    self.ledger = Ledger(self.tx_per_block, self.difficulty)
    self.queue = Queue()
    self.getter_threads = []
    self.worker_threads = []
    self.mutex = Lock()



  def unpack(self, config):
    """ Unpacks the config object and creates instance variables. """
    self.node_ip = config.node_ip
    self.port = int(config.port)
    self.peers = [int(peer) for peer in config.peers]
    self.tx_per_block = int(config.tx_per_block)
    self.difficulty = int(config.difficulty)
    # self.num_of_cores = int(config.num_of_cores)


  def create_msg_mapping(self):
    """ Returns an array such that if indexed with the opcode of a message it returns the message size in bytes. """
    return [
      128*BYTES,
      0*BYTES,
      (160 + (128 * self.tx_per_block))*BYTES,
      32*BYTES
    ]


  def create_socket_server(self):
    """ Opens the server at node_ip as a TCP/IP socket server for receiving messages. """
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    node_socket.bind( (self.node_ip, self.port) )
    node_socket.listen(BACKLOG)
    return node_socket


  def receive_data_from(self, connection, address):
    """ Receive data from a connection until all data has been received. """
    
    data = b""
    while True:
      data = connection.recv(1)
      if data:
        ndx = int(data.hex(), 16) - 48
        data += connection.recv( self.msg_size_mapping[ndx] )
        self.mutex.acquire()
        self.process_data(data)
        self.mutex.release()
        data = b""
      else:
        return True

  def handle_transaction_message(self, data):
    """ Handles a bytearray and processes it as a transaction message. Returns true if it is valid. """
    tx = Transaction(data) # ignores opcode
    # print(tx)
    echo_tx, echo_block = self.ledger.add_transaction(tx)
    return echo_tx, echo_block


  def handle_close_message(self, data):
    """ Handles a bytearray and processes it as a close message. Returns true if it is valid. """
    echo_close, echo_block = True, True
    return echo_close, echo_block


  def handle_block_message(self, data):
    """ Handles a bytearray and processes it as a block message. Returns true if it is valid. """
    # block = Block(data, self.difficulty, self.tx_per_block)
    echo_received_block, echo_block = True, False
    return echo_received_block, echo_block


  def handle_get_block_message(self, data):
    """ Handles a bytearray and processes it as a get block message. Returns false since the message does not need to be broadcast. """
    # TODO fix this
    block_height = data[OPCODE_OFFSET : msg_end_ndx]
    # self.ledger.process_get_block(block_height)
    return False, None


  
  def parse_message(self, data):
    """ Receive data from a connection until all data has been received. """
    cur_opcode = from_byte_to_char(data[0:1])
    # print("Data: {}".format(data))
    if cur_opcode == TRANSACTION_OPCODE:
      echo_data, echo_block = self.handle_transaction_message(data)
    elif cur_opcode == CLOSE_OPCODE:
      echo_data, echo_block = self.handle_close_message(data)
    elif cur_opcode == BLOCK_OPCODE:
      echo_data, echo_block = self.handle_block_message(data)
    elif cur_opcode == GET_BLOCK_OPCODE:
      echo_data, echo_block = self.handle_get_block_message(data)
      
    

  def listen(self):
    """ Listens for a connection and corresponding raw bytes. """
    # self.broadcast_to_peers(self.ledger.blocks[0].raw_byte_array())
    while WAITING_FOR_CONNECTION:
      print("Waiting for a connection...")
      print("-" * 100)
      # Create a thread to handle data receiver
      connection, addr = self.socket.accept()
      connection.settimeout(60 * SECONDS)
      # self.receive_data_from(connection, addr)
      new_thread = Thread(target=self.receive_data_from, args=(connection, addr,))
      new_thread.start()
      # self.getter_threads.append( new_thread )

      # Create a thread to handle work == the number of cores used
      # do = True
      # if do:
      #   print("Executing...worker")
      #   worker_thread = Thread(target=self.process_data, args=())
      #   worker_thread.start()
      #   self.worker_threads.append(worker_thread)
      #   do = False
      
      # self.handle_data_from_connection(connection, addr)
      print("Blocks in Ledger: {}".format(len(self.ledger.blocks)))
      print("-" * 100)


  def process_data(self, data):
    self.parse_message(data) # determines what to do with the message


  def broadcast_to_peers(self, data):
    """ Echo valid messages to peer nodes as bytearray. """
    for peer in self.peers:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      peer_addr = ("localhost", int(peer))
      try:
        sock.connect(peer_addr)
        sock.sendall(data)
      except:
        print("Connection error on broadcast...")
      finally:
        sock.close()


  def start(self):
    """ Creeate and run server instance. """
    self.listen()
