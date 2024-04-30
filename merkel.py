import hashlib

def hash256(msg):
    hashp = hashlib.sha256(hashlib.sha256(bytes.fromhex(msg)).digest()).digest()
    return hashp.hex()

def merkleroot(txid_list):
    n = len(txid_list)
    if(n == 1):
        return txid_list[0]

    result = []
    for i in range(0, n, 2):
        if(i == n - 1):
            concat = txid_list[i]+txid_list[i]
        else:
            concat = txid_list[i]+txid_list[i+1]
        result.append(hash256(concat))
    return merkleroot(result)

with open("txid.txt", "r") as file:
    txid_list = [line.strip() for line in file]

print(merkleroot(txid_list))

for txid in txid_list:
    txid_little_endian = bytes.fromhex(txid)[::-1].hex()
    print(txid_little_endian)

