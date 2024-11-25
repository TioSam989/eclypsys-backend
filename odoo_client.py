import os
import xmlrpc.client
from dotenv import load_dotenv

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")


class OdooClient:
    def __init__(self):
        self.url = ODOO_URL
        self.db = ODOO_DB
        self.username = ODOO_USERNAME
        self.password = ODOO_PASSWORD
        self.common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        self.uid = self.authenticate()

    def authenticate(self):
        return self.common.authenticate(self.db, self.username, self.password, {})

    def search_read(self, model, fields=None, domain=None, limit=None, offset=None):
        fields = fields or []
        domain = domain or []

        try:
            return self.models.execute_kw(
                self.db,
                self.uid,
                self.password,
                model,
                "search_read",
                [domain],
                {"fields": fields, "limit": limit, "offset": offset},
            )
        except xmlrpc.client.Fault as e:
            raise Exception(f"Failed to fetch data: {str(e)}")
