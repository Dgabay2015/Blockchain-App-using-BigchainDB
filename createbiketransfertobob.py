from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit
from keygen import Key
aliceo = Key()
alice = aliceo.getkey()
print(alice.private_key)

bob = generate_keypair()

bdb_root_url = 'https://test.ipdb.io/'  # Use YOUR BigchainDB Root URL here

tokens = {}
tokens['app_id'] = '52087ff5'
tokens['app_key'] = '315c78371efd2b70ddfc7c6ca6024fd7'
bdb = BigchainDB('https://test.ipdb.io/', headers=tokens)

bicycle_asset = {
    'data': {
        'bicycle': {
            'serial_number': 'abcd1234',
            'manufacturer': 'bkfab'
        },
    },
}

bicycle_asset_metadata = {
    'planet': 'earth'
}

prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=bicycle_asset,
    metadata=bicycle_asset_metadata
)

fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx,
    private_keys=alice.private_key
)

sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)

txid = fulfilled_creation_tx['id']

trials = 0

while trials < 10223320:
    trials += 1


asset_id = txid

transfer_asset = {
    'id': asset_id
}

output_index = 0
output = fulfilled_creation_tx['outputs'][output_index]

transfer_input = {
    'fulfillment': output['condition']['details'],
    'fulfills': {
        'output_index': output_index,
        'transaction_id': fulfilled_creation_tx['id']
    },
    'owners_before': output['public_keys']
}

prepared_transfer_tx = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=transfer_asset,
    inputs=transfer_input,
    recipients=bob.public_key,
)

fulfilled_transfer_tx = bdb.transactions.fulfill(
    prepared_transfer_tx,
    private_keys=alice.private_key,
)

sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_tx)

print("Is Bob the owner?",
    sent_transfer_tx['outputs'][0]['public_keys'][0] == bob.public_key)

print("Was Alice the previous owner?",
    fulfilled_transfer_tx['inputs'][0]['owners_before'][0] == alice.public_key)