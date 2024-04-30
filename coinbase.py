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


# Initial header is from a sample coinbase transaction
serial = "010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff2503233708184d696e656420627920416e74506f6f6c373946205b8160a4256c0000946e0100ffffffff02f595814a000000001976a914edf10a7fac6b32e24daa5305c723f3de58db1bc888ac0000000000000000"

coinbase_wtxid = ["0000000000000000000000000000000000000000000000000000000000000000"]
with open("wtxid.txt", "r") as file:
    wtxid = [line.strip() for line in file]
wtxid_list = coinbase_wtxid+wtxid

merkle_root_hash = merkleroot(wtxid_list)
witness_reserved_value = "0000000000000000000000000000000000000000000000000000000000000000"

wtxid_commitment = hash256(merkle_root_hash+witness_reserved_value)
serial += "266a24aa21a9ed"

serial += wtxid_commitment
serial += "0120000000000000000000000000000000000000000000000000000000000000000000000000"

with open("coinbase_data.txt", "w") as file:
    file.write(str(serial) + "\n")