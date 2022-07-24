from . import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('',views.home, name='home'),
    path('room/<id>/',views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<id>', views.update_room, name='update-room'),
    path('delete-room/<id>', views.delete_room, name='delete-room'),
    path('delete-message/<id>', views.delete_message, name='delete-message'),
    path('login/', views.login_page, name='login'),
    path('create-account/', views.signup_page, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/<username>/', views.user_profile, name='profile'),
    path('update-user/', views.update_user, name='update-user')
]