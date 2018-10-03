"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Block class used to keep track of transactions
"""
from hashlib import sha256
from random import getrandbits


from helper import ascii_to_int, block_data_exist, block_has_structure
from transaction import Transaction


class Block(object):
  """ Hanldes blocks. """

  TRANSACTION_START = 161

  def __init__(self, byte_array, difficulty, tx_count):
    self.byte_array = byte_array
    self.difficulty, self.tx_count = difficulty, tx_count
    self.nonce, self.prev_hash, self.hash, self.block_height, self.miner_address, self.block_data = self.parse_block(byte_array.hex())


  def __str__(self):
    start = 160
    builder =  "Block [ Nonce {}, Prior Hash {}, Hash {}, Blockheight {}, Miner Address {}, Transaction Below ]\n".format(
      self.nonce, self.prev_hash, self.hash, self.block_height, self.miner_address
    )
    for tx in range(self.tx_count):
      builder += "\t" + Transaction( self.byte_array[start + (128 * tx) : start + (128 * (tx + 1))] ).__str__() + "\n"
    return builder
  

  def parse_block(self, data_as_hex):
    """ Returns a tuple of the arguments decoded from the raw byte array. """
    # print("Data as hex: {}\n".format(data_as_hex))
    # nonce = self._parse_ascii_byte_array(data_as_hex[0:64])
    if not block_data_exist(self.byte_array, Block.TRANSACTION_START):
      block_data = data_as_hex[322:]
    elif block_has_structure(self.byte_array, Block.TRANSACTION_START):
      block_data = ""
    opcode = data_as_hex[0:2]
    nonce = int(data_as_hex[2:66])
    prev_hash = data_as_hex[66:130]
    # cur_hash = data_as_hex[128:192]
    block_height = int(data_as_hex[194:258])
    miner_address = ascii_to_int(data_as_hex[258:322])
    cur_hash = self.calculate_hash()
    return (nonce, prev_hash, cur_hash, block_height, miner_address, block_data)


  @classmethod
  def create_genesis_block(cls):
    return


  def raw_byte_array(self):
    """ Returns the raw byte array of the block. """
    return self.byte_array


  def calculate_hash(self):
    """ Calculates the hash value of a block. """
    b = self.byte_array
    return sha256( b[1:129] + b[161:] ).digest()


  def update_nonce(self):
    """ Randomly generates a nonce. """
    self.byte_array = self.byte_array[0] + getrandbits(32*8).to_bytes(32, "big") + self.byte_array[1:33]


  def mine(self):
    """ Mines the block until a particular difficulty is achieved. """
    while (bytes(self.difficulty) == self.hash[0:self.difficulty]):
      self.update_nonce()
      self.hash = self.calculate_hash()
    self.byte_array = self.byte_array[0:65] + self.hash + self.byte_array[97:]
    return True
    # input("Final Hash: {}".format(self.hash))
