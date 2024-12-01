#!/usr/bin/env python3

import sys
import json
from pprint import pprint
from argparse import ArgumentParser

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def bailmsg(*args, **kwargs):
	eprint(*args, **kwargs)
	sys.exit(1)

def process_spark(spark):
	if (spark['error'] == None):
		resultarray = spark['result']
#		pprint(resultarray)
		for item in resultarray:
			this_symbol = item['symbol']
			if (this_symbol == g_target_symbol):
				pprint(item)

def process_quote(quoteResponse):
	if (quoteResponse['error'] == None):
		resultarray = quoteResponse['result']
#		pprint(resultarray)
		for item in resultarray:
			this_symbol = item['symbol']
			if (this_symbol == g_target_symbol):
				pprint(item)
#				pprint(item['regularMarketPrice'])
#				pprint(item['regularMarketPreviousClose'])
#				pprint(item['postMarketPrice'])

def process_body(body_str):
	quote = json.loads(body_str)
#	pprint(quote)
	if ('quoteResponse' in quote):
		process_quote(quote['quoteResponse'])
	if ('spark' in quote):
		process_spark(quote['spark'])

def process_resource(resource_str):
	resource = json.loads(resource_str)
#	pprint(resource)
	if (resource['status'] == 200):
		process_body(resource['body'])

if __name__ == '__main__':
	global g_target_symbol

	parser = ArgumentParser()
	parser.add_argument('--file', '-f', type=str, required=True)
	parser.add_argument('--symbol', '-s', type=str, required=True)
	args = parser.parse_args()
	g_target_symbol = args.symbol

	with open(args.file) as f:
		for line in f:
			resource_str = line.strip('\n')
			process_resource(resource_str)
