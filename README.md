# Bitcoin Unlimited Python GetShortTxID
A Python implementation of the GetShortTxID function in the Bitcoin Unlimited software

## Motivation
Bitcoin Unlimited implements the [Graphene](https://gitlab.com/bitcoinunlimited/BCHUnlimited/-/blob/dev/doc/graphene-specification-v2.2.mediawiki) protocol which reduces the 32-byte transaction hashes to 7-byte short ids which are then included in blocks represented by [IBLTs](https://ieeexplore.ieee.org/abstract/document/6120248). If the receiver of a block [misses](https://ieeexplore.ieee.org/abstract/document/8751297) some transactions from the block, it sends the 7-byte short ids of the missing transactions to the sender of the block. The latter then looks up which of the transactions in the block corresponds to the short ids sent by the former and returns the full transactions.

It may be necessary to resolve the short ids to the full transaction hashes for, say, some experiments. One method is to resolve them from [within the Bitcoin Unlimited software](https://github.com/an4s/bitcoinunlimited_shortidresolver). However, this method requires running a full node with all blocks downloaded and transactions indexed. This repository provides an alternative: a Python script, named GetShortTxID, that removes the requirement for running a full node. Provided blockhashes and all transactions present in that block, the script can be run to find out which full transaction hashes correspond to the provided short tx ids.

Since the aforementiond script requires all transactions within a block to be present, another Python script, named GetBlockTxs, is provided that scraps the [Bitcoin Unlimited Explorer](https://explorer.bitcoinunlimited.info/) to acquire transactions present in the block. Path to a file containing hashes of blocks of interest must be provided to the script. The script requires [selenium](https://www.selenium.dev/) for which install instructions are provided [here](https://selenium-python.readthedocs.io/installation.html).

A test script along with test data is provided to check the functionality of the GetShortTxID function.
