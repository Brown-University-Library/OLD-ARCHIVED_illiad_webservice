# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint
from illiad.account import IlliadSession


log = logging.getLogger(__name__)


class V2_Helper( object ):
    """ Handles easyBorrow v2 request. """

    def __init__( self, request_id ):
        self.request_id = request_id
        self.API_KEY = os.environ['ILLIAD_WS__API_AUTH_KEY']
        self.REMOTE_AUTH_URL = os.environ['ILLIAD_WS__REMOTE_AUTH_URL']
        self.REMOTE_AUTH_KEY = os.environ['ILLIAD_WS__REMOTE_AUTH_KEY']  # not the api-key

    def check_validity( self, request ):
        """ Checks post, auth_key, ip, & params.
            Called by make_request_v2() """
        log.debug( '%s - starting check_validity()' % self.request_id )
        return_val = False
        if request.method == 'POST':
            if self.check_params( request ) is True:
                if request.POST['auth_key'] == self.API_KEY:
                    return_val = True
                else:
                    log.debug( '%s - ip, `%s`' % (self.request_id, request.META.get('REMOTE_ADDR', 'unavailable')) )
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    def check_params( self, request ):
        """ Checks params.
            Called by check_validity() """
        log.debug( '%s - starting check_params()' % self.request_id )
        log.debug( '%s - request.POST, `%s`' % (self.request_id, request.POST) )
        return_val = None
        for param in [ 'auth_key', 'openurl', 'request_id', 'username' ]:
            log.debug( '%s - on param, `%s`' % (self.request_id, param) )
            if param not in request.POST.keys():
                return_val = False
                break
        return_val = True if ( return_val is None ) else False
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    # def check_params( self, request ):
    #     """ Checks params.
    #         Called by check_validity() """
    #     log.debug( '%s - starting check_params()' % self.request_id )
    #     return_val = None
    #     for param in [ 'auth_key', 'openurl', 'request_id', 'username' ]:
    #         log.debug( '%s - on param, `%s`' % (self.request_id, param) )
    #         if param not in request.POST.keys():
    #             return_val = False
    #             break
    #     return_val = True if ( return_val is None ) else False
    #     log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
    #     return return_val

    def run_request( self, request ):
        """ Runs module call.
            Called by views.make_request_v2() """
        ill = IlliadSession( self.REMOTE_AUTH_URL, self.REMOTE_AUTH_KEY, request.POST['username'] )
        ill = self._login( ill )
        request_key = self._get_request_key( ill, request.POST['openurl'] )
        if request_key['blocked'] is True:
            v2_response_dct = { 'status': 'login_failed_possibly_blocked' }
            log.debug( '%s - blocked v2_response_dct, `%s`' % (self.request_id, v2_response_dct) )
        else:
            submission_response_dct = self._make_request( ill, request_key )
            v2_response_dct = self.build_v2_submitted_response( submission_response_dct )
        return v2_response_dct

    def _login( self, ill ):
        """ Logs user in to ILLiad.
            Called by run_request() """
        try:
            ill.login()
            log.debug( '%s - illiad remote-auth login successful' % self.request_id )
            return ill
        except Exception as e:
            log.error( '%s - exception, `%s`' % (self.request_id, unicode(repr(e))) )
            raise Exception( 'Could not log user into ILLiad' )

    def _get_request_key( self, ill, openurl ):
        """ Submits openurl to ILLiad to prepare data for request-submission.
            Returns dct.
            Called by run_request() """
        try:
            request_key = ill.get_request_key( openurl )
            log.debug( '%s - request_key, `%s`' % (self.request_id, pprint.pformat(request_key)) )
            return request_key
        except Exception as e:
            log.error( '%s - exception, `%s`' % (self.request_id, unicode(repr(e))) )
            raise Exception( 'Problem submitting openurl to ILLiad' )

    def _make_request( self, ill, request_key ):
        """ Submits request to ILLiad.
            Called by run_request() """
        try:
            submission_response_dct = ill.make_request( request_key )
            log.debug( '%s - submission_response_dct, `%s`' % (self.request_id, pprint.pformat(submission_response_dct)) )
            return submission_response_dct
        except Exception as e:
            log.error( '%s - exception, `%s`' % (self.request_id, unicode(repr(e))) )
            raise Exception( 'Problem submitting request to ILLiad' )

    def build_v2_submitted_response( self, submission_response_dct ):
        """ Builds proper ezb v2-dct for json response.
            Called by run_request() """
        if submission_response_dct['submitted'] is True:
            v2_response_dct = { 'status': 'submission_successful', 'transaction_number': submission_response_dct['transaction_number'] }
        else:
            v2_response_dct = { 'status': 'submission_failed', 'message': 'see illiad-webservice logs for more info' }
        log.debug( '%s - v2_response_dct, `%s`' % (self.request_id, pprint.pformat(v2_response_dct)) )
        return v2_response_dct

    # end class V2_Helper()
