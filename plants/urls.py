from django.conf.urls import url, patterns, include

urlpatterns = patterns('',
    # url(r'^$', 'plants.views.result_list', name='plantLists'),
    url(r'^plantResults/$', 'plants.views.get_plant', name='plantResults'),
    url(r'^tagResult/$', 'plants.views.get_post_by_tag', name='tagResults'),
    url(r'^singlePost/$', 'plants.views.get_singlepost_by_post_id', name='singlepost'),
    url(r'^gallery/$', 'plants.views.gallary_for_each_plant', name='postResults'),
       )
