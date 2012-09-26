=============
python-yammer
=============

Python library for interacting with the Yammer API.

python-yammer is forked from a project of Sunlight Labs (c) 2010,
written by James Turk <jturk@sunlightfoundation.com>. It has been
extended at McCann-Erickson by Adam Gschwender <adam.gschwender@mccann.com>.

All code is under a BSD-style license, see LICENSE for details.

| Homepage: http://github.com/McCannErickson/python-yammer/
| Source: http://github.com/McCannErickson/python-yammer/


Requirements
============

* python >= 2.4
* simplejson >= 1.8 (not required with python 2.6 or greater)
* python-oauth2 >= 1.1.3

Installation
============

The installation can be performed by running the following command::

    $ python setup.py install

It can also be installed via its egg at::

    http://github.com/McCannErickson/python-yammer/tarball/master#egg=python-yammer

Usage
=====

Including the library::

    from yammer import Yammer

Authorizing via OAuth2::

    client = Yammer(CONSUMER_KEY, CONSUMER_SECRET, oauth2=True, \
                        redirect_url='http://example.com/authenticate')
    # redirect user to client.get_authorize_url()
    return redirect(yammer.get_authorize_url())

Accepting authorization via OAuth2::

    client = Yammer(CONSUMER_KEY, CONSUMER_SECRET, oauth2=True)
    access_token = client.authenticate(request.GET.get('code'))
    # save access_token for future use

Interacting with the Yammer messages API::

    client = Yammer(CONSUMER_KEY, CONSUMER_SECRET, oauth2=True, \
                        access_token=access_token)
    msg_id = client.messages.post('My message', group_id=GROUP_ID)
    rv = client.messages.get(msg_id)
    client.messages.delete(msg_id)

Interacting with the Yammer like API::

    client = Yammer(CONSUMER_KEY, CONSUMER_SECRET, oauth2=True, \
                        access_token=access_token)
    client.likes.create(msg_id)
    client.likes.delete(msg_id)
