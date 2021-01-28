from flask_restful import Resource, reqparse, request
import bcrypt

from database.db import mydb


class User(Resource):
  TABLE_NAME = 'usuarios'

  def get(self):
    mycursor = mydb.cursor(buffered=True)

    email = request.args.get('email')
    password = request.args.get('senha')

    if email is None or password is None:
      return {
        'error': 'Fields Empty',
        'message': 'Email or Password query string not informed'
      }, 406
    
    mycursor.execute(f'SELECT senha FROM {self.TABLE_NAME} WHERE email="{email}"')
    myuser = mycursor.fetchone()
    user_password: str

    if myuser is None:
      return {
        'error': 'User invalid',
        'message': 'user information invalid'
      }, 406
    else:
      user_password = myuser[0]

    is_valid_password = bcrypt.checkpw(password.encode(), user_password.encode())
    if is_valid_password:
      mycursor.execute(f'SELECT email, tipo FROM {self.TABLE_NAME} WHERE email="{email}"')
      user = mycursor.fetchone()

      return {
        'email': user[0],
        'tipo': user[1]
      }, 200
    else:
      return {
        'error': 'Fields invalids',
        'message': 'Email ou password is invalid'
      }, 406

  def post(self):
    parser = reqparse.RequestParser()
    mycursor = mydb.cursor(buffered=True)

    parser.add_argument('email')
    parser.add_argument('senha')
    parser.add_argument('tipo')

    params = parser.parse_args()
    password = params['senha']
    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    sql = f'INSERT INTO {self.TABLE_NAME} (email, senha, tipo) VALUES (%s, %s, %s)'
    val = (params['email'], hash_password, params['tipo'])
    mycursor.execute(sql, val)

    mydb.commit()

    return {
      'sucess': 'Usuario criado com sucesso'
    }, 200
