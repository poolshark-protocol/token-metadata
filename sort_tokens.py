import time
import json
from operator import itemgetter

# TODO: https://raw.githubusercontent.com/poolsharks-protocol/token-metadata/master/blockchains/ethereum/assets/0xfF20817765cB7f73d4bde2e66e067E58D11095C2/logo.png
# make background transparent for all images

supported_chains = ['ethereum']
sort_by_volume = []
for chain in supported_chains:
    f = open('blockchains/' + chain + '/tokenlist.json','r')
    print(time.time())
    tokenlist = json.load(f)
   
    search_tokens = tokenlist['search_tokens']
    print(len(search_tokens))
    for token in search_tokens:
        #print(token)
        if 'market_cap_rank' in token.keys() and token['market_cap_rank'] == None:
            sort_by_volume.append(token)
            search_tokens.remove(token)
           # print('removed token')
        elif 'market_cap_rank' not in token.keys():
            print('coin found w/o market cap rank: ' + json.dumps(token))
            search_tokens.remove(token)
        
    for token in search_tokens:
        if 'name' not in token.keys() or token['name'] == '':
            print(json.dumps(token))
    print(len(search_tokens))
    sorted(search_tokens,key=itemgetter('market_cap_rank'))