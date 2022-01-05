import unittest
import pytarkovdata


class TestPytarkovdata(unittest.TestCase):
    def test_get_uid(self):
        assert pytarkovdata.get_uid('6B23-1') == '5c0e5bab86f77461f55ed1f3'

    def test_get_uid_fail(self):
        with self.assertRaises(Exception):
            pytarkovdata.get_uid('asdfg')
