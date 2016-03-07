"""vocab_site URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from vocab import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.login, name="login"),
    url(r'^accounts/logout/$', views.logout_view, name="logout"),
    url(r'^$', views.home, name="home"),
    url(r'^createURI$', views.createURI, name="createURI"),
    url(r'^createUser$', views.createUser, name="createUser"),
    url(r'^createVocab$', views.createVocab, name="createVocab"),
    url(r'^searchResults$', views.searchResults, name="searchResults"),
    url(r'^userProfile$', views.userProfile, name="userProfile"),
]
