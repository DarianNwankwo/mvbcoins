"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Block class used to keep track of transactions
"""
from hashlib import sha256
from random import getrandbits


from helper import add_byte_padding, ascii_to_int, block_data_exist, block_has_structure
from transaction import Transaction

# figure out why difficulkty is increasing

class Block(object):
  """ Hanldes blocks. """

  TRANSACTION_START = 161

  def __init__(self, byte_array, difficulty, block_tx_capacity):
    self.byte_array = byte_array
    self.difficulty, self.block_tx_capacity = difficulty, block_tx_capacity
    # input("Difficulty (b): {}".format(self.difficulty))
    self.opcode, self.nonce, self.prev_hash, self.hash, self.block_height, self.miner_address, self.block_data = self.parse_block(byte_array.hex())


  def __str__(self):
    start = 160
    builder =  "Block [ Nonce {}, Prior Hash {}, Hash {}, Blockheight {}, Miner Address {}, Transaction Below ]\n".format(
      self.byte_array[1:33], self.byte_array[33:65].hex(), self.byte_array[65:97].hex(), self.byte_array[97:129], self.miner_address
    )
    for tx in range(self.block_tx_capacity):
      builder += "\t" + Transaction( self.byte_array[start + (128 * tx) : start + (128 * (tx + 1))] ).__str__() + "\n"
    return builder
  

  def parse_block(self, data_as_hex):
    """ Returns a tuple of the arguments decoded from the raw byte array. """
    # print("Data as hex: {}\n".format(data_as_hex))
    # nonce = self._parse_ascii_byte_array(data_as_hex[0:64])
    block_data = b""
    if not block_data_exist(self.byte_array, Block.TRANSACTION_START):
      block_data = data_as_hex[322:]
    elif block_has_structure(self.byte_array, Block.TRANSACTION_START):
      block_data = ""
    opcode = data_as_hex[0:2]
    nonce = data_as_hex[2:66]
    prev_hash = data_as_hex[66:130]
    cur_hash = data_as_hex[128:192]
    block_height = data_as_hex[194:258]
    miner_address = data_as_hex[258:322]
    # cur_hash = self.calculate_hash()
    return (opcode, nonce, prev_hash, cur_hash, block_height, miner_address, block_data)


  @classmethod
  def generate_block(cls, difficulty, block_tx_capacity, height, prev_block_hash):
    opcode = bytes("2", "ascii")
    nonce = add_byte_padding( bytes("1", "ascii"), 32 )
    prev_hash = prev_block_hash
    block_height = add_byte_padding( bytes( str(height), "ascii" ), 32 )
    miner_addr = add_byte_padding( bytes("don4", "ascii"), 32 )
    block_data = b""
    cur_hash = sha256(bytes("0", "ascii")).digest()
    # print("Previous Hash in Unmined Block: {}".format(prev_hash.hex()))
    data = opcode + nonce + prev_hash + cur_hash + block_height + miner_addr + block_data
    return Block(data, difficulty, block_tx_capacity)


  def raw_byte_array(self):
    """ Returns the raw byte array of the block. """
    return self.byte_array


  def calculate_hash(self):
    """ Calculates the hash value of a block. """
    self.byte_array = self.byte_array[0:65] + sha256( self.byte_array[1:65] + self.byte_array[97:] ).digest() + self.byte_array[97:]


  def update_nonce(self):
    """ Randomly generates a nonce. """
    self.byte_array = self.byte_array[0:1] + getrandbits(32*8).to_bytes(32, "big") + self.byte_array[33:]


  def add_transaction(self, tx_bytes):
    """ Adds the 128B representing a transaction, excluding the opcode. """
    self.byte_array += tx_bytes[1:]
    return self.mine()


  def mine(self):
    """ Mines the block until a particular difficulty is achieved. Returns false if block is not ready to be mined. """
    num_txs = len(self.byte_array[161:]) // 128
    # print("Tx count: {}".format(num_txs))
    if num_txs == self.block_tx_capacity:
      # input("Difficulty: {}".format(self.difficulty))
      # print("Hash: {}".format(self.hash))
      while ("00" * self.difficulty != self.byte_array[65:65 + self.difficulty].hex()):
        # print("0s == self.byte_array[65:65 + self.difficulty]: {} == {}".format("00"*self.difficulty, self.byte_array[65:65 + self.difficulty].hex()))
        self.update_nonce()
        self.calculate_hash()
      self.hash = self.byte_array[65:97].hex()
      # print("Final hash: {}".format(self.byte_array[65:97].hex()))
      # print("Nonce: {}".format(int(self.byte_array[1:33].hex(), 16)))
      # input()
      # print("Difficulty (b): {}".format(self.difficulty))
      # self.update()
      # print("Difficulty (a): {}".format(self.difficulty))
      return True
    elif num_txs > self.block_tx_capacity:
      print("Txs should not be higher than capacity.")
      return False
    return False
    # input("Final Hash: {}".format(self.hash))


  def update(self):
    self.opcode, self.nonce, self.prev_hash, self.hash, self.block_height, self.miner_address, self.block_data = self.parse_block(self.byte_array.hex())
    self.nonce = int(self.nonce, 16)
    self.block_height = ascii_to_int(self.block_height)
