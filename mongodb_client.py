from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def product_exists(self, product_name):
        return self.collection.find_one({'name': product_name}) is not None

    def insert_product(self, product_name, description):
        self.collection.insert_one({'name': product_name, 'description': description})
        print(f"Inserted new product: {product_name}")

    def close(self):
        self.client.close()
