from app import api, app
from controllers.productController import Product
from controllers.usersController import User
from decouple import config

PORT = config('PORT')
api.add_resource(Product, '/product', '/product')
api.add_resource(User, '/users', '/users')

if __name__ == "__main__":
  app.run(port=int(PORT), debug=True)
