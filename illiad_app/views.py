# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

log = logging.getLogger(__name__)


def info( request ):
    """ Returns simplest response. """
    now = datetime.datetime.now()
    return HttpResponse( '<p>info</p> <p>( %s )</p>' % now )


def make_request_v2( request ):
    """ Handles current (October 2015) easyBorrow controller illiad call. """
    now = datetime.datetime.now()
    return HttpResponse( '<p>request_v2</p> <p>( %s )</p>' % now )
