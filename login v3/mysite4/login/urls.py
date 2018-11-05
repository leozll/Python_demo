from django.conf.urls import patterns, url
from login import views

 
urlpatterns = patterns('',
    url(r'^login/$',views.login, name='login'),
    url(r'^success/$',views.success,name = 'success'),
)