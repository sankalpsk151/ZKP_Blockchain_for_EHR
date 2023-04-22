import time
import os
import pickle
import hashlib
from flask import Flask, request
import requests
import json
from . import zkp_org


class Transaction:
    def __str__(self): return "Transaction: {} -> {} : {} {}".format(self.sender,
                                                                  self.recipient, self.amount,self.report)

    def __init__(self, sender, recipient, amount,report):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.report =report

    @classmethod
    def takeInput(cls):
        sender = input("Enter sender: ")
        recipient = input("Enter recipient: ")
        amount = input("Enter amount: ")
        report=input("Enter the report:")

        return cls(sender, recipient, amount,report)

    def verifyTransaction():
        
        pass


class Block:
    def __str__(self): return "Block: {} {}".format(
        self.index, self.previousHash)

    def __init__(self, index, timestamp, transactions, previousHash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.previousHash = previousHash
        # self.transactions = transactions
        # self.merkel_root = None

    @property
    def Hash(self):
        # hashData = self.previousHash + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        hashData = '{}{}{}{}'.format(
            self.previousHash, self.index, self.nonce, self.timestamp
        )
        return hashlib.sha256(hashData.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.difficulty = 4
        self.current_Transactions = []
        self.chain = [self.createGenesisBlock()]

    def createGenesisBlock(self):
        return Block(0, time.time(), [], 1)

    @property
    def getLastBlock(self):
        return self.chain[-1]

    # def newTransaction(self, sender, recipient, amount):
    #     self.current_Transactions.append(Transaction(sender, recipient, amount))
    #     return len(self.current_Transactions)

    # def newTransaction(self, transaction):
    #     self.current_Transactions.append(transaction)
    #     return len(self.current_Transactions)

    def addTransaction(self, transaction=None):
        transaction = Transaction.takeInput()
        self.current_Transactions.append(transaction)
        return len(self.current_Transactions)

    def viewTransactions(self):
        index = self.getLastBlock.index
        for i in range(0, index):
            print(self.current_Transactions[i])

    def addBlock(self, block, proof):
        previous_hash = self.getLastBlock.Hash
        if previous_hash != block.previousHash:
            return False
        if not self.isValidProof(block, proof):
            return False
        # block.Hash = proof
        self.chain.append(block)
        return True

    def mineBlock(self):
        if not self.current_Transactions:
            return False

        lastBlock = self.getLastBlock

        newBlock = Block(index=lastBlock.index + 1,
                         timestamp=time.time(),
                         transactions=self.current_Transactions,
                         previousHash=lastBlock.Hash)

        proof = self.proofOfWork(newBlock)
        self.addBlock(newBlock, proof)
        self.current_Transactions = []
        return newBlock.index

    def proofOfWork(self, block):
        block.nonce = 0
        computed_hash = block.Hash
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.Hash
        return computed_hash

    def isValidProof(self, block, block_hash):
        return (block_hash.startswith('0' * self.difficulty) and
                block_hash == block.Hash)


b = Blockchain()
if os.path.exists("blockchain.pickle"):
    with open("blockchain.pickle", "rb") as f:
        # unpickle the object and store it in a variable
        b = pickle.load(f)
else:
    b.addTransaction(Transaction("sender1", "recipient1", 1,"The patient has diabetes"))
    print(b.mineBlock())
    b.addTransaction(Transaction("sender2", "recipient2", 10,"The patient has cancer"))
    print(b.mineBlock())


while(int(input("Enter 1 if you want to add a transaction\n")) == 1):
    b.addTransaction()
    print(b.mineBlock())

# open a file to write the pickled blockchain object
with open("blockchain.pickle", "wb") as f:
    # pickle the blockchain object and write it to the file
    pickle.dump(b, f)
    # b.viewTransactions()

print("These are transactions ")
print(len(b.chain))
for i in b.chain:
    # print(i)
    for t in i.transactions:
        print(i, t)


app = Flask(__name__)

blockchain = b


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})


app.run(debug=True, port=5000)