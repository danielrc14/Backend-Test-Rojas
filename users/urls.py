from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path(
        'menu_selection/<uuid:uuid>/',
        views.SelectMenuOptionView.as_view(),
        name='menu_selection',
    ),
]
