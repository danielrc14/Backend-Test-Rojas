from django.urls import path
from . import views


app_name = 'menus'
urlpatterns = [
    path('', views.MenuListView.as_view(), name='menu_list'),
    path('create/', views.MenuCreateView.as_view(), name='menu_create'),
    path('<int:pk>/', views.MenuDetailView.as_view(), name='menu_detail'),
    path('<int:pk>/update/', views.MenuUpdateView.as_view(), name='menu_update'),
]
