import json
import hashlib
import time
start_time = time.time()

def encode_varint(value):
    if value < 0xFD:
        return bytes([value])
    elif value <= 0xFFFF:
        return b'\xFD' + value.to_bytes(2, byteorder='little')
    elif value <= 0xFFFF_FFFF:
        return b'\xFE' + value.to_bytes(4, byteorder='little')
    else:
        return b'\xFF' + value.to_bytes(8, byteorder='little')
    
def bytes_to_compact_hex(bytes_data):
    return ''.join(format(byte, '02x') for byte in bytes_data)

def hash256(msg):
    hashp = hashlib.sha256(hashlib.sha256(bytes.fromhex(msg)).digest()).digest()
    return hashp.hex()

def get_p2pkh_info(obj, j):
    serial = ""
    if(str(obj['version']) == '1'):
        serial += "01000000"
    else:   
        serial += "02000000"
    serial += bytes_to_compact_hex(encode_varint(len(obj['vin'])))
    for i in range(len(obj['vin'])):
        tx = obj['vin'][i]
        if(j == i):                
            txid_little_endian = bytes.fromhex(tx['txid'])[::-1].hex()
            serial += txid_little_endian
            serial += tx['vout'].to_bytes(4, byteorder = 'little').hex()
            serial += bytes_to_compact_hex(encode_varint(len(tx['prevout']['scriptpubkey'])//2))
            serial += tx['prevout']['scriptpubkey']
            serial += tx['sequence'].to_bytes(4, byteorder = 'little').hex()
        else:
            txid_little_endian = bytes.fromhex(tx['txid'])[::-1].hex()
            serial += txid_little_endian
            serial += tx['vout'].to_bytes(4, byteorder = 'little').hex()
            serial += "00"
            serial += ""
            serial += tx['sequence'].to_bytes(4, byteorder = 'little').hex()

    list = obj['vin'][j]['scriptsig_asm'].split()
    sig = list[1]
    pk = list[3]
            
    serial += bytes_to_compact_hex(encode_varint(len(obj['vout'])))

    for i in range(len(obj['vout'])):
        tx = obj["vout"][i]
        serial += tx['value'].to_bytes(8, byteorder = 'little').hex()
        serial += bytes_to_compact_hex(encode_varint(len(tx['scriptpubkey'])//2))
        serial += tx['scriptpubkey']
            
    serial += obj['locktime'].to_bytes(4, byteorder = 'little').hex()
    serial += "01000000"
    hash = hash256(serial)
    return [hash, sig, pk]

def get_p2wpkh_info(obj, j):
    temp1 = ""
    for i in range(len(obj['vin'])):
        tx = obj['vin'][i]
        txid_little_endian = bytes.fromhex(tx['txid'])[::-1].hex()
        temp1 += txid_little_endian
        temp1 += tx['vout'].to_bytes(4, byteorder = 'little').hex()

    temp2 = ""
    for i in range(len(obj['vin'])):
        tx = obj['vin'][i]
        temp2 += tx['sequence'].to_bytes(4, byteorder = 'little').hex()

    temp3 = ""
    for i in range(len(obj['vout'])):
        tx = obj["vout"][i]
        temp3 += tx['value'].to_bytes(8, byteorder = 'little').hex()
        temp3 += bytes_to_compact_hex(encode_varint(len(tx['scriptpubkey'])//2))
        temp3 += tx['scriptpubkey']
    serial = ""
    if(str(obj['version']) == '1'):
        serial += "01000000"
    else:   
        serial += "02000000"
    serial += hash256(temp1)
    serial += hash256(temp2)
    tx = obj['vin'][j]
    txid_little_endian = bytes.fromhex(tx['txid'])[::-1].hex()
    serial += txid_little_endian
    serial += tx['vout'].to_bytes(4, byteorder = 'little').hex()
    serial += "1976a914"
    serial += tx['prevout']['scriptpubkey'][4:]
    serial += "88ac"
    serial += tx['prevout']['value'].to_bytes(8, byteorder = 'little').hex()
    serial += tx['sequence'].to_bytes(4, byteorder = 'little').hex()
    serial += hash256(temp3)
    serial += obj['locktime'].to_bytes(4, byteorder = 'little').hex()
    serial += "01000000"
    hash = hash256(serial)
    sig = obj['vin'][j]['witness'][0]
    pk = obj['vin'][j]['witness'][1]
    return [hash, sig, pk]


def get_transaction_info(filename):
    file = open(f'mempool/{filename}', 'r')                                                                                                    
    data = file.read()
    obj = json.loads(data)
    tx_data = []
    for j in range(len(obj['vin'])):
        if(obj['vin'][j]['prevout']['scriptpubkey_type'] == 'p2pkh'):
            info = get_p2pkh_info(obj, j)
        else:
            info = get_p2wpkh_info(obj, j)
    tx_data.append(info)
    return tx_data