#!/usr/bin/env python3

from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
import os
import time


parser = ArgumentParser(description="Crawl Bitcoin Unlimited explorer to retrieve block transactions")
parser.add_argument('ipath', type=str, help="/path/to/file/containing/block/hashes")
parser.add_argument('opath', help="/path/to/dir/for/output/files")
parser.add_argument('-t', '--timeout', type=float, help="time to wait (in seconds) for transaction ids to load (default: 1 second)", default=1)
parser.add_argument('-n', '--no-headless', action='store_true', default=False, help="do not run Firefox headless (default: run headless)")

args = parser.parse_args()

try:
    assert(os.path.exists(args.ipath) and os.path.exists(args.opath))
except AssertionError as e:
    print(">> ERROR : input and/or output path(s) invalid")
    exit(-1)

print(">> INFO -- reading input file <{}>".format(args.ipath))
blockhashes = []
with open(args.ipath, 'r') as f:
    for line in f:
        line = line.rstrip()
        assert(len(line) == 64)
        blockhashes.append(line)
print(">> INFO -- input file <{}> read successfully".format(args.ipath))

opath = '{}{}out'.format(args.opath, os.sep)
if not os.path.exists(opath):
    print(">> INFO -- creating dir <{}> for output files".format(opath))
    os.mkdir(opath)

options = Options()
if not args.no_headless:
    options.headless = True
driver = webdriver.Firefox(options=options)

print(">> INFO -- crawling Bitcoin Unlimited explorer for block transactions")
for blockhash in tqdm(blockhashes):
    baseurl = "https://explorer.bitcoinunlimited.info/block/"
    driver.get('{}{}'.format(baseurl, blockhash))
    elem = driver.find_element_by_partial_link_text("JSON")
    elem.click()
    elem = driver.find_element_by_partial_link_text("Transaction IDs")
    elem.click()
    time.sleep(args.timeout)
    elem = driver.find_elements_by_tag_name("code")
    htmltxids = elem[1].get_attribute("innerHTML").split(",")
    with open('{}{}{}'.format(opath, os.sep, blockhash), 'w') as f:
        for e in htmltxids:
            txid = e.split('"')[3]
            assert(len(txid) == 64)
            f.write(txid + "\n")
