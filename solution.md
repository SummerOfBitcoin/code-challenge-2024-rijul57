# Summer of Bitcoin 2024

> [!IMPORTANT]
> My codes script do not work on grader, I have talked with Anmol regarding this. So I am commiting my output.txt. You can run the code locally, it takes around 12 mins on my system

## Synopsis

This github repo contains my solution for the SOB assignment. This assignment was about mining a custom block. This task included :
1) Verifying transactions
2) Making a block header from the valid transactions

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

It contains the get_transaction_info function that serializes every transaction to calculate its message. 

### merkle_root.py

This was necessary for calculating merkle root for header.
I defined two function in here, mainly calculate_txid_array which returns me an array consisting of all the txids in natural byte ordering, and another function calc_merkle_root which calculates merkle root. Merkle root is nothing but taking hash of 2 consecutive txids, repetitively until only one hash remains. I used a temp array to store the hash in each iteration, and at the end, I used to replace my original txid array with temp array, and make temp array empty again.

Similar to this I also have defined witness_commitment.py which has very similar implementation. Only difference being that calc_merkle_root needs txid for coinbase as a parameter, calc_witness_commitment takes wtxid of coinbase as 0. Also, the here instead of txid array, we use wtxid array (We have already defined a function in our serialise.py to calculate wtxid).

Because of a very similar implementation, I choose not to devote a seperate section for witness_commitment.py in this doc.

### header.py

This file is very similar. It contains two functions:
make_header() which adds all the things such as time, merkle root, etc to the header. The second function make_hash() is responsible for finding a nonce such that hash of header is less than difficulty target.

### main.py

This is the final file which runs all the functions and makes the output.txt. My workflow is: I run verify_transactions() and write all the verified p2pkh and p2wpkh transactions in valid_transactions.txt (In order to keep my block under weight limit, I have broken the loop at a point when enough transations were included already). Then make_block() is called which calls make_coinbase() to make the coinbase, and then calls make_hash() to make a header with valid nonce, and then finally calls calculate_txid() to included txids of the valid_transactions in the block.

With this, my block is mined, and I got a score of 93. With my endsemester exams going on, and proposal left, I did not try to optimise the score/time of the code. But I had few optimisations in mind. Most basic one was to sort all the verified transactions based on their fee and then start taking the transactions with most fees. I could have also optimised run time at places by changing the implementation or maybe some data structures, but due to lack of time I couldn't.

## Tirth Bhayani

## IIT-BHU