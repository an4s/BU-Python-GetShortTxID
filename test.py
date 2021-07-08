#!/usr/bin/env python3

from GetShortTxID import GetShortTxID
import os

test_status = True
with open('test_data{}blockhashes'.format(os.sep), 'r') as f:
    for line in f:
        blockhash = line.rstrip()
        assert(len(blockhash) == 64)
        file_content = None
        with open('test_data{}blockshorttxids{}{}{}txids'.format(os.sep, os.sep, blockhash, os.sep), 'r') as t:
            file_content = [line.rstrip() for line in t]
            assert(len(file_content) >= 4)
            this_shorttxidk0 = int(file_content[0])
            this_shorttxidk1 = int(file_content[1])
            this_shorttxids = set()
            for shorttxid in file_content[3:]:
                this_shorttxids.add(int(shorttxid))
            shorttxid2txhash = dict()
            with open('test_data{}out{}{}'.format(os.sep, os.sep, blockhash), 'r') as b:
                for line in b:
                    txhash = line.rstrip()
                    shorttxid = GetShortTxID(this_shorttxidk0, this_shorttxidk1, txhash)
                    if shorttxid in this_shorttxids:
                        assert(shorttxid not in shorttxid2txhash)
                        shorttxid2txhash[shorttxid] = txhash
                if len(shorttxid2txhash) != len(this_shorttxids):
                    test_status = False
                    print(">> ERROR : not all shorttxids could be resolved to full tx hashes for block <{}>".format(blockhash))

print(">> Test", ("passed" if test_status else "failed"))
