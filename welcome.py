# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify
from keygen import alice, bob
from asset import Asset

# here I create for testing purposes to keypair objects
# one named bob and another alice each containing a priv and pub key


asset = Asset("bicycle")

app = Flask(__name__)

@app.route('/')
def Welcome():

    return app.send_static_file('index.html')

@app.route('/createuser')
def createuser():


    return '<h1>Thanks for creating an account!</h1>\n' \
           ' <h2>These are your keys you will use for signing and verifying transactions</h2>\n' \
           '<strong>public key :</strong> ' + alice.public_key + '\n\n' \
           '<strong>private key : </strong>' + alice.private_key + '\n' \
            '\n<button type="button" class="btn btn-hot text-uppercase btn-lg"><a href="/">Return</a></button>'


# @app.route('/createassetbike')
# def createuser():
#
#     return

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)


@app.route('/createassett/<name>')
def CreateAsset():

    return app.send_static_file('createasset.html')

@app.route('/sendasset/<name>')
def SendAsset(name):
    asset.transferasset()
    return "asset has been transfered!"

@app.route('/viewasset')
def ViewAsset():
    tx = asset.view_asset()
    return jsonify(results=tx)

@app.route('/createasset/<name>/')
def SayHello(name):
    # asset = Asset(name)
    print(asset.get_asset_details())

    # message = {
    #     # 'message': 'You created the asset ' + asset.get_asset_details()
    #
    # }
    message = str(asset.get_asset_details())
    # return jsonify(results=message)
    return message
port = os.getenv('PORT', '5001')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
