from pycoingecko import CoinGeckoAPI
from web3 import Web3
import json
import requests
import os
import time
from PIL import Image
from io import BytesIO
from pathlib import Path

cg = CoinGeckoAPI()
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/UtS222NKanBSIOdJz3yMWWQjFeC3OtyV'))
print(w3.isConnected())
erc20_file = open('abis/ERC20.json')
erc20_abi = json.load(erc20_file)
supported_chains = ['ethereum']
search_tokens_blacklist = ['RealT Token', 'RealToken']

coins = cg.get_coins_list(include_platform=True)
i = 0
tokens = {}
print(time.time())

for chain in supported_chains:
    tokens[chain] = []
    for coin in coins:
        if chain in coin['platforms'].keys() and coin['platforms'][chain] != '':
            skip_token = False
            for term in search_tokens_blacklist:
                if coin['name'].startswith(term):
                    skip_token = True
                    #print('skipped token')
                if os.path.exists('blockchains/' + chain + '/assets/' + Web3.toChecksumAddress(coin['platforms']['ethereum'])):
                    skip_token = True
                    #print('token already exists')

            if skip_token == False:
                contract = w3.eth.contract(Web3.toChecksumAddress(coin['platforms']['ethereum']), abi=erc20_abi)
                path = 'blockchains/' + chain + '/assets/' + contract.address
                if not os.path.exists(path):
                    os.makedirs(path)
                if not os.path.exists(path + '/info.json'):
                    token = {}
                    #try:
                    print(coin)
                    too_many_requests = True
                    while too_many_requests:
                        try:
                            time.sleep(1.3)
                            coin_info = cg.get_coin_info_from_contract_address_by_id(chain, coin['platforms'][chain])
                            too_many_requests = False
                        except:
                            print('429 - Too Many Requests: waiting 5 seconds')
                            time.sleep(5)
                    try:        
                        token['name'] = contract.functions.name().call()
                        token['symbol'] = contract.functions.symbol().call()
                        token['id'] = contract.address
                        token['decimals'] = contract.functions.decimals().call()
                    except:
                        print('contract function failed for ' + json.dumps(coin) + '\ncontinuing..')
                        continue

                    token['coingecko_url'] = 'https://www.coingecko.com/en/coins/' + coin['id']
                    token['market_cap_rank'] = coin_info['market_cap_rank']
                    
                    if coin_info['market_data']['total_volume'] != None and coin_info['market_data']['total_volume'] != '{}' and 'usd' in coin_info['market_data']['total_volume'].keys():
                        #print(coin_info['market_data']['total_volume'])
                        token['24_hr_volume_usd'] =coin_info['market_data']['total_volume']['usd']

                    if coin_info['public_notice'] != None:
                        token['public_notice'] = coin_info['public_notice']
                    try: 
                        img_data = requests.get(coin_info['image']['large']).content
                    except:
                        print('bad image URL...continuing')
                        continue
                    img = Image.open(BytesIO(img_data))
                    img.save(path + '/logo.png')

                    token['logoURI'] = 'https://raw.githubusercontent.com/poolsharks-protocol/token-metadata/master/' + path + '/logo.png'
                    
                    with open(path + '/info.json','w+') as token_info:
                        token_info.write(json.dumps(token, indent=4))
                    # except:
                    #   print('error calling contract for ' + json.dumps(coin))
                    
                    
                else:
                    print('token already exists')
                    with open(path + '/info.json','r+') as token_info:
                        token = json.load(token_info)
                        print('found file: ' + json.dumps(coin))
                    
                tokens[chain].append(token)
            #else:
                #print('skipped token')

    f = open('blockchains/' + chain + '/tokenlist.json','r')
    print(time.time())
    tokenlist = json.load(f)
    tokenlist['search_tokens'] = tokenlist['search_tokens'] + tokens[chain]
    fw = open('blockchains' + '/ethereum' + '/tokenlist.json','w')
    fw.write(json.dumps(tokenlist, indent=4))
