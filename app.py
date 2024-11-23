import os
import xmlrpc.client
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

app = Flask(__name__)

@app.route("/fields", methods=["GET"])
def get_fields():
    try:
        fields = models.execute_kw(
            ODOO_DB,
            uid,
            ODOO_PASSWORD,
            "product.product",
            "field_get",
            [],
            {"attributes": ["string", "type"]},
        )
        return jsonify(fields), 200
    except Exception as err:
        return jsonify({"Error": str(2)}), 500

if __name__ == "__main__":
    app.run(debug=True)