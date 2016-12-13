import pymongo


class Cache:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn.lebonprix
        self.db.items.create_index('list_id')

    def get(self, item_id):
        return self.db.items.find_one({"list_id": item_id})

    def set(self, item):
        cur = self.db.items.update({'list_id': item['list_id']},
                                   item, upsert=True)
