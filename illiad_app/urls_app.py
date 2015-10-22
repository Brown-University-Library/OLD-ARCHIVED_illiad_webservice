# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView


urlpatterns = patterns('',

    url( r'^info/$',  'illiad_app.views.info', name='info_url' ),

    url( r'^v2/make_request/$',  'illiad_app.views.make_request_v2', name='request_v2' ),

    url( r'^$',  RedirectView.as_view(pattern_name='info_url') ),

    )
