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
w3 = Web3(Web3.HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/Q0kaVFDZYtPDdMzGcGCQ6lrFNqJrLCVi'))
print(w3.isConnected())
erc20_file = open('abis/ERC20.json')
erc20_abi = json.load(erc20_file)
supported_chains = ['polygon-pos']
new_tokens_only = False
search_tokens_blacklist = ['RealT Token', 
                           'RealToken', 
                           'All.me', 
                           'AltEstate Token',
                           'CloutContracts',
                           'Cointorox',
                           'Cryptocurrency Top 10 Index',
                           'Curio Governance',
                           'DigixDAO',
                           'Energoncoin',
                           'Ethereum Gold',
                           'EXMR FDN',
                           'Freeliquid',
                           'Future Of Finance Fund',
                           'Giga Watt Token',
                           'HedgeTrade',
                           'High Performance Blockchain',
                           'LNX Protocol',
                           'Paypex',
                           'Prime DAI',
                           'Qobit'
                           'Rapidz',
                           'Sai',
                           'SENSO',
                           'Silent Notary',
                           'Spaghetti',
                           'SpideyFloki',
                           'Taxa Token',
                           'TOP Network',
                           'Union Fair Coin',
                           'WM PROFESSIONAL',
                           'Wrapped IoTex',
                           'Wrapped XMR by BTSE'
                          ]

coins = cg.get_coins_list(include_platform=True)
i = 0
tokens = {}
print(time.time())

for chain in supported_chains:
    tokens[chain] = []
    for coin in coins:
        if chain in coin['platforms'].keys() and coin['platforms'][chain] != '':
            skip_token = False
            new_token = False
            for term in search_tokens_blacklist:
                if coin['name'].startswith(term):
                    skip_token = True
                    #print('skipped token')

            if skip_token == False:
                contract = w3.eth.contract(Web3.toChecksumAddress(coin['platforms'][chain]), abi=erc20_abi)
                path = 'blockchains/' + chain + '/assets/' + contract.address
                token = {}
                if not os.path.exists(path):
                    os.makedirs(path)
                    new_token = True

                #############################
                ###### CONTRACT CALLS #######
                #############################

                if not os.path.exists(path + '/info.json'):
                
                    try:  
                        token['name'] = contract.functions.name().call()
                    except:
                        print('name() failed for' + json.dumps(coin) + '..using coingecko name value..')
                        token['name'] = coin['name']
                    if name == '':
                        print('name() failed for' + json.dumps(coin) + '..using coingecko name value..')
                        token['name'] = coin['name']

                    try:    
                        token['symbol'] = contract.functions.symbol().call()
                    except:
                        print('symbol() failed for' + json.dumps(coin) + '..using coingecko symbol value..')
                        token['symbol'] = coin['symbol'].upper()
                        
                    token['id'] = contract.address

                    try:
                        token['decimals'] = contract.functions.decimals().call()
                    except:
                        print('decimals() failed for' + json.dumps(coin) + '..continuing on..')
                        continue

                ##########################################
                ###### HANDLE TOKEN ALREADY EXISTS #######
                ##########################################

                else:
                    print('token info.json already exists')
                    with open(path + '/info.json','r+') as token_info:
                        token = json.load(token_info)
                        print('found file: ' + json.dumps(coin))

                if new_tokens_only and not new_token:
                    print(token)
                    tokens[chain].append(token)
                    continue

                #############################
                ###### COINGECKO INFO #######
                #############################
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
                        img_data = requests.get(coin_info['image']['large']).content
                    except:
                        print('bad image URL...continuing')
                        continue
                    img = Image.open(BytesIO(img_data))
                    img.save(path + '/logo.png')

                token['coingecko_url'] = 'https://www.coingecko.com/en/coins/' + coin['id']
                if 'usd' in coin_info['market_data']['market_cap'].keys():
                    token['market_cap_usd'] = coin_info['market_data']['market_cap']['usd']
                else:
                    token['market_cap_usd'] = 0.0
                token['market_cap_rank'] = coin_info['market_data']['market_cap_rank']
                
                if coin_info['market_data']['total_volume'] != None and coin_info['market_data']['total_volume'] != '{}' and 'usd' in coin_info['market_data']['total_volume'].keys():
                    #print(coin_info['market_data']['total_volume'])
                    token['24_hr_volume_usd'] =coin_info['market_data']['total_volume']['usd']

                if coin_info['public_notice'] != None:
                    token['public_notice'] = coin_info['public_notice']

                token['logoURI'] = 'https://raw.githubusercontent.com/poolsharks-protocol/token-metadata/master/' + path + '/logo.png'
                
                with open(path + '/info.json','w+') as token_info:
                    token_info.write(json.dumps(token, indent=4))
                    
                tokens[chain].append(token)
            else:
                print('skipped token')

    if os.path.exists('blockchains/' + chain + '/tokenlist.json'):
        f = open('blockchains/' + chain + '/tokenlist.json','r')
        print(time.time())
        tokenlist = json.load(f)
        tokenlist['search_tokens'] = tokens[chain] + tokenlist['search_tokens']
    else:
        tokenlist = {}
        tokenlist['search_tokens'] = tokens[chain]
    fw = open('blockchains' + '/' + chain + '/tokenlist.json','w+')
    fw.write(json.dumps(tokenlist, indent=4))
