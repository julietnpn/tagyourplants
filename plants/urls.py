from django.conf.urls import url, patterns, include

urlpatterns = patterns('',
    # url(r'^$', 'plants.views.result_list', name='plantLists'),
    url(r'^plantResults/$', 'plants.views.get_plant', name='plantResults'),
    url(r'^tagResult/$', 'plants.views.get_post_by_tag', name='tagResults'),
    url(r'^singlePost/$', 'plants.views.get_singlepost_by_post_id', name='singlepost'),
    url(r'^upvote/(?P<postID>[0-9]+)/$', 'plants.views.upvote', name='upvote'),
    # url(r'^singlePost/upvote', 'plants.views.postVotes', name='postVotes'),
    )
