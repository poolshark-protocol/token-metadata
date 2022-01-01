import time
import json

supported_chains = ['ethereum']

for chain in supported_chains:
    f = open('blockchains/' + chain + '/tokenlist.json','r')
    print(time.time())
    tokenlist = json.load(f)

    for token in tokenlist['search_tokens']:
        print(token)