import mysql.connector
from models.blockchain import BlockChain
from models.block import Block
from decouple import config

APP_MODE = config('FLASK_ENV')
DATABASE_HOST = config('DATABASE_HOST')
DATABASE_SERVER_NAME = config('DATABASE_NAME')
DATABASE_USER = config('DATABASE_USER')
DATABASE_PASSWORD = config('DATABASE_PASSWORD')

print(APP_MODE)
print(DATABASE_HOST)
print(DATABASE_SERVER_NAME)
print(DATABASE_PASSWORD)
print(DATABASE_USER)


def create_table_products(database_cursor):
  TABLE_NAME = 'produtos'
  database_cursor.execute('SHOW TABLES')
  tables = database_cursor.fetchall()

  have_table = False
  for table in tables:
    if table[0] == TABLE_NAME:
      have_table = True
      break

  # CREATE TABLE IF NOT EXISTS
  if not have_table:
    database_cursor.execute(f'CREATE TABLE {TABLE_NAME} '
                            '(hash VARCHAR(255) PRIMARY KEY,'
                            'process_id INT,'
                            'nonce INT,'
                            'num_block INT,'
                            'tipo VARCHAR(30),'
                            'quantidade_em_litros INT,'
                            'ITGU INT,'
                            'localizacao VARCHAR(255),'
                            'temperatura FLOAT,'
                            'data VARCHAR(255),'
                            'qualidade_do_produto INT,'
                            'lote VARCHAR(255),'
                            'product_id VARCHAR(255))')


def create_table_users(database_cursor):
  TABLE_NAME = 'usuarios'
  database_cursor.execute('SHOW TABLES')
  tables = database_cursor.fetchall()

  have_table = False
  for table in tables:
    if table[0] == TABLE_NAME:
      have_table = True
      break

  if not have_table:
    database_cursor.execute(f'CREATE TABLE {TABLE_NAME} '
                            '(id INT AUTO_INCREMENT PRIMARY KEY,'
                            'email VARCHAR(255) UNIQUE,'
                            'senha VARCHAR(255),'
                            'tipo VARCHAR(255))')

mydb = None

if (APP_MODE == 'development'):
  mydb = mysql.connector.connect(
    host=DATABASE_HOST,
    username=DATABASE_USER,
    password=DATABASE_PASSWORD
  )

  DATABASE_NAME = 'blockchain'
  mycursor = mydb.cursor()
  mycursor.execute('Show Databases')

  have_a_database = False
  for name_of_database in mycursor:
    if name_of_database[0] == DATABASE_NAME:
      have_a_database = True
      break

  if have_a_database:
    mydb = mysql.connector.connect(
      host='localhost',
      username='root',
      password='majuge123',
      database=DATABASE_NAME
    )

    mycursor = mydb.cursor()
    create_table_products(mycursor)
    create_table_users(mycursor)

  else:
    mycursor.execute(f'CREATE DATABASE {DATABASE_NAME}')
    mydb = mysql.connector.connect(
      host='localhost',
      username='root',
      password='majuge123',
      database=DATABASE_NAME
    )

    mycursor = mydb.cursor()
    create_table_products(mycursor)
    create_table_users(mycursor)
else:
  mydb = mysql.connector.connect(
    host=DATABASE_HOST,
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    database=DATABASE_SERVER_NAME,
    use_pure=True,
    ssl_disabled=True
  )
  mycursor = mydb.cursor()
  create_table_products(mycursor)
  create_table_users(mycursor)

# DATABASE_NAME = 'blockchain'
# mycursor = mydb.cursor()
# mycursor.execute('Show Databases')
#
# have_a_database = False
# for name_of_database in mycursor:
#   if name_of_database[0] == DATABASE_NAME:
#     have_a_database = True
#     break
#
# if have_a_database:
#   mydb = mysql.connector.connect(
#     host='localhost',
#     username='root',
#     password='majuge123',
#     database=DATABASE_NAME
#   )
#
#   mycursor = mydb.cursor()
#   create_table_products(mycursor)
#   create_table_users(mycursor)
#
# else:
#   mycursor.execute(f'CREATE DATABASE {DATABASE_NAME}')
#   mydb = mysql.connector.connect(
#     host='localhost',
#     username='root',
#     password='majuge123',
#     database=DATABASE_NAME
#   )
#
#   mycursor = mydb.cursor()
#   create_table_products(mycursor)
#   create_table_users(mycursor)
