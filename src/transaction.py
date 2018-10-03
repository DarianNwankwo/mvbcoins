"""
Author: Darian Osahar Nwankwo
Date: September 5, 2018
Description: Transaction class for handling transactions
"""
from hashlib import sha256


from helper import ascii_to_int


class Transaction(object):
  """ Hanldes the hashing and processing of raw bytes that represent a transaction. """


  OPCODE_START                     = 0
  OPCODE_END     = SENDER_START    = 1
  SENDER_END     = RECEIVER_START  = 33
  RECEIVER_END   = AMOUNT_START    = 65
  AMOUNT_END     = TIMESTAMP_START = 97
  TIMESTAMP_END                    = 129


  def __init__(self, byte_array):
    """ Stores the bytearray and arguments of it. """
    self.byte_array = byte_array
    self.opcode, self.sender, self.receiver, self.amount, self.timestamp = self.parse_transaction(byte_array.hex())

  
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
    b = self.byte_array
    return sha256( b[Transaction.SENDER_START:Transaction.TIMESTAMP_END] ).digest()

  

  def parse_transaction(self, data_as_hex):
    """ Returns a tuple of the arguments decoded from the hex representation of the raw byte array. """
    opcode = data_as_hex[0:2]
    sender = data_as_hex[2:66]
    receiver = data_as_hex[66:130]
    amount = ascii_to_int(data_as_hex[130:194])
    timestamp = ascii_to_int(data_as_hex[194:258])
    return (opcode, sender, receiver, amount, timestamp)