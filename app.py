from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={'/product': {"origins": "*"}, '/users': {"origins": "*"}, '/test': {"origins": "*"}})

@app.route('/test')
def test():
  return {
    'ok': 'ok'
  }, 200

api = Api(app)
