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
    path('add-event/', views.add_event, name='add_event'),
    path('<int:id>/', views.event_details, name='event_details'),
    path('my-events/', views.my_events, name='my_events'),
    path('my-events/<int:id>/', views.update_event, name='update_event'),
    path('my-events/delete/<int:id>/', views.delete_event, name='delete_event'),
    path('book-event/<int:event_id>/', views.book_an_event, name='book_an_event'),
    path('my-events/booked/', views.my_booked_events, name='my_booked_events'),
]