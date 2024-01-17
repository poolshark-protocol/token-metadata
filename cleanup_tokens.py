from pathlib import Path
import os
import json
from datetime import datetime
total = 0
active = 0
abandoned = 0
spam = 0
rmdirs = 0

blockchain = "scroll"


supported_chains = ['scroll']
ids_to_wipe = []
new_search_tokens = []
# TODO: use to cleanup tokens we don't want
# for chain in supported_chains:
#     f = open('blockchains/' + chain + '/tokenlist.json','r')
#     tokenlist = json.load(f)
#     search_tokens = tokenlist['search_tokens']
#     print(len(search_tokens))
#     for token in search_tokens:
#         #print(token)
#         if '24_hr_volume_usd' in token.keys() and token['24_hr_volume_usd'] > 0:
#             new_search_tokens.append(token)

#     tokenlist['search_tokens'] = new_search_tokens
#     tokenlist['timestamp'] = str(datetime.now())
#     f = open('blockchains/' + chain + '/tokenlist.json','w')
#     f.write(json.dumps(tokenlist, indent=4))

for path in Path('blockchains/' + blockchain + '/assets/').rglob('info.json'): 
  with open(path, 'r') as info:
   total += 1
   if '"status": "active"' in info.read():
     active += 1
   elif '"status": "abandoned"' in info.read():
     abandoned += 1
   elif '"status": "spam"' in info.read():
     spam += 1

for path in os.listdir('blockchains/' + blockchain + '/assets/'):
  if "logo.png" not in os.listdir('blockchains/' + blockchain + '/assets/' + path):
    os.remove('blockchains/' + blockchain + '/assets/' + path + '/info.json')
    os.rmdir('blockchains/' + blockchain + '/assets/' + path)
    rmdirs+=1
  elif os.listdir('blockchains/' + blockchain + '/assets/' + path) == []:
    os.rmdir('blockchains/' + blockchain + '/assets/' + path + '/info.json')
    rmdirs+=1
print('--------------------------')
print(blockchain.upper() + ":     " + str(total))
print('--------------------------')
print("active:       " + str(active))
print("abandoned:    " + str(abandoned))
print("spam:         " + str(spam))
print("dirs removed: " + str(rmdirs))


    