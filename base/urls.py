from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby, name='lobby'),
    path('room/', views.room, name='room'),
    path('get_token/', views.getToken, name='get_token'),
    path('create_member/', views.createMember, name='create_member'),
    path('get_member/', views.getMember, name='get_member'),
    path('delete_member/', views.deleteMember, name='delete_member'),
    path('get_room_status/', views.getRoomStatus, name='get_room_status'),  # Xonaning holatini olish
]
