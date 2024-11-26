from flask import Blueprint, jsonify, request  # type: ignore
from odoo_client import OdooClient

odoo = OdooClient()

products_bp = Blueprint("products", __name__)

fields = ["name", "list_price", "type", "image_1920", "categ_id"]

@products_bp.route("/products", methods=["GET"])
def get_products():
    try:
        limit = request.args.get("limit", type=int, default=500)
        offset = request.args.get("offset", type=int, default=0)

        products = odoo.search_read(
            "product.product", fields=fields, limit=limit, offset=offset or 0
        )

        processed_products = [
            {
                "name": product.get("name", "Unknown"),
                "price": product.get("list_price", 0.0),
                "type": product.get("type", "Unknown"),
                "category": product.get("categ_id", "Uncategorized"),
                "img": (
                    f"data:image/png;base64,{product['image_1920']}"
                    if product.get("image_1920")
                    else ""
                ),
            }
            for product in products
        ]

        return jsonify(processed_products), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch products: {str(e)}"}), 500

@products_bp.route("/products/categories", methods=["GET"])
def get_categories_with_products():
    try:
        limit = request.args.get("limit", type=int, default=100)
        offset = request.args.get("offset", type=int, default=0)

        products = odoo.search_read(
            "product.product",
            fields=fields,
            limit=limit,
            offset=offset,
        )

        if not products:
            return jsonify({"error": "No products found"}), 404

        categories = {}
        for product in products:
            categ_data = product.get("categ_id")
            product_data = {
                "id": product.get("id"),
                "name": product.get("name", "Unknown"),
                "price": product.get("list_price", 0.0),
                "img": (
                    f"data:image/png;base64,{product.get('image_1920')}"
                    if product.get("image_1920")
                    else None
                ),
            }

            if not categ_data:
                categ_id = "000"
                categ_name = "Uncategorized"
            else:
                categ_id, categ_name = categ_data

            if categ_id not in categories:
                categories[categ_id] = {
                    "id": categ_id,
                    "name": categ_name,
                    "products": [],
                }

            categories[categ_id]["products"].append(product_data)

        categories_list = list(categories.values())

        return jsonify(categories_list), 200

    except Exception as err:
        return jsonify({"error": f"Failed to fetch categories: {str(err)}"}), 500
