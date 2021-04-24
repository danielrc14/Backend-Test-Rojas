from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'', views.MenuListView.as_view(), name='menu_list'),
]
