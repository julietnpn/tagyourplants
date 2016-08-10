from django.conf.urls import url, patterns, include

urlpatterns = patterns('',
    url(r'^$', 'plants.views.result_list', name='plantLists'),
    url(r'^plantResults/$', 'plants.views.get_plant', name='plantResults'),
    url(r'^tagResult/$', 'plants.views.get_post_by_tag', name='tagResults'),
       )
