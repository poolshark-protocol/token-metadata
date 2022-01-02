import time
import json
from operator import itemgetter
from datetime import datetime

# TODO: https://raw.githubusercontent.com/poolsharks-protocol/token-metadata/master/blockchains/ethereum/assets/0xfF20817765cB7f73d4bde2e66e067E58D11095C2/logo.png
# make background transparent for all images

supported_chains = ['ethereum']
sorted_tokens = []
for chain in supported_chains:
    f = open('blockchains/' + chain + '/tokenlist.json','r')
    print(time.time())
    tokenlist = json.load(f)

    search_tokens = tokenlist['search_tokens']
    print(len(search_tokens))
    for token in search_tokens:
        #print(token)
        if 'market_cap_rank' in token.keys() and token['market_cap_rank'] == None and '24_hr_volume_usd' in token.keys():
            token['sort_value'] = token['24_hr_volume_usd']
            sorted_tokens.append(token)
        elif 'market_cap_rank' in token.keys() and token['market_cap_rank'] != None and token['market_cap_usd'] > 0:
            token['sort_value'] = token['market_cap_usd']
            sorted_tokens.append(token)
        
    for token in search_tokens:
        if 'name' not in token.keys() or token['name'] == '':
            print('found bad token..')
            print(json.dumps(token))
    sorted_tokens = sorted(sorted_tokens, key=lambda d: d['sort_value'], reverse=True)
    for token in sorted_tokens:
        del token['sort_value']
        del token['sort_key']
    tokenlist['search_tokens'] = sorted_tokens
    tokenlist['timestamp'] = str(datetime.now())
    f = open('blockchains/' + chain + '/tokenlist.json','w')
    f.write(json.dumps(tokenlist, indent=4))

