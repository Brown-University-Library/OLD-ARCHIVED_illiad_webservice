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
        """ Checks post and auth_key and ip.
            Called by make_request_v2() """
        return_val = False
        log.debug( 'return_val, `%s`' % return_val )
        return return_val
