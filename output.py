import hashlib

def hash256(msg):
    hashp = hashlib.sha256(hashlib.sha256(bytes.fromhex(msg)).digest()).digest()
    return hashp.hex()

with open("block_data.txt", "r") as file:
    block_data_list= [line.strip() for line in file]

block_data = block_data_list[0]

with open("coinbase_data.txt", "r") as file:
    data = [line.strip() for line in file]

coinbase_txid = data[0]

with open("txid.txt", "r") as file:
    tx_list = [line.strip() for line in file]


with open("output.txt", "w") as file:
    file.write(str(block_data) + "\n")
    file.write(str(coinbase_txid) + "\n")
    coinbase_txid_little_endian = bytes.fromhex(coinbase_txid)[::-1].hex()
    file.write(hash256(coinbase_txid_little_endian) + "\n")
    for txid in tx_list:
        txid_little_endian = bytes.fromhex(txid)[::-1].hex()
        file.write(str(txid_little_endian) + "\n")
