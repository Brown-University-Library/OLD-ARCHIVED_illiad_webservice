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



def info( request ):
    """ Returns simple response. """
    doc_url = os.environ['ILLIAD_WS__DOCS']
    now = datetime.datetime.now()
    referrer = request.META.get( 'REMOTE_ADDR', 'unavailable' )
    dct = { 'date_time': unicode(now), 'docs': doc_url, 'ip': referrer }
    output = json.dumps( dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def make_request_v2( request ):
    """ Handles current (October 2015) easyBorrow controller illiad call. """
    log.debug( 'starting' )
    # log.debug( 'request.__dict__, `%s`' % pprint.pformat(request.__dict__) )
    v2_helper = V2_Helper( request.POST.get('request_id', 'no_id') )
    if v2_helper.check_validity( request ) is False:
        return HttpResponseBadRequest( 'Bad Request' )
    v2_response_dct = v2_helper.run_request( request )
    output = json.dumps( v2_response_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )
