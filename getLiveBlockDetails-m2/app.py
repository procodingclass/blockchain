from web3 import Web3
from web3.middleware import geth_poa_middleware
from flask import Flask, render_template, request,jsonify
import datetime

app = Flask(__name__)

def getBlockData(blockNumber): 
    completeBlockData = []
    apiUrl = 'https://mainnet.infura.io/v3/ec5acb1175dc468c9f3ee9a84a02fe98' #student will add this
    web3 = Web3(Web3.HTTPProvider(apiUrl)) 
    getBlockData = web3.eth.getBlock(blockNumber) # any block can be taken

    blockData = {}
    blockData['totalDifficulty'] = getBlockData['totalDifficulty']
    blockData['blockNumber'] = getBlockData['number']
    blockData['size'] = getBlockData['size']
    blockData['currentHash'] = getBlockData['hash'].hex()
    blockData['previousHash'] = getBlockData['parentHash'].hex()

    transactionTimeStamp = datetime.datetime.fromtimestamp(getBlockData['timestamp'])
    readableDate = transactionTimeStamp.strftime("%Y-%m-%d %H:%M:%S")
    blockData['timestamp'] = readableDate

    numberOfTransactions = len(getBlockData['transactions'])
    blockData['numberOfTransactions'] = numberOfTransactions

    allTransactions = []
    for transaction in range(0, 10):
        transactionList = {}

        transactionHash = getBlockData['transactions'][transaction].hex()
        transactionList['transactionHash'] = transactionHash

        getTransaction = web3.eth.get_transaction(transactionHash)

        transactionList['receiver'] = getTransaction['to']
        transactionList['sender'] = getTransaction['from']

        transactionAmount = int(getTransaction['value']) / 10**18
        transactionList['amount'] = transactionAmount
        allTransactions.append(transactionList)

    blockData['transactions'] = allTransactions
    print(blockData)

    return blockData

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        blockNumber = request.form['blockNumber']
        getBlockDataFunction = getBlockData(int(blockNumber))
        return jsonify(getBlockDataFunction)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
