import argparse
import mock
import sys
import unittest

import yammer


class TestYammerOAuth(unittest.TestCase):
    def setUp(self):
        self.key = 'key'
        self.secret = 'secret'
        # self.key = 'ik52ElwSuf527gAfukukQ'
        # self.secret = 'pGNJ2N9p0UB9qZRxq1H8mL9Ii2l1GSrlQD6lhM6JRUE'

    def teardown(self):
        pass

    def test_init(self):
        y = yammer.Yammer(self.key, self.secret)

    def test_unauthorized(self):
        y = self._make_client()
        self.assertRaises(yammer.UnauthorizedError, y.messages.all)

    @mock.patch('httplib2.Http.request')
    def test_get_authorize_url(self, mockHttpRequest):
        y = self._make_client()

        def mock_request(_client, _uri, **_kwargs):
            return ({'status': '200'}, 'oauth_token=request_key&oauth_token_secret=request_secret&oauth_callback_confirmed=true')

        mockHttpRequest.side_effect = mock_request
        y.get_authorize_url()

    @mock.patch('httplib2.Http.request')
    def test_verify(self, mockHttpRequest):
        y = self._make_client(oauth_token='request_key',
                              oauth_token_secret='request_secret')

        def mock_request(_client, _uri, **_kwargs):
            return ({'status': '200'}, 'oauth_token=access_key&oauth_token_secret=access_secret&oauth_callback_confirmed=true')

        mockHttpRequest.side_effect = mock_request
        token = y.verify('0000')
        self.assertEqual(token.key, 'access_key')
        self.assertEqual(token.secret, 'access_secret')

    def _make_client(self, **kwargs):
        return yammer.Yammer(self.key, self.secret, **kwargs)


class TestYammerOAuth2(unittest.TestCase):
    def setUp(self):
        self.key = 'key'
        self.secret = 'secret'
        self.redirect_url = 'http://localhost/callback'

    def teardown(self):
        pass

    def test_init(self):
        y = self._make_client()

    def test_unauthorized(self):
        y = self._make_client()
        self.assertRaises(yammer.UnauthorizedError, y.messages.all)

    def test_get_authorize_url(self):
        y = self._make_client()
        y.get_authorize_url()

    @mock.patch('httplib2.Http.request')
    def test_authenticate(self, mockHttpRequest):
        y = self._make_client()

        def mock_request(_client, _uri, **_kwargs):
            return ({'status': '200'}, '{"access_token":{"token":"access_token"}}')

        mockHttpRequest.side_effect = mock_request
        token = y.authenticate('0000')
        self.assertEqual(token, 'access_token')

    def _make_client(self, **kwargs):
        return yammer.Yammer(self.key, self.secret,
                             oauth2=True, redirect_url=self.redirect_url,
                             **kwargs)


if __name__ == "__main__":
    unittest.main()
