import hashlib
from wtxid import get_wtxid

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

COINBASE_WTXID = "0000000000000000000000000000000000000000000000000000000000000000"
WITNESS_RESERVED_VALUE = "0000000000000000000000000000000000000000000000000000000000000000"

def get_wtxid_list(COINBASE_WTXID):
    wtxid_list = [COINBASE_WTXID]
    witness_txid = get_wtxid()
    wtxid_list.extend(witness_txid)
    return wtxid_list

# Initial part of serialization is from a sample coinbase transaction
def generate_coinbase_tx():
    serial = "010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff2503233708184d696e656420627920416e74506f6f6c373946205b8160a4256c0000946e0100ffffffff02f595814a000000001976a914edf10a7fac6b32e24daa5305c723f3de58db1bc888ac0000000000000000266a24aa21a9ed"
    wtxid_list = get_wtxid_list(COINBASE_WTXID)
    witness_root_hash = merkleroot(wtxid_list)
    witness_commitment = hash256(witness_root_hash + WITNESS_RESERVED_VALUE)

    serial += witness_commitment
    serial += "0120000000000000000000000000000000000000000000000000000000000000000000000000"
    return serial

