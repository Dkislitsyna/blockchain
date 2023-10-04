import json
import hashlib


class Block:
    def __init__(self, index, timestamp, data, previousHash=' '):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.hash = self.calculateHash()


    def __dict__(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previousHash": self.previousHash,
            "hash": self.hash
        }


    def calculateHash(self):
        return hashlib.sha256((str(self.index) + self.previousHash + self.timestamp + self.data).\
                              encode('utf-8')).hexdigest()


    def printBlock(self):
        print("Block #" + str(self.index))
        print("Timestamp #" + str(self.timestamp))
        print("Data: " + str(self.data))
        print("Block Hash: " + str(self.hash))
        print("Block Previous Hash: " + str(self.previousHash))
        print("---------------")


class BlockChain:
    def __init__(self):
        self.chain = [self.createGenesisBlock()]


    def createGenesisBlock(self):
        return Block(0, "04/10/2023", "Genesis Block", "0")


    def getLatestBlock(self):
        return self.chain[len(self.chain) - 1]


    def addBlock(self, newBlock):
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.hash = newBlock.calculateHash()
        self.chain.append(newBlock)


    def isChainValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]
            # checks whether data has been tampered with
            if currentBlock.hash != currentBlock.calculateHash():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False
            return True


    def printBlockChain(self):
        for i in range(1, len(self.chain)):
            self.chain[i].printBlock()


    def saveToJson(self):
        with open('data.json', 'w') as outfile:
            for i in range(1, len(self.chain)):
                json.dump(self.chain[i].__dict__(), outfile)


def main():
    MegaBeast = BlockChain()
    MegaBeast.addBlock(Block(1, "01/10/2023", "One"))
    MegaBeast.addBlock(Block(2, "02/10/2023", "Two"))
    MegaBeast.addBlock(Block(3, "03/10/2023", "Three"))
    MegaBeast.addBlock(Block(4, "04/10/2023", "Four"))
    MegaBeast.printBlockChain()
    # no tampering in our block chain yet so should be true here
    print ("Chain valid? " + str(MegaBeast.isChainValid()))
    MegaBeast.saveToJson()


# Only run the main() function, if this is the root script running.
# This allows importing this script file to use its functions inside other scripts.
if __name__ == '__main__':
    main()

