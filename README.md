# Bitcoin Unlimited Python GetShortTxID
A Python implementation of the GetShortTxID function in the Bitcoin Unlimited software

## Motivation
Bitcoin Unlimited implements the [Graphene](https://gitlab.com/bitcoinunlimited/BCHUnlimited/-/blob/dev/doc/graphene-specification-v2.2.mediawiki) protocol which reduces the 32-byte transaction hashes to 7-byte short ids which are then included in blocks represented by [IBLTs](https://ieeexplore.ieee.org/abstract/document/6120248). If the receiver of a block [misses](https://ieeexplore.ieee.org/abstract/document/8751297) some transactions from the block, it sends the 7-byte short ids of the missing transactions to the sender of the block. The latter then looks up which of the transactions in the block corresponds to the short ids sent by the former and returns the full transactions.

It may be necessary to resolve the short ids to the full transaction hashes for, say, some experiments. One method is to resolve them from [within the Bitcoin Unlimited software](https://github.com/an4s/bitcoinunlimited_shortidresolver). However, this method requires running a full node with all blocks downloaded and transactions indexed. This repository provides an alternative: a Python script, named `GetShortTxID`, that removes the requirement for running a full node. Provided block hashes and all transactions present in that block, the script can be run to find out which full transaction hashes correspond to the provided short tx ids.

Since the aforementiond script requires all transactions within a block to be present, another Python script, named `GetBlockTxs`, is provided that scraps the [Bitcoin Unlimited Explorer](https://explorer.bitcoinunlimited.info/) to acquire transactions present in the block. Path to a file containing hashes of blocks of interest must be provided to the script. The script requires [selenium](https://www.selenium.dev/) for which install instructions are provided [here](https://selenium-python.readthedocs.io/installation.html).

## Usage

A test script along with test data is provided to check the functionality of the GetShortTxID function. The directory `blockshorttxids` contains subdirectories where the label of each subdirectory is the hash of a block. Within each subdirectory is a file containing the [left and right halves of the SipHash key](https://gitlab.com/bitcoinunlimited/BCHUnlimited/-/blob/dev/doc/graphene-specification-v2.2.mediawiki#CGrapheneSet), `shorttxidk0` and `shorttxidk1` respectively, and the short tx ids of transactions which need to be resolved. For each full transaction hash in the block of interest, call the function `GetShortTxID(shorttxidk0, shorttxidk1, fulltxhash)` to find the short tx id of the hash. Check if this short tx id is present in the file corresponding to the block hash.

## Epilogue

Please provide feedback on the tool and report issues, if you find any. Your contributions are welcome!
