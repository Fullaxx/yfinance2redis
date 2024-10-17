#!/usr/bin/env python3
# pip3 install yfinance

import yfinance as yf
#from pprint import pprint
from argparse import ArgumentParser

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('--symbol', '-s', type=str, required=True)
	args = parser.parse_args()
	res = yf.Ticker(args.symbol)

	for method in dir(res):
		if not method.startswith('__'):
			print(method)
