from app import api, app
from controllers.productController import Product
from controllers.usersController import User
from decouple import config

PORT = config('PORT')

if __name__ == "__main__":
  api.add_resource(Product, '/product', '/product')
  api.add_resource(User, '/users', '/users')

  app.run(port=int(PORT), debug=True)
