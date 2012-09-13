import httplib2
try:
    import json
except ImportError:
    import simplejson as json
import time
import urllib
import urlparse
import oauth2 as oauth

class Yammer(object):
    base_url = 'https://www.yammer.com/api/v1/'

    def __init__(self, *args, **kwargs):
        use_oauth2 = False
        if 'oauth2' in kwargs:
            use_oauth2 = bool(kwargs['oauth2'])
            del kwargs['oauth2']
        if use_oauth2:
            self.client = _YammerOAuth2Client(*args, **kwargs)
        else:
            self.client = _YammerOAuthClient(*args, **kwargs)
        self.messages = _MessageEndpoint(self)
        self.groups = _GroupEndpoint(self)
        self.users = _UserEndpoint(self)
        self.likes = _LikeEndpoint(self)

    def _apicall(self, endpoint, method, **params):
        url = '%s%s' % (self.base_url, endpoint)
        body = ''
        cleaned_params = dict([(k,v) for k,v in params.iteritems() if v])

        if cleaned_params:
            body = urllib.urlencode(cleaned_params)
            if method in ['GET', 'DELETE']:
                url = '%s?%s' % (url, body)
                body = ''

        resp, content = self.client.request(url, method=method, body=body)
        if resp.status == 401:
            raise UnauthorizedError()
        elif resp.status == 404:
            raise NotFoundError()
        elif resp.status not in [200, 201]:
            raise UnknownError('invalid http response: %d' % resp.status)

        try:
            json_obj = json.loads(content)
            if 'response' in json_obj \
                    and json_obj['response'].get('stat', None) == 'fail':
                raise YammerError(json_obj['response']['message'])
            return json_obj
        except ValueError:
            if method in ['POST', 'DELETE'] and not bool(content.strip()):
                # empty response acceptable for posts and deletes
                return dict()
            raise UnknownError('invalid response')

    def __getattr__(self, name):
        return getattr(self.client, name)


class _YammerOAuthClient(object):
    def __init__(self, consumer_key, consumer_secret,
                 oauth_token=None, oauth_token_secret=None,
                 request_token_url=None, access_token_url=None,
                 authorize_url=None):
        self.request_token_url = 'https://www.yammer.com/oauth/request_token' \
            if request_token_url is None else request_token_url
        self.access_token_url = 'https://www.yammer.com/oauth/access_token' \
            if access_token_url is None else access_token_url
        self.authorize_url = 'https://www.yammer.com/oauth/authorize' \
            if authorize_url is None else authorize_url

        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        if oauth_token and oauth_token_secret:
            self.token = oauth.Token(oauth_token, oauth_token_secret)
        else:
            self.token = None
        self.client = oauth.Client(self.consumer, self.token)

    @property
    def request_token(self):
        if not hasattr(self, '_request_token'):
            self._request_token = self._get_token(self.request_token_url)
        return self._request_token

    def get_authorize_url(self):
        return "%s?oauth_token=%s" \
            % (self.authorize_url, self.request_token.key)

    def get_access_token(self, oauth_verifier):
        # set verifier
        if not self.token:
            token = self.request_token
        else:
            token = self.token
        token.set_verifier(oauth_verifier)
        self.client = oauth.Client(self.consumer, token)
        return self._get_token(self.access_token_url, "POST")

    def verify(self, oauth_verifier):
        self.token = self.get_access_token(oauth_verifier)
        self.client = oauth.Client(self.consumer, self.token)
        return self.token

    def _get_token(self, url, method="GET"):
        resp, content = self.client.request(url, method)
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])
        d = dict(urlparse.parse_qsl(content))
        return oauth.Token(d['oauth_token'], d['oauth_token_secret'])

    def __getattr__(self, name):
        return getattr(self.client, name)


