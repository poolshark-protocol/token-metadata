from pathlib import Path
import os

import shutil


active = 0
abandoned = 0
spam = 0
rmdirs = 0

def remove_empty_dirs(path):
  for root, dirnames, filenames in os.walk('blockchains/ethereum/assets', topdown=False):
      for dirname in dirnames:
          Path(path + dirname).rmdir()

for path in Path('blockchains/ethereum/assets/').rglob('info.json'): 
  with open(path, 'r') as info:
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

print("active tokens found: " + str(active))
print("abandoned tokens found: " + str(abandoned))
print("spam tokens found: " + str(spam))
print("token directories removed: " + str(rmdirs))


    