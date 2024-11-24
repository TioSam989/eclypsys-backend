from flask import Blueprint, jsonify, request
from odoo_client import OdooClient

odoo = OdooClient()
products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    """Retrieve all products"""
    try:
        products = odoo.search_read('product.product', fields=['name', 'list_price', 'type'])
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": f"Failed to f]etch products: {str(e)}"}), 500
