# from bloco import Block
from database.db import mydb
from models.block import Block
from models.blockchain import BlockChain

if __name__ == "__main__":
    blockchain = BlockChain()
    print(mydb)
    block = Block({}, 0, '000000000', '00000000000')


    # bloco1Data = {
    #   'productName': 'A',
    #   'user': 'Fulano'
    # }
    # bloco2Data = {
    #   'productName': 'A',
    #   'user': 'Cicrano'
    # }
    #
    # bloco1 = Block(bloco1Data)
    # bloco2 = Block(bloco2Data)
    #
    # blockchain.add(bloco1)
    # blockchain.add(bloco2)

    # print(blockchain.get_all()[1].data)
    # print(blockchain.get_all()[1].hash())
    # for block in blockchain.get_all():
    #   print(block.createdAt)

