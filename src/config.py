"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: Config class for handling arguments received from the command line
"""
import argparse

class Config(object):
  """ Handles command line arguments received and should be passed to a server object. """

  def __init__(self, node_ip):
    self.port, self.peers, self.tx_per_block, self.difficulty, self.num_of_cores = self._parse_arguments()
    self.node_ip = node_ip


  def _parse_arguments(self):
    """ Retreive arguments from the command line to configure the node. """
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Port your node is listening on", required=True)
    parser.add_argument("--peers", help="A comma separated list of peer ports your node will broadcast transactions received to", required=True)
    parser.add_argument("--numtxinblock", help="The number of transactions to be put in a block. Defaults to 50,000", required=False, default=50000)
    parser.add_argument("--difficulty", help="Difficulty parameter. This is the number of leading bytes that must be zero during mining", required=True)
    parser.add_argument("--numcores", help="The number of cores your node supports", required=True)
    args = parser.parse_args()
    return (args.port, args.peers.split(","), args.numtxinblock, args.difficulty, args.numcores)