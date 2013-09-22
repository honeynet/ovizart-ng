from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ui.views.index'),
    url(r'^login/$', 'ui.views.login'),
    url(r'^logout/$', 'ui.views.logout'),
    url(r'^new/$', 'ui.views.upload_file'),
    url(r'^delete/$', 'ui.views.delete_analysis'),
    url(r'^show/(?P<analysisId>.+)$', 'ui.views.show_analysis'),
    url(r'^pcap/(?P<analysisId>.+)/(?P<streamKey>.+)', 'ui.views.download_pcap'),
    url(r'^reassembled/(?P<analysisId>.+)/(?P<streamKey>.+)/(?P<trafficType>[012])$', 'ui.views.download_reassembled'),
    url(r'^attachment/(?P<analysisId>.+)/(?P<streamKey>.+)/(?P<filePath>.+)$', 'ui.views.download_attachment')

)
