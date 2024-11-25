from flask import Blueprint, jsonify, request  # type: ignore
from odoo_client import OdooClient

odoo = OdooClient()

products_bp = Blueprint("products", __name__)

fields = ["name", "list_price", "type", "image_1920", "categ_id"]


@products_bp.route("/products", methods=["GET"])
def get_products():
    try:
        limit = request.args.get("limit", type=int, default=10)
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


@products_bp.route("/products/by-category", methods=["GET"])
def get_products_by_category():
    try:
        limit = request.args.get("limit", type=int, default=100)
        offset = request.args.get("offset", type=int, default=500)

        products = odoo.search_read(
            "product.product",
            fields=["id", "categ_id"],
            limit=limit,
            offset=offset,
        )

        for product in products:
            categ_id = product.get("categ_id")

            if not categ_id:
                product_id = product.get("id")
                odoo.models.execute_kw(
                    odoo.db,
                    odoo.uid,
                    odoo.password,
                    "product.product",
                    "unlink",
                    [[product_id]],
                )

        categories = []

        for product in products:
            categ_id = product.get("categ_id")

            if categ_id:
                categories.append({"id": categ_id[0], "name": categ_id[1]})
            else:
                categories.append({"id": "000", "name": "Uncategorized"})

        return jsonify(categories), 200

    except Exception as err:
        return jsonify({"error": f"Failed to fetch categories: {str(err)}"}), 500


@products_bp.route("/products/bestsellers", methods=["GET"])
def get_bestsellers():
    try:
        limit = request.args.get("limit", type=int, default=5)

        products = odoo.search_read(
            "product.product", fields=fields + ["sales_count"], limit=limit
        )

        bestsellers = sorted(
            products, key=lambda x: x.get("sales_count", 0), reverse=True
        )[:limit]

        processed_bestsellers = [
            {
                "name": product.get("name", "Unknown"),
                "list_price": product.get("list_price", 0.0),
                "type": product.get("type", "Unknown"),
                "img": (
                    f"data:image/png;base64,{product.get('image_1920', '')}"
                    if product.get("image_1920")
                    else ""
                ),
                "sales_count": product.get("sales_count", 0),
            }
            for product in bestsellers
        ]

        return jsonify(processed_bestsellers), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch bestsellers: {str(e)}"}), 500
