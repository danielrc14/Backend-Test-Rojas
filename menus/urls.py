from django.urls import path
from . import views


app_name = 'menus'
urlpatterns = [
    path('', views.MenuListView.as_view(), name='menu_list'),
    path('create/', views.MenuCreateView.as_view(), name='menu_create'),
    path('<int:pk>/', views.MenuDetailView.as_view(), name='menu_detail'),
    path(
        '<int:pk>/update/',
        views.MenuUpdateView.as_view(),
        name='menu_update'
    ),
    path(
        '<int:menu_pk>/create_option/',
        views.MenuOptionCreateView.as_view(),
        name='menuoption_create',
    ),
    path(
        'option/<int:pk>/update',
        views.MenuOptionUpdateView.as_view(),
        name='menuoption_update',
    ),
    path(
        'selections_list',
        views.MenuOptionSelectionListView.as_view(),
        name='selections_list',
    ),
    path(
        'send_link',
        views.SendMenuSelectionLinksView.as_view(),
        name='send_link',
    ),
]
