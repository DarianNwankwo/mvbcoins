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
    for tx in range(self.tx_count):
      builder += "\t" + Transaction( self.byte_array[start + (128 * tx) : start + (128 * (tx + 1))] ).__str__() + "\n"
    return builder
  

  def _parse_block(self, data_as_hex):
    """ Returns a tuple of the arguments decoded from the raw byte array. """
    # print("Data as hex: {}\n".format(data_as_hex))
    # nonce = self._parse_ascii_byte_array(data_as_hex[0:64])
    # print("Nonce before: {}\n".format(data_as_hex[0:64]))
    nonce = self._parse_ascii_byte_array(data_as_hex[0:64])
    prev_hash = data_as_hex[64:128]
    # cur_hash = data_as_hex[128:192]
    # print("Block Height (HEX): {}".format(data_as_hex[192:256]))
    block_height = self._parse_ascii_byte_array(data_as_hex[192:256])
    # print("Block Height (INT): {}".format(block_height))
    miner_address = self._parse_ascii_byte_array_to_str(data_as_hex[256:320])
    # print("\nBlock Data: {}\n".format(data_as_hex[320:]))
    block_data = data_as_hex[320:]
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


  def _parse_ascii_byte_array_to_str(self, ascii_string):
    """ Parses the nonce, prev_hash, cur_hash, block_height, miner_address, and block_Data and returns the integer representation. """
    # print("Value of Ascii String: {}".format(ascii_string))
    val = ""
    for i in range(len(ascii_string)//2):
      # print("Substring: {}".format(int(ascii_string[ 2*i : 2*i + 2 ], 16)))
      val += chr(int(ascii_string[ 2*i : 2*i + 2 ], 16))
    # print("Val Inside Parse Ascii: {}".format(val))
    return str(val)


  def raw_byte_array(self):
    """ Returns the raw byte array of the block. """
    return bytes("2", "ascii") + self.byte_array


  def calculate_hash(self):
    """ Calculates the hash value of a block. """
    sum_bytes = b""
    for attr, val in vars(self).items():
      if attr not in ('byte_array', 'hash', 'difficulty', 'tx_count'):
        # print("Val: {}".format(val))
        sum_bytes += bytes(str(val), "ascii")
    hashed = sha256(sum_bytes).hexdigest()
    hashed_bytes = bytes.fromhex(hashed)
    # print("Hashed Bytes: {}\n".format(hashed_bytes))
    self.byte_array = self.byte_array[0:64] + hashed_bytes + self.byte_array[96:]
    # print("Byte Array of Block: {}\n".format(self.byte_array))

    return hashed


  def mine_block(self):
    """ Mines the block until a particular difficulty is achieved. """
    # print("\nMining...")
    while (self.hash[0:(self.difficulty*2)] != "00" * self.difficulty):
      self.nonce += 1
      self.hash = self.calculate_hash()
    # print("Byte array before update: {}".format(self))
    self.byte_array = self._add_byte_padding(bytes(str(self.nonce), "ascii"), 32) + self.byte_array[32:]
    # print("Byte array after update: {}".format(self))
    # print("Final Hash - As Bytes: {}\n".format(self.hash, self.byte_array[96:128]))


  def _add_byte_padding(self, byte_val, width):
    """ Adds padding to a bytearray to fit message size. """
    # print((width - len(bytes(byte_val))))
    # print(bytes(byte_val))
    return (width - len(bytes(byte_val))) * bytes("0", "ascii") + bytes(byte_val)

  
  @classmethod
  def create_genesis_block(cls, tx_count):
    """ Create a genesis block to start the chain. """
    # TODO: Actually create a real block
    nonce = (0).to_bytes(32, "big")
    prior_hash = bytes.fromhex("0" * 32)
    cur_hash = bytes.fromhex( sha256(bytes("100", "ascii")).hexdigest() )
    blockheight = (0).to_bytes(32, "big")
    miner_addr = bytes([0]) * 28 + bytes("don4", "ascii")
    block_data = b""
    data = nonce + prior_hash + cur_hash + blockheight + miner_addr + block_data
    return Block(data, 1, 0)
