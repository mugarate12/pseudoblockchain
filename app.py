from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app, resources={'/product': {"origins": "*"}, '/users': {"origins": "*"}})
api = Api(app)
