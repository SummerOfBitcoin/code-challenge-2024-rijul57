block(coinbase_serialization)

    # with open("output.txt", "w") as file:
    #     file.write(str(block_header) + "\n")
    #     file.write(str(coinbase_serialization) + "\n")
    #     coinbase_serialization_little = bytes.fromhex(hash256(coinbase_serialization))[::-1].hex()
    #     file.write(str(coinbase_serialization_little) + "\n")
    #     for filename in valid_tx:
    #         txid = get_txid(filename)
    #         txid_little = bytes.fromhex(hash256(txid))[::-1].hex()
    #         file.write(str(txid_