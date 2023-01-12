from django.urls import path
from MyApp import views
# SET THE NAMESPACE!
app_name = 'MyApp'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    #path(r'^register/$',views.register, name='register'),
    path('/register/', views.register, name='register'),
    path('/login/', views.user_login, name='user_login'),
]
