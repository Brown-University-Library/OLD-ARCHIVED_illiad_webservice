# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json, random
from . import settings_app
from django.test import Client, TestCase


class ClientV2_Test( TestCase ):
    """ Tests easyBorrow-api v2 """

    def test__check_bad_method(self):
        """ GET (api requires POST) should return 400. """
        c = Client()
        response = c.get( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual( 400, response.status_code )
        self.assertEqual( 'Bad Request', response.content )

    def test__check_bad_post_params(self):
        """ POST with bad params should return 400. """
        c = Client()
        response = c.post( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual( 400, response.status_code )
        self.assertEqual( 'Bad Request', response.content )

    # def test__check_good_post_params__known_user(self):
    #     """ POST with good params should submit a request and return a transaction number.
    #         This test is good, just disabled so as not to submit unnecessary real requests. """
    #     c = Client()
    #     response = c.post(
    #         '/v2/make_request/',
    #         { 'auth_key': settings_app.TEST_AUTH_KEY, 'openurl': 'foo_b', 'request_id': 'foo_c', 'username': settings_app.TEST_EXISTING_GOOD_USER }
    #         )
    #     self.assertEqual( 200, response.status_code )
    #     response_dct = json.loads( response.content )
    #     self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
    #     self.assertEqual( 'submission_successful', response_dct['status'] )

    # def test__new_user(self):
    #     """ New user POST should submit a request and return a transaction number.
    #         TODO: This test needs work; it is disabled so as not to submit unnecessary real requests. """
    #     c = Client()
    #     username = '{test_root}{random}'.format( test_root=settings_app.TEST_NEW_USER_ROOT, random=random.randint(11111, 99999) )
    #     response = c.post(
    #         '/v2/make_request/',
    #         { 'auth_key': settings_app.TEST_AUTH_KEY, 'openurl': 'foo_b', 'request_id': 'foo_c', 'username': username }
    #         )
    #     self.assertEqual( 200, response.status_code )
    #     response_dct = json.loads( response.content )
    #     self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
    #     self.assertEqual( 'submission_successful', response_dct['status'] )

    # def test__blocked_user(self):
    #     """ TODO """

    # def test__disavowed_user(self):
    #     """ TODO """

    # end class ClientV2_Test()
