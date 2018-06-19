import pymongo


class Mongo:

    def __init__(self, db, collection):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client[db]
        self.coll = self.db[collection]

    def insert(self, document):
        return self.coll.insert(document)

    def insert_many(self, documents):
        resutls = self.coll.insert_many(documents)
        return resutls.inserted_ids

    def __del__(self):
        self.client.close()
