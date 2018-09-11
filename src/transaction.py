"""
Author: Darian Osahar Nwankwo
Date: September 5, 2018
Description: Transaction class for handling transactions
"""

class Transaction(object):
  """ Hanldes the hashing and processing of raw bytes that represent a transaction. """

  def __init__(self, byte_array):
    """ Stores the bytearray and arguments of it. """
    self.byte_array = byte_array
    tx_info = self.parse_transaction(byte_array.hex())
    self.opcode = tx_info[0]
    self.sender = tx_info[1]
    self.receiver = tx_info[2]
    self.amount = tx_info[3]
    self.timestamp = tx_info[4]

  
  def __str__(self):
    """ Pretty printing of transaction for debugging purposes. """
    return "\nOpcode: {} -- Sender: {} -- Receiver: {} -- Amount: {} -- Timestamp: {}\n".format(
      self.opcode, self.sender, self.receiver, self.amount, self.timestamp
    )
  

  def raw_byte_array():
    """ Returns the raw byte array of the transaction. """
    return self.byte_array


  def calculate_hash(self):
    """ Calculates the hash value of a transaction. """
    sum_bytes = b""
    for attr, val in vars(self):
      sum_bytes += bytes(val, "ascii")
    return sha256(sum_bytes).hexdigest()


  @classmethod
  def should_close(cls, opcode_bytes):
    """ Returns """
    opcode = opcode_bytes.hex()
    opcode = Transaction.parse_ascii_byte_array(opcode)
    return opcode == 1
  

  def parse_transaction(self, data_as_hex):
    """ Returns a tuple of the arguments decoded from the raw byte array. """
    opcode = Transaction.parse_ascii_byte_array(data_as_hex[0:2])
    sender = data_as_hex[2:66]
    receiver = data_as_hex[66:130]
    amount = Transaction.parse_ascii_byte_array(data_as_hex[130:194])
    timestamp = Transaction.parse_ascii_byte_array(data_as_hex[194:258])
    return (opcode, sender, receiver, amount, timestamp)


  @classmethod
  def parse_ascii_byte_array(cls, ascii_string):
    """ Parses the opcode, amount, and timestamp and returns the integer representation. """
    val = ""
    for i in range(len(ascii_string)//2):
        val += chr(int(ascii_string[ 2*i : 2*i + 2 ], 16))
    return int(val)
