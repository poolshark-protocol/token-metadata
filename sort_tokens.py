import time
import json
from operator import itemgetter
from datetime import datetime

# TODO: https://raw.githubusercontent.com/poolsharks-protocol/token-metadata/master/blockchains/ethereum/assets/0xfF20817765cB7f73d4bde2e66e067E58D11095C2/logo.png
# make background transparent for all images

supported_chains = ['ethereum']
sort_values = []
for chain in supported_chains:
    f = open('blockchains/' + chain + '/tokenlist.json','r')
    print(time.time())
    tokenlist = json.load(f)

    search_tokens = tokenlist['search_tokens']
    print(len(search_tokens))
    for token in search_tokens:
        #print(token)
        if 'market_cap_rank' in token.keys() and token['market_cap_rank'] == None and '24_hr_volume_usd' in token.keys():
            sort_values.append(token['24_hr_volume_usd'])
        elif 'market_cap_rank' in token.keys() and token['market_cap_rank'] != None:
            sort_values.append(token['market_cap_usd'])
        
        
    for token in search_tokens:
        if 'name' not in token.keys() or token['name'] == '':
            print('found bad token..')
            print(json.dumps(token))

    print([search_tokens for _,search_tokens in sorted(zip(sort_values,search_tokens))])
    # tokenlist['search_tokens'] = sort_by_mkt_cap + sort_by_volume
    # tokenlist['timestamp'] = str(datetime.now())
    # f = open('blockchains/' + chain + '/tokenlist.json','w')
    # f.write(json.dumps(tokenlist, indent=4))

