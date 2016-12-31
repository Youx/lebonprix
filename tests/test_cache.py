import unittest, unittest.mock
from lebonprix.cache import Cache


class TestCache(unittest.TestCase):
    def setUp(self):
        self.item = {
            'list_id': 1234,
            'other_data': {
                'qwe': 'qwe'
            }
        }

    def test_init_creates_client(self):
        with unittest.mock.patch('lebonprix.cache.pymongo') as pymongo:
            c = Cache()
            pymongo.MongoClient.assert_called_once_with()

    def test_init_creates_index_on_items_list_id(self):
        with unittest.mock.patch('lebonprix.cache.pymongo') as pymongo:
            c = Cache()
            pymongo.MongoClient().lebonprix.items.create_index.assert_called_once_with('list_id')
    
    def test_get_finds_one_item_by_list_id(self):
        with unittest.mock.patch('lebonprix.cache.pymongo') as pymongo:
            c = Cache()
            c.get(1234)
            pymongo.MongoClient().lebonprix.items.find_one.assert_called_once_with(
                {'list_id': 1234}
            )
    
    def test_get_returns_mongo_data(self):
        with unittest.mock.patch('lebonprix.cache.pymongo') as pymongo:
            c = Cache()
            pymongo.MongoClient().lebonprix.items.find_one.return_value = self.item
            res = c.get(1234)
            self.assertEqual(res, self.item)

    def test_set_upserts_item_with_list_id(self):
        item = {
            'list_id': 1234,
            'other_data': {
                'qwe': 'qwe'
            }
        }
        with unittest.mock.patch('lebonprix.cache.pymongo') as pymongo:
            c = Cache()
            c.set(self.item)
            pymongo.MongoClient().lebonprix.items.update.assert_called_once_with(
                {'list_id': 1234},
                self.item,
                upsert=True
            )