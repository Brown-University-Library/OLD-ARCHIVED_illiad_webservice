# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint
from illiad.account import IlliadSession

# from django.conf import settings as project_settings
# from django.core.urlresolvers import reverse
# from django.db import models
# from django.http import HttpResponseRedirect
# from django.utils.encoding import smart_unicode
# from django.utils.text import slugify

log = logging.getLogger(__name__)


class V2_Helper( object ):
    """ Handles easyBorrow v2 request. """

    def __init__( self ):
        self.REMOTE_AUTH_URL = os.environ['ILLIAD_WS__REMOTE_AUTH_URL']
        self.REMOTE_AUTH_KEY = os.environ['ILLIAD_WS__REMOTE_AUTH_KEY']  # not the api-key


    def check_validity( self, request ):
        """ Checks post, auth_key, ip, & params.
            Called by make_request_v2() """
        log.debug( 'starting check_validity()' )
        return_val = False
        if request.method == 'POST':
            log.debug( 'method was POST' )
            if self.check_params( request ) is True:
                return_val = True
        log.debug( 'return_val, `%s`' % return_val )
        return return_val

    def check_params( self, request ):
        """ Checks params.
            Called by check_validity() """
        log.debug( 'starting check_params()' )
        log.debug( 'request.POST.keys(), `%s`' % request.POST.keys() )
        return_val = None
        for param in [ 'auth_key', 'openurl', 'request_id', 'username' ]:
            log.debug( 'on param, `%s`' % param )
            if param not in request.POST.keys():
                return_val = False
                break
        return_val = True if ( return_val is None ) else False
        log.debug( 'return_val, `%s`' % return_val )
        return return_val

    def run_request( self, request ):
        """ Runs module call.
            Called by views.make_request_v2() """
        ill = IlliadSession( self.REMOTE_AUTH_URL, self.REMOTE_AUTH_KEY, request.POST['username'] )
        ill = self._login( ill )
        request_key = self._get_request_key( ill, request.POST['openurl'] )
        if request_key['blocked'] is True:
            v2_response_dct = { 'status': 'login_failed_possibly_blocked' }
            log.debug( 'blocked v2_response_dct, `%s`' % v2_response_dct )
        else:
            submission_response_dct = self._make_request( ill, request_key )
            v2_response_dct = self.build_v2_submitted_response( submission_response_dct )
        return v2_response_dct

    def _login( self, ill ):
        """ Logs user in to ILLiad.
            Called by run_request() """
        try:
            ill.login()
            log.debug( 'illiad remote-auth login successful' )
            return ill
        except Exception as e:
            log.error( 'exception, `%s`' % unicode(repr(e)) )
            raise Exception( 'Could not log user into ILLiad' )

    def _get_request_key( self, ill, openurl ):
        """ Submits openurl to ILLiad to prepare data for request-submission.
            Returns dct.
            Called by run_request() """
        try:
            request_key = ill.get_request_key( openurl )
            log.debug( 'request_key, `%s`' % pprint.pformat(request_key) )
            return request_key
        except Exception as e:
            log.error( 'exception, `%s`' % unicode(repr(e)) )
            raise Exception( 'Problem submitting openurl to ILLiad' )

    def _make_request( self, ill, request_key ):
        """ Submits request to ILLiad.
            Called by run_request() """
        try:
            submission_response_dct = ill.make_request( request_key )
            log.debug( 'submission_response_dct, `%s`' % pprint.pformat(submission_response_dct) )
            return submission_response_dct
        except Exception as e:
            log.error( 'exception, `%s`' % unicode(repr(e)) )
            raise Exception( 'Problem submitting request to ILLiad' )

    def build_v2_submitted_response( self, submission_response_dct ):
        """ Builds proper ezb v2-dct for json response.
            Called by run_request() """
        if submission_response_dct['submitted'] is True:
            v2_response_dct = { 'status': 'submission_successful', 'transaction_number': submission_response_dct['transaction_number'] }
        else:
            v2_response_dct = { 'status': 'submission_failed', 'message': 'see illiad-webservice logs for more info' }
        log.debug( 'v2_response_dct, `%s`' % pprint.pformat(v2_response_dct) )
        return v2_response_dct

    # end class V2_Helper()
