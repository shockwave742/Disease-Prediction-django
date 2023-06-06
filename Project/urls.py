"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from MyApp import views as v1
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v1.index),
    path('home', v1.index, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("signup/", v1.SignUpView.as_view(), name="signup"),
    path('profile', v1.profile_view, name='profile_view'),
    path('reports', v1.reports_view, name='reports_view'),
    path('input-symptoms', v1.input_symptoms_view, name='input_symptoms_view'),
    path('error', v1.error_token_view, name='error_token_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
'''
