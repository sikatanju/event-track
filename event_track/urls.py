from django.urls import path

from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.event_home, name='event_home'),
    path('login/', views.authorize_user, name='authorize_user'),
    path('logout/', views.unauthorize_user, name='unauthorize_user'),
    path('register/', views.register_user, name='register_user'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('update-profile/', views.update_user, name='update_user'),
]