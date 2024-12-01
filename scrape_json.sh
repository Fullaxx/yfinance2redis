#!/bin/bash

set -e

if [ -z "$1" ]; then
  >&2 echo "$0: <SYMBOL>"
  exit 1
fi

SYMBOL="$1"
QUOTE_URL="https://finance.yahoo.com/quote/${SYMBOL}"

CURL_OPT=""
#CURL_OPT="-4"
#CURL_OPT="-6"
#CURL_OPT+=" --user-agent Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.1"
CURL_OPT+=" --user-agent Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604"

rm -rf ${SYMBOL}
mkdir ${SYMBOL}
pushd ${SYMBOL}

# Download compressed resource
curl "${CURL_OPT}" "${QUOTE_URL}" >${SYMBOL}.zq

# Find the script blocks
zcat ${SYMBOL}.zq | sed -e "s@</script>@</script>\n@g" | sed -e "s@<script @\n<script @g" | grep 'data-url="https://query1.finance.yahoo.com/v7/finance/quote' >${SYMBOL}.quotescript.txt
zcat ${SYMBOL}.zq | sed -e "s@</script>@</script>\n@g" | sed -e "s@<script @\n<script @g" | grep 'data-url="https://query1.finance.yahoo.com/v7/finance/spark' >${SYMBOL}.sparkscript.txt

# extract the JSON objects
grep "symbols=${SYMBOL}" ${SYMBOL}.quotescript.txt | sed -e "s@>{@>\n{@g" |  sed -e "s@}</script>@}\n</script>@g" | grep -Ev '<script|script>' >${SYMBOL}.quotescript.json
grep "symbols=${SYMBOL}" ${SYMBOL}.sparkscript.txt | sed -e "s@>{@>\n{@g" |  sed -e "s@}</script>@}\n</script>@g" | grep -Ev '<script|script>' >${SYMBOL}.sparkscript.json

popd
./process_json.py -s ${SYMBOL} -f ${SYMBOL}/${SYMBOL}.quotescript.json
./process_json.py -s ${SYMBOL} -f ${SYMBOL}/${SYMBOL}.sparkscript.json
rm -rf ${SYMBOL}
