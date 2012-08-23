import argparse
import sys
import unittest

import yammer

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

class TestYammer(unittest.TestCase):
    def setUp(self):
        pass

    def teardown(self):
        pass

    def test_init(self):
        client = yammer.Yammer(CONSUMER_KEY, CONSUMER_SECRET)

    def test_unauthorized(self):
        client = yammer.Yammer(CONSUMER_KEY, CONSUMER_SECRET)
        self.assertRaises(yammer.UnauthorizedError, client.messages.all)

    def test_get_authorize_url(self):
        client = yammer.Yammer(CONSUMER_KEY, CONSUMER_SECRET)
        client.get_authorize_url()

        client = yammer.Yammer(CONSUMER_KEY, CONSUMER_SECRET, oauth2=True)
        client.get_authorize_url()

    def test_authenticate(self):
        client = yammer.Yammer(CONSUMER_KEY, CONSUMER_SECRET, oauth2=True)
        self.assertRaises(Exception, client.authenticate, ["0000000000000000"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the yammer client tests')
    parser.add_argument('--key', help='yammer application key', required=True,
                        nargs='?', default='')
    parser.add_argument('--secret', help='yammer application secret',
                        required=True, nargs='?', default='')
    parser.add_argument('extra', nargs='*',
                        help='additional arguments to send to the unittest')

    args = parser.parse_args()
    sys.argv[1:] = args.extra

    CONSUMER_KEY = args.key
    CONSUMER_SECRET = args.secret

    unittest.main()
