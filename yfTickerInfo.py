#!/usr/bin/env python3
# pip3 install yfinance

import yfinance as yf
from pprint import pprint
from argparse import ArgumentParser

def delete_if_exists(stock_d, key):
	if key in stock_d:
		del stock_d[key]

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('--symbol', '-s', type=str, required=True)
	args = parser.parse_args()
	yf_symbol = args.symbol.replace('/','-')
	res = yf.Ticker(yf_symbol)

	delete_if_exists(res.info, 'companyOfficers')
	delete_if_exists(res.info, 'longBusinessSummary')
	pprint(res.info)