class _YammerOAuth2Client(object):
    def __init__(self, consumer_key, consumer_secret,
                 access_token=None, redirect_url=None,
                 access_token_url=None, authorize_url=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.redirect_url = redirect_url
        self.authorize_url = 'https://www.yammer.com/dialog/oauth' \
            if authorize_url is None else authorize_url
        self.access_token_url = \
            'https://www.yammer.com/oauth2/access_token.json' \
            if access_token_url is None else access_token_url
        self.client = httplib2.Http()

    def get_authorize_url(self):
        qs = dict(client_id=self.consumer_key, redirect_uri=self.redirect_url)
        qs = {x : y for x, y in qs.items() if y is not None}
        return "%s?%s" % (self.authorize_url, urllib.urlencode(qs))

    def authenticate(self, code):
        qs = dict(client_id=self.consumer_key,
                  client_secret=self.consumer_secret,
                  code=code)
        qs = {x : y for x, y in qs.items() if y is not None}
        url = "%s?%s" % (self.access_token_url, urllib.urlencode(qs))
        resp, content = self.client.request(url, 'GET')
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        d = dict()
        try:
            json_obj = json.loads(content)
            if 'error' in json_obj:
                raise YammerError(json_obj['error']['message'])
            d = json_obj.get('access_token', dict())
        except ValueError:
            raise UnknownError('invalid response')

        if 'token' not in d:
            raise YammerError('invalid access token response')
        self.access_token = d['token']
        return self.access_token

    def request(self, *args, **kwargs):
        if self.access_token is not None:
            if 'headers' not in kwargs:
                kwargs['headers'] = \
                    dict({'Authorization': 'Bearer %s' % self.access_token})
            else:
                kwargs['headers']['Authorization'] = \
                    'Bearer %s' % self.access_token
        return self.client.request(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.client, name)


class _Endpoint(object):
    def __init__(self, yammer):
        self.yammer = yammer

    def _get(self, endpoint, **params):
        return self.yammer._apicall(endpoint, 'GET', **params)

    def _post(self, endpoint, **params):
        return self.yammer._apicall(endpoint, 'POST', **params)

    def _delete(self, endpoint, **params):
        return self.yammer._apicall(endpoint, 'DELETE', **params)


class _MessageEndpoint(_Endpoint):
    def all(self, **kwargs):
        """Returns all messages

        Keyword arguments:
        older_than -- returned messages must be older than the supplied id
        newer_than -- returned messages must be newer than the supplied id
        threaded -- possible values:
                        true (only show first message of thread)
                        extended (show first/two most recent messages of thread)
        limit -- return only the specified number of messages
        """
        return self._get_msgs('messages.json', **kwargs)

    def get(self, id, **kwargs):
        """Returns the supplied message; see all() for keywords"""
        return self._get_msgs('messages/%d.json' % id, **kwargs)

    def sent(self, **kwargs):
        """Returns sent messages; see all() for keywords"""
        return self._get_msgs('messages/sent.json', **kwargs)

    def received(self, **kwargs):
        """Returns received messages; see all() for keywords"""
        return self._get_msgs('messages/received.json', **kwargs)

    def private(self, **kwargs):
        """Returns private messages to the user; see all() for keywords"""
        return self._get_messages('messages/private.json', **kwargs)

    def following(self, **kwargs):
        """Returns followed messages; see all() for keywords"""
        return self._get_msgs('messages/following.json', **kwargs)

    def from_user(self, id, **kwargs):
        """Returns messages from the given user; see all() for keywords"""
        return self._get_msgs('messages/from_user/%d.json' % id, **kwargs)

    def from_bot(self, id, **kwargs):
        """Deprecated; no longer implemented"""
        raise NotImplementedError

    def about_topic(self, id, **kwargs):
        """Returns messages within the given topic; see all() for keywords"""
        return self._get_msgs(
            'messages/about_topic/%d.json' % id, **kwargs)

    def tagged_width(self, id, **kwargs):
        """Alias to about_topic()"""
        return self.about_topic(id)

    def in_group(self, id, **kwargs):
        """Returns messages within the given group; see all() for keywords"""
        return self._get_msgs('messages/in_group/%d.json' % id, **kwargs)

    def liked_by(self, id, **kwargs):
        """Returns liked messages; see all() for keywords"""
        return self._get_msgs('messages/liked_by/%d.json' % id, **kwargs)

    def favorites_of(self, id, **kwargs):
        """Alias to liked_by()"""
        return self.liked_by(id, **kwargs)

    def in_thread(self, id, **kwargs):
        """Returns messages within the thread; see all() for keywords"""
        return self._get_msgs('messages/in_thread/%d.json' % id, **kwargs)

    def post(self, body, **kwargs):
        """Create a message with the given body

        Keyword arguments:
        group_id -- The group id to post the message to
        replied_to_id -- The message id to reply to
        direct_to_id -- The user id to send a private message to
        broadcast -- If message should be broadcast (admin only)
        topics -- A list of topics (max 20)
        pending_attachments -- A list of pending attachment ids (max 20)
        og_<property> -- Open graph properties
        """
        if not body:
            raise ValueError('body is required')

        if not kwargs.get('group_id') and not kwargs.get('direct_to_id') \
                and not kwargs.get('replied_to_id'):
            raise ValueError(
                'group_id, replied_to_id, or direct_to_id must be supplied')
        self._convert_list_to_keys(kwargs, 'topics', 'topic', size=20)
        self._convert_list_to_keys(
            kwargs, 'pending_attachments', 'pending_attachment', size=20)

        kwargs['body'] = body
        return self._post('messages.json', **kwargs)

    def delete(self, id):
        """Delete the message with the given id"""
        return self._delete('messages/%d' % id)

    def _get_msgs(self, endpoint, **kwargs):
        rv = self._get(endpoint,
                       older_than=kwargs.get('older_than'),
                       newer_than=kwargs.get('newer_than'),
                       threaded=kwargs.get('threaded'),
                       limit=kwargs.get('limit'))
        return rv

    def _convert_list_to_keys(self, args, list_key, item_key, size=None):
        if not list_key in args:
            return

        if not args.get(list_key):
            args[list_key] = []
        elif not isinstance(args.get(list_key), list):
            args[list_key] = [args.get(list_key)]

        if size is not None and len(args.get(list_key)) > size:
            raise ValueError('%s length must not exceed %d' % (list_key, size))
        for x in range(len(args.get(list_key))):
            args['%s%d' % (item_key, x + 1)] = args.get(list_key)[x]

        del args[list_key]


class _GroupEndpoint(_Endpoint):
    def all(self, **kwargs):
        """Lists all groups

        Keyword arguments:
        page -- return groups on the page, 1-based
        letter -- return only groups starting with the letter
        sort_by -- possible values: messages, members, privacy, created_at,
                   creator
        reverse -- reverse the sort order
        """
        return self._get('groups.json', **kwargs)

    def get(self, id):
        """Get the group with the supplied id"""
        return self._get('groups/%d.json' % id)

    def create(self, name, private=None):
        """Create a new group with the supplied name"""
        return self._post('groups', name=name, private=private)

    def update(self, id, name, private=None):
        """Update an existing group"""
        return self._post('groups/%d' % id, name=name, private=private)


class _UserEndpoint(_Endpoint):
    def all(self, **kwargs):
        """Lists all users

        Keyword arguments:
        page -- return users on the page, 1-based
        letter -- returning users beginning wit the given letter
        sort_by -- possible values: messages, followers
        reverse -- reverse the sort order
        """
        return self._get('users.json', **kwargs)

    def get(self, id):
        """Get the user with the supplied id"""
        return self._get('users/%d.json' % id)

    def current(self):
        """Get the currently logged in user"""
        return self._get('users/current.json')

    def by_email(self, email):
        """Get the user matching the supplied email address"""
        return self._get('users/by_email.json', email=email)


class _LikeEndpoint(_Endpoint):
    def create(self, message_id, user_id=None):
        """Like the supplied message

        Keyword arguments:
        user_id -- The user id that likes the message, otherwise current user
        """
        if user_id is not None:
            url = 'messages/liked_by/%d.json' % user_id
        else:
            url = 'messages/liked_by/current.json'
        return self._post(url, message_id=message_id)

    def delete(self, message_id, user_id=None):
        """Remove like from the supplied message

        Keyword arguments:
        user_id -- The user id that likes the message, otherwise current user
        """
        if user_id is not None:
            url = 'messages/liked_by/%d.json' % user_id
        else:
            url = 'messages/liked_by/current.json'
        return self._delete(url, message_id=message_id)


class UnauthorizedError(Exception):
    """Request to Yammer has not been authorized."""
    pass

class NotFoundError(Exception):
    """Yammer could not find the requested resource."""
    pass

class YammerError(Exception):
    """Yammer responded with a failure message."""
    pass

class UnknownError(Exception):
    """Unexpected error from Yammer."""
    pass
