from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
#from .views import UserRetrieval
#from .views import UserValidate
import views

urlpatterns = {
  url(r'^twitter_login/$', views.twitter_login, name='twitter_login'),
  url(r'^twitter_home/$', views.twitter_home, name='twitter_home'),
  url(r'^twitter_logout/$', views.twitter_logout, name='twitter_logout'),
  url(r'^twitter_register/$',views.twitter_register, name='register'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
