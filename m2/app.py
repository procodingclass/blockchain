import hashlib
import json
import time
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Block(object):
    def __init__(self):
        self.chain = []
        self.new_transactions = []
        self.count = 0
        self.new_block(previous_hash="No previous Hash. Since this is the first block.", proof=100)

    def new_block(self, proof, previous_hash=None):
        seconds = time.time()
        block = {
            'Block No': self.count,
            'timestamp': time.ctime(seconds),
            'transactions': self.new_transactions or 'No Transactions First Genesis Block',
            'gasfee': 0.1,
            'nonce': proof,
            'previousHash': previous_hash or self.hash(self.chain[-1]) ,

        }
        self.new_transactions = []
        self.count = self.count + 1
        self.chain.append(block)

        return block

    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof_condition = False

        while check_proof_condition is False:
            compare_proof = new_proof ** 2 - previous_proof ** 2
            string_compare_proof = str(compare_proof).encode()
            encode_proof = hashlib.sha256(string_compare_proof)
            hash_proof = encode_proof.hexdigest()
            if hash_proof[:4] == '0000':
                check_proof_condition = True
            else:
                new_proof = new_proof + 1

        return new_proof

    def transaction(self, sender, receiver, amount):
        print(sender + " - " + receiver + " - " + amount)
        sender_encoder = hashlib.sha256(sender.encode())
        sender_hash = sender_encoder.hexdigest()
        receiverEncoder = hashlib.sha256(receiver.encode())
        receiverHash = receiverEncoder.hexdigest()

        transaction_data = {
            'sender': sender_hash,
            'receiver': receiverHash,
            'amount': amount
        }
        self.new_transactions.append(transaction_data)
        return self.last_block

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        block['currentHash'] = hex_hash
        return hex_hash

    def mine(self):
        last_block = blockchain.last_block()

        last_proof = last_block['nonce']

        proof = blockchain.proof_of_work(last_proof)

        last_hash = blockchain.hash(last_block)

        block = blockchain.new_block(proof, last_hash)
        return block

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['previousHash'] != previous_block['currentHash']:
                return False

            previous_nonce = previous_block['nonce']
            current_nonce = current_block['nonce']
            compare_proof = current_nonce ** 2 - previous_nonce ** 2

            string_compare_proof = str(compare_proof).encode()
            encode_compare_proof = hashlib.sha256(string_compare_proof)

            hash_compare_proof = encode_compare_proof.hexdigest()

            if hash_compare_proof[:4] != '0000':
                return False
            previous_block = current_block
            block_index = block_index + 1

        return True

    def resetBlockData(self):
        self.chain = []
        self.new_transactions = []
        self.count = 0
        self.new_block(previous_hash="No previous Hash. Since this is the first block.", proof=100)


blockchain = Block()
@app.route('/', methods=['GET', 'POST'])
def index():
    blockchain.resetBlockData()
    if request.method == 'POST':
        numberOfBlocks = int(request.form['numberOfBlocks'])
        for increment_block in range(1, numberOfBlocks + 1):
            print("Transaction details for block -",increment_block)
            numberOfTransactionInputName = 'B'+str(increment_block)+'numberOfTransaction'
            numberOfTransaction = request.form[numberOfTransactionInputName]
            print("Numbers of Transaction: ", numberOfTransaction)
            for increment_transaction in range(1, int(numberOfTransaction) +1):
                blockTransaction = 'B'+str(increment_block)+'T'+str(increment_transaction)
                sender = request.form[blockTransaction+'senderName']
                receiver = request.form[blockTransaction+'receiverName']
                amount = request.form[blockTransaction+'amount']
                transaction = blockchain.transaction(sender, receiver, amount)
            blockchain.mine()

        # print(blockchain.chain)
        valid = blockchain.chain_valid(blockchain.chain)
        if valid:
            print('The Blockchain is valid.')
            blockchain.chain.append("Validated")
        else:
            print('The Blockchain is not valid.')

        return jsonify(blockchain.chain)

        # return blockchain.chain
        # return render_template('blocks.html', blockData=blockchain.chain )
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()