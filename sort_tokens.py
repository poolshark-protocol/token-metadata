import time
import json

# TODO: https://raw.githubusercontent.com/poolsharks-protocol/token-metadata/master/blockchains/ethereum/assets/0xfF20817765cB7f73d4bde2e66e067E58D11095C2/logo.png
# make background transparent for all images

supported_chains = ['ethereum']

for chain in supported_chains:
    f = open('blockchains/' + chain + '/tokenlist.json','r')
    print(time.time())
    tokenlist = json.load(f)

    for token in tokenlist['search_tokens']:
        print(token)