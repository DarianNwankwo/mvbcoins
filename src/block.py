"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Block class used to keep track of transactions
"""
from hashlib import sha256


from transaction import Transaction


class Block(object):
  """ Hanldes blocks. """

  def __init__(self, byte_array, difficulty, tx_count):
    if len(byte_array) > 0:
      self.byte_array = byte_array
      # print("First 32 Nonce: {}".format(byte_array[0:32]))
      block_info = self._parse_block(byte_array.hex())
      self.nonce = block_info[0]
      self.prev_hash = block_info[1]
      self.hash = block_info[2]
      self.block_height = block_info[3]
      self.miner_address = block_info[4]
      self.block_data = block_info[5] # transactions
    self.difficulty = difficulty
    self.tx_count = tx_count


  def __str__(self):
    start = 160
    builder =  "Block [ Nonce {}, Prior Hash {}, Hash {}, Blockheight {}, Miner Address {}, Transaction Below ]\n".format(
      self.nonce, self.prev_hash, self.hash, self.block_height, self.miner_address
    )
    for tx in range(tx_count):
      builder += "\t" + Transaction( self.byte_array[start + (128 * tx) : start + (128 * (tx + 1))] ).__str__() + "\n"
    return builder
  

  def _parse_block(self, data_as_hex):
    """ Returns a tuple of the arguments decoded from the raw byte array. """
    # print("Data as hex: {}\n".format(data_as_hex))
    # nonce = self._parse_ascii_byte_array(data_as_hex[0:64])
    nonce = int(data_as_hex[0:64])
    prev_hash = data_as_hex[64:128]
    # cur_hash = data_as_hex[128:192]
    block_height = self._parse_ascii_byte_array(data_as_hex[192:256])
    miner_address = self._parse_ascii_byte_array(data_as_hex[256:320])
    block_data = self._parse_ascii_byte_array(data_as_hex[320:])
    cur_hash = self.calculate_hash()
    return (nonce, prev_hash, cur_hash, block_height, miner_address, block_data)


  def _parse_ascii_byte_array(self, ascii_string):
    """ Parses the nonce, prev_hash, cur_hash, block_height, miner_address, and block_Data and returns the integer representation. """
    # print("Value of Ascii String: {}".format(ascii_string))
    val = ""
    for i in range(len(ascii_string)//2):
      # print("Substring: {}".format(int(ascii_string[ 2*i : 2*i + 2 ], 16)))
      val += chr(int(ascii_string[ 2*i : 2*i + 2 ], 16))
    # print("Val Inside Parse Ascii: {}".format(val))
    return int(val)


  def raw_byte_array(self):
    """ Returns the raw byte array of the block. """
    return self.byte_array


  def calculate_hash(self):
    """ Calculates the hash value of a block. """
    sum_bytes = b""
    for attr, val in vars(self).items():
      if attr not in ('byte_array', 'hash', 'difficulty'):
        sum_bytes += bytes(val, "ascii")
    hashed = sha256(sum_bytes).hexdigest()
    hashed_bytes = bytes.fromhex(hashed)
    self.byte_array = self.byte_array[0:96] + hashed_bytes + self.byte_array[128:] 

    return hashed


  def mine_block(self):
    """ Mines the block until a particular difficulty is achieved. """
    while (self.hash[0:self.difficulty] != "0" * self.difficulty):
      self.nonce += 1
      self.hash = self.calculate_hash()

  
  @classmethod
  def create_genesis_block(cls):
    """ Create a genesis block to start the chain. """
    genesis = Block("", 1, 0)
    genesis.hash = sha256( bytes("0", encoding="ascii") ).hexdigest()
    genesis.prev_hash = sha256( bytes("", encoding="ascii") ).hexdigest()
    genesis.block_height = 0
    return genesis
