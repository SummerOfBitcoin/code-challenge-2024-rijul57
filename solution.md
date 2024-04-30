# Summer of Bitcoin 2024

## Synopsis

This github repo contains my solution for the SOB assignment. This assignment was about mining a custom block. This task included :

1. Verifying transactions
2. Making a block header from the valid transactions

Here is a detail of all the functions and files I have created to solve the assignment.

## Usage

python main.py

### transactions.py

It contains the function get_p2pkh_and_p2wpkh(). This function loops through all the tranactions in the mempool and filters out the transactions that contain p2pkh and p2wpkh transactions as input. The implementation involves verifying the p2pkh and p2wpkh transactions.

### verify.py

I have used no existing elliptic libraries to verify the signatures. The add, double, multiply functions arer used to perform operation on points on elliptic curves. The decodepk function that calculates the y component of the public key, while the decodesig function parses the r and s components from the signature. The verify function then checks
whether `(s⁻¹ * z)G + (s⁻¹ * r)Q `is equal to R or not.
Here, R and S are components of DER signature, Q is the public key, z is the message hash and G is the generator point.

### get_data.py

It contains the get_transaction_info function that serializes every transaction to calculate its message. It contains two functions get_p2pkh_info and get_p2wpkh_info depending on the nature of transaction (legacy/segwit). These functions implement the basic serialization step, components of which are used to compute txids as well as wtxids.
They are also used to parse the signatures and public key values from the json transactioin object.

### coinbase.py

This file contains the generate_coinbase_tx function which basically builds the whole coinbase transaction. Since we do not own a pubkey, i used a sample coinbase transaction to get the fields unrelated to the assignment. The main thing here was to calculate the witness commitment. That required witness transaction ids of all the valid transactions, the code for which is written in wtxid.py. It also includes the function merkleroot which is used for calculating the merkleroot of a list of transactions.

### wtxid.py

This file is used to calculate the witness txid of all the transactions to be used in calculating the witness commitment hash. The witness Id of legacy transactions is same as that of their txid. For legacy transactions, we additionally add the witness stack at the end of the serialised transaction.

### block.py

This file is finally used to calculate the block header info usign its merkle root. It contains the get_merkle_root function that calculates the merkle root to be added in the block header. It then loops through various nonce values
until it finaaly reaches a value that is less than our target.

### txid.py

This file serialises all transactions and calulates their txids.

### main.py

This is the main file that runs all the code for the solution. The workflow is following:

1. Get a list of all p2pkh and p2wpkh transactions.
2. Verify these transactions and add all the valid trasnactions to a valid_tx.txt file.
3. Generate the coinbase transaction.
4. Make the block header
5. Finally append all the info into the output.txt file.

## Thoughts

My solution gives a score of 92. I have broken the loop at the point of 2650 to not exceed the maximum block weight. It takes approximately 2:30 minutes to run which is well under the maximum 10 min time limit. There are further optimisations to efficiency that can be made. The goal of the miner for any block is to maximise the transaction fee withing the given block weight limit. One approach to tackle this could be sorting all the transactions by fee and taking first x transactions such that block weight < maximum block weight. The academic pressure for assignments and th eongoing endsems as well as the time contraints for writing a good proposal prevented me from doing so.

## Rijul Singla

## IIT-BHU
