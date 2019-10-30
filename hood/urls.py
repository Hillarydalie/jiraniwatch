from django.conf.urls import url,include
from . import views as main_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
# from .views import ImageCreateView

# Template URLS
app_name = 'awwwards'

urlpatterns = [
    path('', main_views.index , name = 'homepage'),
    path('signup/', main_views.signup, name='signup'),
    path('search/', main_views.search_results, name="search_results"),
    path('new/post/',main_views.new_post,name='post'),
    path('edit/',main_views.edit,name='edit'),
    url(r'^profile/(?P<profile_id>[-\w]+)/$', main_views.profile, name='profile'),
    path('new/business/',main_views.business,name='business'),
    path('hood/',main_views.neighbourhood,name='neighbourhood'),
    path('business/',main_views.bizdisplay,name='bizdisplay'),
    path('neighbourhood_display/', main_views.mtaadisplay, name='displayhood'),

]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)