from models.block import Block

class BlockChain:

  @staticmethod
  def valid_hash(hash: str):
    return hash.startswith('0000')

  def add(self, block: Block, database_instance):
    TABLE_NAME = 'produtos'
    mycursor = database_instance.cursor()

    while not self.valid_hash(block.hash()):
      block.nonce += 1

    # preparar os dados pra gravação no banco
    if block.data['tipo'] == 'comercializacao':
      mycursor.execute(f'SELECT product_id FROM {TABLE_NAME} ORDER BY product_id DESC LIMIT 1')
      last_product_id = mycursor.fetchone()
      product_id = 0
      print(last_product_id)
      if last_product_id is not None:
        if last_product_id[0] is not None:
          product_id = last_product_id[0]

      my_block_data = {
        'tipo': None,
        'quantidade_em_litros': None,
        'ITGU': None,
        'localizacao': None,
        'temperatura': None,
        'data': None,
        'qualidade_do_produto': None,
        'lote': None,
        'product_id': product_id + 1
      }

      my_block_data = {**my_block_data, **block.data}
      # inserindo dados no banco
      sql = f'INSERT INTO {TABLE_NAME} (hash, process_id, nonce, num_block, tipo, quantidade_em_litros, ITGU, localizacao, temperatura, data, qualidade_do_produto, lote, product_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
      val = (block.hash(), block.process_id, block.nonce, block.num_block, my_block_data['tipo'],
             my_block_data['quantidade_em_litros'], my_block_data['ITGU'], my_block_data['localizacao'],
             my_block_data['temperatura'], block.createdAt, my_block_data['qualidade_do_produto'],
             my_block_data['lote'], my_block_data['product_id'])
      mycursor.execute(sql, val)

      database_instance.commit()
      mycursor.fetchall()
    else:
      my_block_data = {
        'tipo': None,
        'quantidade_em_litros': None,
        'ITGU': None,
        'localizacao': None,
        'temperatura': None,
        'data': None,
        'qualidade_do_produto': None,
        'lote': None
      }

      my_block_data = {**my_block_data, **block.data}
      # inserindo dados no banco
      sql = f'INSERT INTO {TABLE_NAME} (hash, process_id, nonce, num_block, tipo, quantidade_em_litros, ITGU, localizacao, temperatura, data, qualidade_do_produto, lote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
      val = (block.hash(), block.process_id, block.nonce, block.num_block, my_block_data['tipo'], my_block_data['quantidade_em_litros'], my_block_data['ITGU'], my_block_data['localizacao'], my_block_data['temperatura'], block.createdAt, my_block_data['qualidade_do_produto'], my_block_data['lote'])
      mycursor.execute(sql, val)

      database_instance.commit()
      mycursor.fetchall()

  def mount_block_to_validate(self, data, previous_hash):
    my_block_data = {
      'tipo': data[4],
      'quantidade_em_litros': data[5],
      'ITGU': data[6],
      'localizacao': data[7],
      'temperatura': data[8],
      'data': data[9],
      'qualidade_do_produto': data[10],
      'lote': data[11],
      'product_id': data[12]
    }

    block = Block(my_block_data, data[3], previous_hash, data[1])
    block.nonce = data[2]
    return block

  def is_valid_new_block(self, latest_num_block, actual_num_block, database_cursor):
    TABLE_NAME = 'produtos'
    number_of_validate_blocks = 6

    while (latest_num_block - number_of_validate_blocks) < 0:
      number_of_validate_blocks -= 1

    offset = actual_num_block - number_of_validate_blocks
    limit = number_of_validate_blocks

    database_cursor.execute(f'SELECT * FROM {TABLE_NAME} ORDER BY num_block LIMIT {limit} OFFSET {offset}')
    blocks = database_cursor.fetchall()

    for i in range(len(blocks) - 1):
      myblock = self.mount_block_to_validate(blocks[i + 1], blocks[i][0])
      myhash = myblock.hash()

      if myhash != myblock.hash():
        return False

    return True
