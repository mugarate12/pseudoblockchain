from app import api, app
from controllers.productController import Product
from controllers.usersController import User

if __name__ == "__main__":
  api.add_resource(Product, '/product', '/product')
  api.add_resource(User, '/users', '/users')

  app.run(port=3333, debug=True)
