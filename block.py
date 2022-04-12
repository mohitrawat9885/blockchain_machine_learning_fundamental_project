
from importlib.metadata import files
import json
import os
import hashlib
import re
import string
from unittest import result

from numpy import block

BLOCKCHAIN_DIR = 'blockchain/'


def get_hash(prev_block):
    with open(BLOCKCHAIN_DIR + prev_block, 'rb') as f:
        content = f.read()
    return hashlib.md5(content).hexdigest()


def check_integrity():
    files =  sorted(os.listdir(BLOCKCHAIN_DIR), key=lambda x: int(x))

    results = []

    for file in files[1:]:
        with open(BLOCKCHAIN_DIR + file) as f:
            block = json.load(f)

        prev_hash = block.get('prev_block').get('hash')
        prev_filename = block.get('prev_block').get('filename')

        actual_hash = get_hash(prev_filename)

        if prev_hash == actual_hash:
            res = 'Ok'
        else:
            res = 'was Changed'
        res = res+"  ___**🔗**__"+ "__"+file+"__"+block['shape']
        # print(f'Block {prev_filename}: {res}')
        results.append({'block': prev_filename, 'result': res})

    return results


def write_block(shape, text):
    blocks_count = len(os.listdir(BLOCKCHAIN_DIR))
    prev_block = str(blocks_count)
    if blocks_count == 0:
        prev_hash = ""
        prev_block = ""
    else:
        prev_hash = get_hash(prev_block)
    
    data = {
        "shape" : shape,
        "text": text,
        "prev_block" : {
        "hash" : prev_hash,
        "filename" : prev_block
        }
    }

    current_block = BLOCKCHAIN_DIR + str(blocks_count + 1) 

    with open(current_block, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')



def main():
    check_integrity()

if __name__ == '__main__':
    main()