#!/usr/bin/env python
#
# Analyzed a single blockchain transaction
#
# References (TTD: should maybe go on main page)
#   https://en.bitcoin.it/wiki/Protocol_documentation#tx
#   http://upcoder.com/8/fast-blockchain-scanning/
#   http://www.righto.com/2014/02/bitcoins-hard-way-using-raw-bitcoin.html
#   https://en.wikipedia.org/wiki/Endianness

import sys
from bc_classes import *

def examine_transaction(argv):
    if len(argv) != 2:
        print('Usage: %s FILENAME'%argv[0])
        exit(0)

    f = open(argv[1], 'r')
    trans_hex = f.read().rstrip()
    f.close()
    #print('Transaction is %s characters'%len(trans_hex))
    #prthex(trans_hex)

    tx = BC_Transaction(trans_hex, 0)
    print('Transaction was %s hex digits long'%tx.len)
    tx.display(indent='  ')

examine_transaction(sys.argv)
