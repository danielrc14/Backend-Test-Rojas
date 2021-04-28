"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import (
    path,
    include,
)
from django.shortcuts import redirect

from .utils.healthz import healthz


def home_view(request):
    if (
        request.user.is_authenticated
        and request.user.has_perm('menus.add_menu')
    ):
        return redirect('menus:menu_list')
    else:
        return redirect('login')


urlpatterns = [
    path("", home_view, name="home"),
    path("healthz", healthz, name="healthz"),
    path("menus/", include("menus.urls", namespace="menus")),
    path("users/", include("users.urls", namespace="users")),
    path("accounts/", include("django.contrib.auth.urls")),
]
