#!/usr/bin/env python3

from argparse import ArgumentParser
from selenium import webdriver
from tqdm import tqdm
import os
import time


parser = ArgumentParser(description="Crawl Bitcoin Unlimited explorer to retrieve block transactions")
parser.add_argument('ipath', type=str, help="/path/to/file/containing/block/hashes")
parser.add_argument('opath', help="/path/to/dir/for/output/files")
parser.add_argument('-t', '--timeout', type=float, help="time to wait (in seconds) for transaction ids to load (default: 1 second)", default=1)
parser.add_argument('-n', '--no-headless', action='store_true', default=False, help="do not run browser in headless mode (default: run in headless mode)")
parser.add_argument('-c', '--use-chrome', action='store_true', default=False, help="use chrome browser to scrap data")
parser.add_argument('-e', '--use-edge', action='store_true', default=False, help="use edge browser to scrap data")

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

driver = None
if args.use_chrome:
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.headless = not args.no_headless
    driver = webdriver.Chrome(options=options)
elif args.use_edge:
    from msedge.selenium_tools import EdgeOptions, Edge
    options = EdgeOptions()
    options.use_chromium = True
    if not args.no_headless:
        options.add_argument("--headless")
        options.add_argument("disable-gpu")
    driver = Edge(options=options)
else:
    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.headless = not args.no_headless
    driver = webdriver.Firefox(options=options)

assert(driver is not None)

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
