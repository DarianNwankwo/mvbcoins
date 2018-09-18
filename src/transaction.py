"""
Author: Darian Osahar Nwankwo
Date: September 5, 2018
Description: Transaction class for handling transactions
"""
from hashlib import sha256

class Transaction(object):
  """ Hanldes the hashing and processing of raw bytes that represent a transaction. """

  def __init__(self, byte_array):
    """ Stores the bytearray and arguments of it. """
    self.byte_array = byte_array
    tx_info = self._parse_transaction(byte_array.hex())
    self.sender = tx_info[0]
    self.receiver = tx_info[1]
    self.amount = tx_info[2]
    self.timestamp = tx_info[3]

  
  def __str__(self):
    """ Pretty printing of transaction for debugging purposes. """
    return "Transaction [ Sender {}, Receiver {}, Amount {}, Timestamp {} ]".format(
      self.sender, self.receiver, self.amount, self.timestamp
    )
  

  def raw_byte_array(self):
    """ Returns the raw byte array of the transaction. """
    return self.byte_array


  def calculate_hash(self):
    """ Calculates the hash value of a transaction based on sender, receiver, amount, and timestamp. """
    sum_bytes = b""
    for attr, val in vars(self).items():
      if attr != "byte_array":
        # print("\nVal - Attr: {} - {}\n".format(val, attr))
        # print("{}".format(attr != "byte_array"))
        sum_bytes += bytes(str(val), "ascii")
    return sha256(sum_bytes).hexdigest()
  

  def _parse_transaction(self, data_as_hex):
    """ Returns a tuple of the arguments decoded from the raw byte array. """
    sender = data_as_hex[0:64]
    receiver = data_as_hex[64:128]
    amount = self._parse_ascii_byte_array(data_as_hex[128:192])
    timestamp = self._parse_ascii_byte_array(data_as_hex[192:256])
    # print("\nOutput: {}\n".format((sender, receiver, amount, timestamp)))
    return (sender, receiver, amount, timestamp)


  def _parse_ascii_byte_array(self, ascii_string):
    """ Parses the amount and timestamp and returns the integer representation. """
    val = ""
    for i in range(len(ascii_string)//2):
        val += chr(int(ascii_string[ 2*i : 2*i + 2 ], 16))
    return int(val)