import unittest
import unittest.mock
import json
from lebonprix.crawler.search import Item
from lebonprix.crawler.search import Search


class TestItem(unittest.TestCase):
    def setUp(self):
        self.req_mock = unittest.mock.Mock()
        self.item = {
            'list_id': 1234,
            'other_data': {
                'qwe': 'qwe'
            }
        }
        self.resp = unittest.mock.Mock()
        self.resp.text = json.dumps(self.item)

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_init_works(self, cache):
        i = Item(1234, self.req_mock)

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_in_cache_returns_true_if_cache_returns_data(self, cache):
        cache().get.return_value = self.item
        i = Item(1234, self.req_mock)
        self.assertTrue(i.in_cache())

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_in_cache_returns_false_if_cache_returns_none(self, cache):
        cache().get.return_value = None
        i = Item(1234, self.req_mock)
        self.assertFalse(i.in_cache())

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_call_returns_cached_data_if_up_to_date(self, cache):
        cache().get.return_value = self.item
        i = Item(1234, self.req_mock)
        res = i()
        self.assertEqual(res, self.item)

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_call_makes_post_request_if_no_cached_data(self, cache):
        cache().get.return_value = None
        self.req_mock.post.return_value = self.resp
        i = Item(1234, self.req_mock)
        i()
        self.req_mock.post.assert_called_once_with(
            url = 'https://mobile.leboncoin.fr/templates/api/view.json',
            params = {'ad_id': 1234},
            data = {**i.DATA, **{'ad_id': 1234}},
            headers = i.HEADERS
        )

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_call_returns_data_from_post_if_no_cached_data(self, cache):
        cache().get.return_value = None
        self.req_mock.post.return_value = self.resp
        i = Item(1234, self.req_mock)
        res = i()
        self.assertEqual(res, self.item)

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_call_updates_cache_if_no_cached_data(self, cache):
        cache().get.return_value = None
        self.req_mock.post.return_value = self.resp
        i = Item(1234, self.req_mock)
        res = i()
        cache().set.assert_called_once_with(self.item)

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_call_updates_cache_if_missing_some_additional_data(self, cache):
        cache().get.return_value = self.item
        self.req_mock.post.return_value = self.resp
        i = Item(1234, self.req_mock, {'missing_data': 'asd'})
        res = i()
        cache().set.assert_called_once_with(
            {**self.item, **{'missing_data': 'asd'}}
        )

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_call_returns_cache_with_additional_data(self, cache):
        cache().get.return_value = self.item
        self.req_mock.post.return_value = self.resp
        i = Item(1234, self.req_mock, {'missing_data': 'asd'})
        res = i()
        self.assertEqual(res, {**self.item, **{'missing_data': 'asd'}})

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_call_returns_post_data_with_additional_data_when_no_cache(self, cache):
        cache().get.return_value = None
        self.req_mock.post.return_value = self.resp
        i = Item(1234, self.req_mock, {'missing_data': 'asd'})
        res = i()
        self.assertEqual(res, {**self.item, **{'missing_data': 'asd'}})

    @unittest.mock.patch('lebonprix.crawler.search.Cache')
    def test_call_sets_cache_with_post_data_and_additional_data_when_no_cache(self, cache):
        cache().get.return_value = None
        self.req_mock.post.return_value = self.resp
        i = Item(1234, self.req_mock, {'missing_data': 'asd'})
        res = i()
        cache().set.assert_called_once_with(
            {**self.item, **{'missing_data': 'asd'}}
        )


class TestSearch(unittest.TestCase):
    def setUp(self):
        pass
    
    @unittest.mock.patch('lebonprix.crawler.search.Item')
    def test_init_works(self, item):
        Search(10, ['key1'])


if __name__ == '__main__':
    unittest.main()