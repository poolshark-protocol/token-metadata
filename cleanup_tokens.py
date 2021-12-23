from pathlib import Path
import os

import shutil


i = 0

def remove_empty_dirs(path):
  for root, dirnames, filenames in os.walk('blockchains/ethereum/assets', topdown=False):
      for dirname in dirnames:
          Path(path + dirname).rmdir()

for path in Path('blockchains/ethereum/assets/').rglob('info.json'): 
  with open(path, 'r') as info:
   if "abandoned" in info.read():
     i+=1
     print(i)
     print(path.parent)
     # for file in path.parent.iterdir():
     #  file.unlink()
     shutil.rmtree(path.parent)
     # print(str(path.parent) + " removed.")
     # path.parent.rmdir()

for path in os.listdir('blockchains/ethereum/assets'):
    print(i)
    i+=1

    if os.listdir('blockchains/ethereum/assets/' + path) == []:
      os.rmdir('blockchains/ethereum/assets/' + path)
    # if os.path.isfile(os.path.join(dir, path)):
    #     initial_count += 1


    