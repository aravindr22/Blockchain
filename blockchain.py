#To be installed
#Flask==0.12.2: pip install Flask==0.12.2

#Module 1- Creation of BlockChain

import datetime
import hashlib
import json
from flask import Flask,jsonify
from werkzeug.middleware.proxy_fix import ProxyFix


#Building a Blockchain

class Blockchain:
    
    #Initializing the chain and creating Genisis Block
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        #Creating a Block
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'prev_hash' : previous_hash
            }        
        #Appending the Block to Chain
        self.chain.append(block)
        return block
    
    #To get the details about previous block
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            previous_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
        return True
    
    
#BlockChain Mining
        
#Web page
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
#BlockChain Creation
blockchain = Blockchain()

#Mining Block
@app.route("/mine_block", methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, prev_hash)
    response = {
        'message': 'Congratulations, You have just mined a new Block',
        'index' : block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous hash': block['prev_hash']
                }
    return jsonify(response), 200

#Getting the full chain
@app.route('/get_chain', methods = ['GET'] )    
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
                }
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'] )    
def is_valid():
    is_valid1 = blockchain.is_chain_valid(blockchain.chain)
    if is_valid1:
        response = { 'message': 'The Blockchain is valid'}
    else:
        response = { 'message': 'The Blockchain is not valid'}
    return jsonify(response), 200

#Running the app
#app.run(host = '0.0.0.0', port = 5000)
if __name__ == '__main__':
    app.run()