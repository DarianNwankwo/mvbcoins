"""
Author: Darian Osahar Nwankwo
Date: October 3, 2018
Description: Helper methods for node
"""
def ascii_to_int(ascii_string):
  """ Returns the integer representation of an ascii string that has been decoded into a hex string.
  
  ex: b"1010" (raw bytes) ==> "31303130" (hex, ascii_string) ==> "1010" (str) ==> 1010
  """
  val = ""
  length = len(ascii_string) // 2
  for i in range(length):
      start, end = 2*i, 2*i + 2
      # Grabs two characters since ascii to hex takes 2B to represent the ascii value
      val += chr( int( ascii_string[start:end], 16 ) )
  return int(val)


def block_data_exist(block_bytes, block_data_start):
  """ Returns true if the bytes representing a block has transactions. """
  return len(block_bytes) > block_data_start


def block_has_structure(block_bytes, block_data_start):
  """ Returns true if the block has the prereqs to be a block besides block data. """
  return len(block_bytes) == block_data_start


def add_byte_padding(byte_val, width):
  """ Adds padding to a bytearray to fit message size. """
  # print((width - len(bytes(byte_val))))
  # print(bytes(byte_val))
  return (width - len(bytes(byte_val))) * bytes("0", "ascii") + bytes(byte_val)