from transactions import get_p2pkh_and_p2wpkh
from verify import verify, decodepk, decodesig
from get_data import get_transaction_info
from coinbase import generate_coinbase_tx
from block import make_block
from txid import hash256, get_txid

def generate_block():
    p2pkh_p2wpkh = get_p2pkh_and_p2wpkh()
    valid_tx = []

    for filename in p2pkh_p2wpkh[:20]:
        check = True
        tx_data = get_transaction_info(filename)
        for info in tx_data:
            pkt = decodepk(info[2])
            st = decodesig(info[1])
            isValid = verify(pkt, st, int(info[0], 16))
            if(isValid == False):
                check = False
                break
        if(check):
            valid_tx.append(filename)

    with open("valid_tx.txt", "w") as file:
        for item in valid_tx:
            file.write(str(item) + "\n")

    coinbase_serialization = generate_coinbase_tx()
    block_header = make_block(coinbase_serialization)

    with open("output.txt", "w") as file:
        file.write(str(block_header) + "\n")
        file.write(str(coinbase_serialization) + "\n")
        coinbase_serialization_little = bytes.fromhex(hash256(coinbase_serialization))[::-1].hex()
        file.write(str(coinbase_serialization_little) + "\n")
        for filename in valid_tx:
            txid = get_txid(filename)
            txid_little = bytes.fromhex(hash256(txid))[::-1].hex()
            file.write(str(txid_little) + "\n")


generate_block()


