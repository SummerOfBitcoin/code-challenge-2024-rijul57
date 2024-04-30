import os
import json

FOLDER_PATH = "mempool"

def get_p2pkh_and_p2wpkh():
    p2pkh_p2wpkh = []
    for filename in os.listdir(FOLDER_PATH):

        """Load the json files from mempool"""
        file = open(f'{FOLDER_PATH}/{filename}', 'r')                                                                                                    
        data = file.read()
        obj = json.loads(data)
        

        """Add p2wpkh transactions to list"""
        check = True
        for i in range(len(obj['vin'])):
            if (obj['vin'][i]['prevout']['scriptpubkey_type'] != 'v0_p2wpkh'):
                check = False
                break

        if(check):
            p2pkh_p2wpkh.append(filename)


        """Add p2wpkh transactions to list"""
        check = True
        for i in range(len(obj['vin'])):
            if (obj['vin'][i]['prevout']['scriptpubkey_type'] != 'p2pkh'):
                check = False
                break

        if(check):
            p2pkh_p2wpkh.append(filename)

    return p2pkh_p2wpkh



