#!/usr/bin/env python3
"""
Author: Darian Osahar Nwankwo
Date: September 10, 2018
Description: A minimally viable implementation of bitcoin. The current implementation sets
up a server and receives messages using sockets.
"""
from config import Config
from server import Server

if __name__ == "__main__":
  config = Config("localhost")
  node = Server(config)
  node.run() # or, more succinctly Server(Config("localhost")).run()