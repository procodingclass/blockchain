import hashlib
import json
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Block:
    def __init__(self,formData):
        self.chain = []
        self.getNewTransactions = formData
        self.count = 0
        self.newBlock(newBlockData="",previousHash="No previous Hash. Since this is the first block.")
        

    def newBlock(self,newBlockData, previousHash=None):
        if(newBlockData):
            newTransactions = newBlockData
            previousHash = self.chain[0]["currentHash"]
        else:
            newTransactions = self.getNewTransactions

        sender = newTransactions['senderName']
        senderHash = hashlib.sha256(sender.encode('utf-8')).hexdigest()
        receiver = newTransactions['receiverName']
        receiverHash = hashlib.sha256(receiver.encode('utf-8')).hexdigest()

        newTransactionsDumps = json.dumps(newTransactions)
        transactionHash = hashlib.sha256(newTransactionsDumps.encode('utf-8')).hexdigest()

        allTransactions = {
            'senderName': senderHash,
            'receiverName': receiverHash,
            'amount': newTransactions['amount'],
            'transaction Hash' : transactionHash
        }
    
        seconds = time.time()
        block = {
            'Block No': self.count,
            'timestamp': time.ctime(seconds),
            'transactions': allTransactions or 'No Transactions First Genesis Block',
            'gasfee': 0.1,
            'previousHash': previousHash,
        }
        self.count = self.count + 1
        self.chain.append(block)

        blockDumps = json.dumps(block)
        blockEncoded = blockDumps.encode()

        rawHash = hashlib.sha256(blockEncoded)
        hexHash = rawHash.hexdigest()
        block['currentHash'] = hexHash

        if(newBlockData):
            if(self.chain[0]["currentHash"] == self.chain[1]["previousHash"]):
                validation = {
                    "validation": "true"
                }
            else:
                validation = {
                    "validation": "false"
                }
            self.chain.append(validation)

        return block

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        formData = {
            'senderName': request.form['senderName'],
            'receiverName': request.form['receiverName'],
            'amount': request.form['amount']
        }
        blockClassObj = Block(formData)

        if(request.form['newBlockSenderName']):
            formData = {
                'senderName': request.form['newBlockSenderName'],
                'receiverName': request.form['newBlockReceiverName'],
                'amount': request.form['newBlockAmount']
            }
            blockClassObj.newBlock(formData)
        
        return jsonify(blockClassObj.chain)
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run()