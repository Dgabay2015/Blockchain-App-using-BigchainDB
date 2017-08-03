from bigchaindb_driver import BigchainDB
from keygen import alice, bob

tokens = {}
tokens['app_id'] = '52087ff5'
tokens['app_key'] = '315c78371efd2b70ddfc7c6ca6024fd7'
bdb = BigchainDB('https://test.ipdb.io/', headers=tokens)


# here I create for testing purposes to keypair objects
# one named bob and another alice each containing a priv and pub key


class Asset:
    def __init__(self, description):
        name = {
            'data': {
                description: {
                    'serial_number': 'abcd1234',
                    'manufacturer': 'bkfab',
                },
            },
        }

        prepared_creation_tx = bdb.transactions.prepare(
            operation='CREATE',
            signers=alice.public_key,
            asset=name,
        )
        self.fulfilled_creation_tx = bdb.transactions.fulfill(
            prepared_creation_tx,
            private_keys=alice.private_key
        )
        sent_creation_tx = bdb.transactions.send(self.fulfilled_creation_tx)
        self.txid = self.fulfilled_creation_tx['id']

        trials = 0

        while trials < 102233210:
            trials += 1

        print(bdb.transactions.status(self.txid))


    def get_asset_details(self):
        return(self.fulfilled_creation_tx)

    def gettxid(self):
        return(self.txid)

    def transferasset(self):
        asset_id = self.txid
        transfer_asset = {
            'id': asset_id
        }
        output_index = 0
        output = self.fulfilled_creation_tx['outputs'][output_index]
        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': self.fulfilled_creation_tx['id']
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

    def view_asset(self):
        creation_tx = bdb.transactions.retrieve(self.txid)
        return creation_tx

