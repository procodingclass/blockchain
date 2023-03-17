from flask import Flask, render_template, request,jsonify, redirect
import requests
from datetime import datetime

from web3 import Web3
app = Flask(__name__)


def sendETH(sender, receiver, secretKey, amount, gasFee, gasLimit):
    infuraUrl = 'https://sepolia.infura.io/v3/087c45ae45bf42bc91c8b07e02fd5d4d'
    web3InfuraConnection = Web3(Web3.HTTPProvider(infuraUrl))
    try:
        nonce = web3InfuraConnection.eth.getTransactionCount(sender)
        transaction = {
            'nonce': nonce,
            'to': receiver,
            'value': web3InfuraConnection.toWei(amount, 'ether'),
            'gas': int(gasLimit),
            'gasPrice': web3InfuraConnection.toWei(gasFee, 'gwei')
        }
        signedTransaction = web3InfuraConnection.eth.account.signTransaction(transaction, secretKey)
        transactionHash = web3InfuraConnection.eth.sendRawTransaction(signedTransaction.rawTransaction)
        print('Your transaction is successful. Your Transaction ID is:', transactionHash.hex())
        message = {"status":"success", "transactionId":transactionHash.hex()}
        print(message)
        return message

    except Exception as e:
        print(e)
        message = {"status":"failed", "message":"Please try again"}
        return message


def getEthBalance(accountAddress):
    infuraUrl = 'https://sepolia.infura.io/v3/087c45ae45bf42bc91c8b07e02fd5d4d'
    web3InfuraConnection = Web3(Web3.HTTPProvider(infuraUrl))

    try:
        # Convert the address to a checksummed format
        checksumAddress = web3InfuraConnection.toChecksumAddress(accountAddress)

        # Query the blockchain for the account balance
        balance = web3InfuraConnection.eth.get_balance(checksumAddress)

        # Convert the balance from wei to ether
        etherBalance = web3InfuraConnection.fromWei(balance, 'ether')
        output = {"status":"success", "balance":etherBalance}
        return output
    except:
        output = {"status":"failed"}
        return output

def getEthTransactions(accountAddress):
    apiKey = 'EIWQCHMWYYNAC3CIP6NAITGXEG9Y2A1DV7'
    apiUrl = f"https://api-sepolia.etherscan.io/api?module=account&action=txlist&address={accountAddress}&startblock=0&endblock=99999999&page=1&offset=10&sort=desc&apikey={apiKey}"
    response = requests.get(apiUrl)
    allTransactions = response.json()['result']
    print(allTransactions)

    for transaction in allTransactions:
        print("----------")

        transactionAmount = int(transaction['value']) / 10**18
        transactionTimeStamp = datetime.fromtimestamp(int(transaction['timeStamp']))
        transactionGasPrice = float(transaction['gasPrice']) * float(transaction['gasUsed']) * 10 ** -18

        transaction['timeStamp'] = transactionTimeStamp
        transaction['value'] = transactionAmount
        transaction['gasPrice'] = transactionGasPrice
        print(transaction['gasPrice'])

    output = {"status":"success", "allTransactions":allTransactions}
    return output


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/makeTransactionPage', methods=['GET', 'POST'])
def makeTransactionPage():
    return render_template('makeTransactionPage.html')


@app.route('/viewBalancePage', methods=['GET', 'POST'])
def viewBalancePage():
    return render_template('viewBalancePage.html')


@app.route('/viewAllTransactionPage', methods=['GET', 'POST'])
def viewAllTransactionPage():
    return render_template('viewAllTransactionPage.html')


@app.route('/makeTransaction', methods=['POST'])
def makeTransaction():
    if request.method == 'POST':
        sender = request.form['sender']
        receiver = request.form['receiver']
        secretKey = request.form['key']
        amount = request.form['amount']
        gasFee = request.form['gasFee']
        gasLimit = request.form['gasLimit']
        
        sendETHfunction = sendETH(sender, receiver, secretKey, amount, gasFee, gasLimit)
        return jsonify(sendETHfunction)
    

@app.route('/getBalance', methods=['POST'])
def getBalance():
    if request.method == 'POST':
        accountAddress = request.form['accountAddress']
        getEthBalanceFunction = getEthBalance(accountAddress)
        return jsonify(getEthBalanceFunction)

@app.route('/getTransactions', methods=['POST'])
def getTransactions():
    if request.method == 'POST':
        accountAddress = request.form['accountAddress']
        getEthTransactionsFunction = getEthTransactions(accountAddress)
        return jsonify(getEthTransactionsFunction)


if __name__ == '__main__':
    app.run()
