from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

cipherCode = {
    'a' : 'z',
    'b' : 'y',
    'c' : 'x',
    'd' : 'w',
    'e' : 'v',
    'f' : 'u',
    'g' : 't',
    'h' : 's',
    'i' : 'r',
    'j' : 'q',
    'k' : 'p',
    'l' : 'o',
    'm' : 'n',
    'n' : 'm',
    'o' : 'l',
    'p' : 'k',
    'q' : 'j',
    'r' : 'i',
    's' : 'h',
    't' : 'g',
    'u' : 'f',
    'v' : 'e',
    'w' : 'd',
    'x' : 'c',
    'y' : 'b',
    'z' : 'a',
}

decipherCode = {
    'z' : 'a' ,
    'y' : 'b' ,
    'x' : 'c' ,
    'w' : 'd' ,
    'v' : 'e' ,
    'u' : 'f' ,
    't' : 'g' ,
    's' : 'h' ,
    'r' : 'i' ,
    'q' : 'j' ,
    'p' : 'k' ,
    'o' : 'l' ,
    'n' : 'm' ,
    'm' : 'n' ,
    'l' : 'o' ,
    'k' : 'p' ,
    'j' : 'q' ,
    'i' : 'r' ,
    'h' : 's' ,
    'g' : 't' ,
    'f' : 'u' ,
    'e' : 'v' ,
    'd' : 'w' ,
    'c' : 'x' ,
    'b' :  'y' ,
    'a' : 'z' ,
}


def cipher(sender, receiver, amount):
    cipherText = ""
    transactionCipher = {}

    sender = sender.lower()
    for char in sender:
        if char in cipherCode:
            cipherText += cipherCode[char]
        else:
            cipherText += char
    transactionCipher["sender"] = cipherText

    cipherText = ""
    receiver = receiver.lower()
    for char in receiver:
        if char in cipherCode:
            cipherText += cipherCode[char]
        else:
            cipherText += char
    transactionCipher["receiver"] = cipherText

    transactionCipher["amount"] = amount

    return transactionCipher


def decipher(sender, receiver, amount):
    decipherText = ""
    transactionDecipher = {}

    sender = sender.lower()
    for char in sender:
        if char in decipherCode:
            decipherText += decipherCode[char]
        else:
            decipherText += char
    transactionDecipher["sender"] = decipherText
    

    decipherText = ""
    receiver = receiver.lower()
    for char in receiver:
        if char in decipherCode:
            decipherText += decipherCode[char]
        else:
            decipherText += char
    transactionDecipher["receiver"] = decipherText

    transactionDecipher["amount"] = amount
    return transactionDecipher

@app.route('/decipher', methods=['POST'])
def performDecipher():
  data = request.get_json()
  sender = data["senderName"]
  receiver = data["receiverName"]
  amount = data["amount"]
  decipherOutput = decipher(sender, receiver, amount)
  print(decipherOutput)
  return jsonify(decipherOutput)
  
@app.route('/', methods=['GET', 'POST'])
def performcipher():
    if request.method == 'POST':
        sender = request.form["senderName"]
        receiver = request.form["receiverName"]
        amount = request.form["amount"]
        cipherOutput = cipher(sender, receiver, amount)
        return jsonify(cipherOutput)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()