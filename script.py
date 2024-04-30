import os
import json

p2pkh = []
ct = 0

folder_path = "mempool"
for filename in os.listdir(folder_path):
    file = open(f'mempool/{filename}', 'r')                                                                                                    
    data = file.read()
    obj = json.loads(data)
    
    check = True
    for i in range(len(obj['vin'])):
        if (obj['vin'][i]['prevout']['scriptpubkey_type'] != 'v0_p2wpkh'):
            check = False
            break

    if(check):
        ct += 1
        p2pkh.append(filename)

    check = True
    for i in range(len(obj['vin'])):
        if (obj['vin'][i]['prevout']['scriptpubkey_type'] != 'p2pkh'):
            check = False
            break

    if(check):
        ct += 1
        p2pkh.append(filename)
 
print(ct)
with open("transactions.txt", "w") as file:
    for item in p2pkh:
        file.write(str(item) + "\n")



