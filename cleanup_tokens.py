from pathlib import Path
import os
import shutil

total = 0
active = 0
abandoned = 0
spam = 0
rmdirs = 0

blockchain = "ethereum"

for path in Path('blockchains/' + blockchain + '/assets/').rglob('info.json'): 
  with open(path, 'r') as info:
   total += 1
   if '"status": "active"' in info.read():
     active += 1
   elif '"status": "abandoned"' in info.read():
     abandoned += 1
   elif '"status": "spam"' in info.read():
     spam += 1

for path in os.listdir('blockchains/ethereum/assets'):
    if os.listdir('blockchains/ethereum/assets/' + path) == []:
      os.rmdir('blockchains/ethereum/assets/' + path)
      rmdirs+=1
print('--------------------------')
print(blockchain.upper() + ":     " + str(total))
print('--------------------------')
print("active:       " + str(active))
print("abandoned:    " + str(abandoned))
print("spam:         " + str(spam))
print("dirs removed: " + str(rmdirs))


    