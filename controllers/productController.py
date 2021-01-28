from flask_restful import Resource, reqparse, request

from database.db import mydb
from models.block import Block
from models.blockchain import BlockChain


class Product(Resource):

  def get_product_by_process_id(self, process_id):
    mycursor = mydb.cursor(buffered=True)
    TABLE_NAME = 'produtos'

    if process_id is None:
      return {
        'error': 'Process ID Error',
        'message': 'process_id query string not informed'
      }, 406

    mycursor.execute(f'SELECT * FROM {TABLE_NAME} where process_id={process_id}')
    myblocks = mycursor.fetchall()

    response_data = []
    for block in myblocks:
      if block[4] == 'producao':
        response_data.append({
          'quantidade_em_litros': block[5],
          'localizacao': block[7],
          'temperatura': block[8],
          'ITGU': block[6],
          'tipo': block[4]
        })
      elif block[4] == 'transporte':
        response_data.append({
          'temperatura': block[8],
          'tipo': block[4]
        })
      elif block[4] == 'industria':
        response_data.append({
          'data': block[9],
          'temperatura': block[8],
          'qualidade_do_produto': block[10],
          'tipo': block[4]
        })
      else:
        response_data.append({
          'data': block[9],
          'lote': block[11],
          'product_id': block[12],
          'tipo': block[4]
        })

    return {
      'process_id': process_id,
      'blocks': response_data
           }, 200

  def get_product_by_product_id(self, product_id):
    mycursor = mydb.cursor(buffered=True)
    TABLE_NAME = 'produtos'

    if product_id is None:
      return {
        'error': 'Product ID Error',
        'message': 'product_id query string not informed'
      }, 406

    mycursor.execute(f'SELECT process_id FROM {TABLE_NAME} where product_id={product_id}')
    result = mycursor.fetchone()
    process_id: int
    if result is None:
      return {
        'error': 'Product Id Error',
        'message': 'product_id invalid'
      }, 406
    else:
      process_id = result[0]

    mycursor.execute(f'SELECT * FROM {TABLE_NAME} where process_id={process_id}')
    myblocks = mycursor.fetchall()

    response_data = []
    for block in myblocks:
      if block[4] == 'producao':
        response_data.append({
          'quantidade_em_litros': block[5],
          'localizacao': block[7],
          'temperatura': block[8],
          'ITGU': block[6],
          'tipo': block[4]
        })
      elif block[4] == 'transporte':
        response_data.append({
          'temperatura': block[8],
          'tipo': block[4]
        })
      elif block[4] == 'industria':
        response_data.append({
          'data': block[9],
          'temperatura': block[8],
          'qualidade_do_produto': block[10],
          'tipo': block[4]
        })
      else:
        response_data.append({
          'data': block[9],
          'lote': block[11],
          'product_id': block[12],
          'tipo': block[4]
        })

    return {
      'blocks': response_data
    }, 200

  def get(self):
    process_id = request.args.get('process_id')
    product_id = request.args.get('product_id')

    if product_id is not None:
      return self.get_product_by_product_id(product_id)
    else:
      return self.get_product_by_process_id(process_id)

  def post(self):
    parser = reqparse.RequestParser()
    mycursor = mydb.cursor(buffered=True)
    blockchain = BlockChain()
    TABLE_NAME = 'produtos'

    tipo = request.args.get('tipo')
    parser.add_argument('quantidade_em_litros')
    parser.add_argument('ITGU')
    parser.add_argument('temperatura')
    parser.add_argument('localizacao')
    parser.add_argument('data')
    parser.add_argument('qualidade_do_produto')
    parser.add_argument('lote')
    parser.add_argument('process_id')

    params = parser.parse_args()
    block_data = {**params, "tipo": tipo}
    process_id: int

    # Caso não haja o bloco inicial vazio da blockchain, o cria
    mycursor.execute(f'SELECT * FROM {TABLE_NAME}')
    haveBlockGenesis = len(mycursor.fetchall())
    if haveBlockGenesis == 0:
      block = Block({'tipo': 'Head'}, 0, '000000000', 0)
      blockchain.add(block, mydb)

    # procuro o ultimo process_id que iniciei, e incremento um para o novo
    if block_data['tipo'] == 'producao':
      mycursor.execute(f'SELECT process_id from {TABLE_NAME} ORDER BY process_id DESC LIMIT 1')
      latest_process_id = mycursor.fetchone()[0]

      process_id = latest_process_id + 1
    # procuro se existem blocos com o process_id informado
    else:
      if params['process_id'] is not None:
        mycursor.execute(f'SELECT process_id from {TABLE_NAME} where process_id={params["process_id"]}')
        # retorna None se não tiver registros
        process_id_tuple = mycursor.fetchone()

        if process_id_tuple is None:
          return {
            'error': 'process_id Error',
            'message': 'process_id not exists in database'
          }, 406
        else:
          process_id = process_id_tuple[0]
      else:
        return {
          'error': 'process_id Error',
          'message': 'process_id not informed'
        }, 406

    # quero pegar o hash e número do ultimo bloco adicionado
    mycursor.execute(f'SELECT num_block, hash from {TABLE_NAME} ORDER BY num_block DESC LIMIT 1')
    latest_block_data = mycursor.fetchone()
    if latest_block_data is None:
      return {
        'error': 'Block Error',
        'message': 'cannot get data of lastest block'
      }, 406
    else:
      numblock = latest_block_data[0] + 1
      previous_hash = latest_block_data[1]

    block = Block(block_data, numblock, previous_hash, process_id)
    # validar o hash desse bloco
    is_valid_block = blockchain.is_valid_new_block(latest_block_data[0], numblock, mycursor)
    if is_valid_block is False:
      return {
        'error': 'Blockchain Error',
        'message': 'Blockchain invalidate this block'
      }

    # inserir de fato na blockchain
    blockchain.add(block, mydb)

    return {
      "sucess": "Bloco adicionado com sucesso!"
    }, 200
