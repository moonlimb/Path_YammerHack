import unittest

from yammer import Yammer

class TestYammer(unittest.TestCase):
    def setUp(self):
        pass

    def teardown(self):
        pass

    def test_init(self):
        yammer_client = Yammer("foo", "bar")


if __name__ == '__main__':
    unittest.main()
