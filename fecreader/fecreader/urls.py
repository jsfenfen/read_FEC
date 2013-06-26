from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fecreader.views.home', name='home'),
    # url(r'^fecreader/', include('fecreader.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^base/$', TemplateView.as_view(template_name="test_templates/base.html")),
    url(r'^styletest/$', TemplateView.as_view(template_name="test_templates/styletest.html")),
    url(r'', include('public_views.datapages.urls')),    
)