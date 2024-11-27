from flask import Flask
from routes.products import products_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.register_blueprint(products_bp)

if __name__ == '__main__':
    app.run(debug=True)
