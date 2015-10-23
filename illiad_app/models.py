# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint, itertools
from django.conf import settings as project_settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_unicode
from django.utils.text import slugify

log = logging.getLogger(__name__)


class V2_Helper( object ):
    """ Handles easyBorrow v2 request. """

    def __init__( self ):
        self.place_holder = 'foo'

    def check_validity( self, request ):
        """ Checks post, auth_key, ip, & params.
            Called by make_request_v2() """
        log.debug( 'starting check_validity()' )
        return_val = False
        if request.method is 'POST' or project_settings.DEBUG is True:
            return_val = True
        log.debug( 'return_val, `%s`' % return_val )
        return return_val

    def check_params( self, request ):
        """ Checks params.
            Called by check_validity() """
        log.debug( 'starting check_params()' )
        return_val = None
        required_params = [ 'auth_key', 'openurl', 'request_id', 'username' ]
        for param in required_params:
            if param is not in request.POST.keys():
                return_val = False
                break
        if return_val is None:
            return_val = True
        log.debug( 'return_val, `%s`' % return_val )
        return return_val
