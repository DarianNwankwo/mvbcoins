class Transaction(object):

  def __init__(self, opcode, sender, receiver, amount, timestamp):
    self.opcode = opcode
    self.sender = sender
    self.receiver = receiver
    self.amount = amount
    self.timestamp = timestamp

  
  def __str__(self):
    return "\nOpcode: {} -- Sender: {} -- Receiver: {} -- Amount: {} -- Timestamp: {}\n".format(
      self.opcode, self.sender, self.receiver, self.amount, self.timestamp
    )
  
  def bytify(self):
    """ Get the byte representation of each transaction component wise"""
    opcode = str(self.opcode).encode("utf-8")
    sender = str(self.sender).encode("utf-8")
    receiver = str(self.sender).encode("utf-8")
    amount = str(self.amount).encode("utf-8")
    timestamp = str(self.timestamp).encode("utf-8")
    return bytes(opcode) + bytes(sender) + bytes(receiver) + bytes(amount) + bytes(timestamp)

  def close(self):
    return self.opcode == 1