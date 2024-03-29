"""plantySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include,patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'plants.views.homepage', name='homepage'),
    url(r'^plants/', include('plants.urls')),
    url(r'^searchResults/', 'plants.views.result_list'),
    url(r'^tagResult/', 'plants.views.get_post_by_tag'),
    url(r'^nativePlant/', 'plants.views.get_native_plant', name='nativePlant'),
    url(r'^upvote/(?P<post_id>\w+)/$', 'plants.views.upVotes', name='vote'),
    url(r'^downvote/(?P<post_id>\w+)/$', 'plants.views.downVotes', name='vote'),
]

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
