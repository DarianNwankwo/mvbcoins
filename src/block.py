class Block(object):

  def __init__(self, timestamp, transactions, previousHash):
    self.timestamp = timestamp
    self.transactions = transactions
    self.previousHash = previousHash