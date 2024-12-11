#!/usr/bin/env python3
# pip3 install yfinance

import json
import datetime
import yfinance as yf
from pprint import pprint
from argparse import ArgumentParser

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('--symbol', '-s', type=str, required=True)
	args = parser.parse_args()
	res = yf.Ticker(args.symbol)

	pprint(res.calendar)

	my_list = []
	earnings_date_array = res.calendar['Earnings Date']
	for e in earnings_date_array:
		my_list.append(f'{e}')

	json_str = json.dumps(my_list)
	print(json_str)

	now = datetime.date.today()
	new_list = json.loads(json_str)
	for d in new_list:
		dt_obj = datetime.date.fromisoformat(d)
		print(dt_obj - now)
