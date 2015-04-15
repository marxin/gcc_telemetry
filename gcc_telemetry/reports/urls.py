from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^list$', views.list, name='list'),
    url(r'^(?P<report_base_id>[0-9]+)/$', views.detail, name = 'detail')
]
