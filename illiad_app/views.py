# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from illiad_app.models import V2_Helper

log = logging.getLogger(__name__)
v2_helper = V2_Helper()


def info( request ):
    """ Returns simplest response. """
    now = datetime.datetime.now()
    return HttpResponse( '<p>info</p> <p>( %s )</p>' % now )


def make_request_v2( request ):
    """ Handles current (October 2015) easyBorrow controller illiad call. """
    log.debug( 'starting' )
    if v2_helper.check_validity( request ) is False:
        return HttpResponseBadRequest( 'Please stop.' )
    v2_helper.run_request( request )
    now = datetime.datetime.now()
    return HttpResponse( '<p>request_v2</p> <p>( %s )</p>' % now )
