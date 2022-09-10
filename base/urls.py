from django.urls import path
from . import views


urlpatterns=[
    path('login/', views.loginpage, name='login'),
    path('register/', views.registeruser, name='register'),
     path('logout/', views.logoutUser, name='logout'),
    path("",views.home,name="home"),
    path('room/<str:pk>',views.room,name='room'),
    path('profile/<str:pk>',views.userProfile,name='user-profile'),
    path("create_room/",views.createroom,name="create-room"),
    path("update_room/<str:pk>",views.updateRoom,name="update-room"),
    path("delete_room/<str:pk>",views.deleteRoom,name="delete-room"),
    path("delete_message/<str:pk>",views.deleteMessage,name="delete-message"),
    path("update-user",views.updateUser,name="update-user"),
    path("topics",views.topicspage,name="topics"),
    path("activity",views.activitypage,name="activity")
    
]