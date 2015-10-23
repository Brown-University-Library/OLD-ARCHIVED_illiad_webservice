# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import Client, TestCase


class ClientV2_Test( TestCase ):
    """ Tests easyBorrow-api v2 """

    def test__check_bad_method( self ):
        """ Checks GET (api requires POST). """
        c = Client()
        response = c.get( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual(
            400,
            response.status_code )
        self.assertEqual(
            'Please stop.',
            response.content )

    def test__check_bad_post_params( self ):
        """ Tests title solr query. """
        c = Client()
        response = c.post( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual(
            400,
            response.status_code )
        self.assertEqual(
            'Please stop.',
            response.content )

    def test__check_good_post_params( self ):
        """ Tests title solr query. """
        c = Client()
        response = c.post( '/v2/make_request/', {'auth_key': 'foo_a', 'openurl': 'foo_b', 'request_id': 'foo_c', 'username': 'foo_d'} )
        self.assertEqual(
            200,
            response.status_code )
        self.assertEqual(
            True,
            'request_v2' in response.content )

    # end class ClientV2_Test()
