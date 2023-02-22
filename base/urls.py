from django.urls import path

# it means whatever you upload a website first you import views
 
from.import views

urlpatterns = [
    path('login/',views.loginpage,name="login"),
     path('logout/',views.logoutuser,name="logout"),
     path('register/',views.registerpage,name="register"),

    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),

    # path('profile/<str:pk>/',views.userprofile,name="user-profile"),

    path('user-profile/<str:pk>/',views.userprofile,name="user-profile"),
    
    path('create-room/',views.createroom,name="create-room"),
    
    path('update-room/<str:pk>/',views.updateroom, name="update-room"),

    path('delete-room/<str:pk>/',views.deleteroom, name="delete-room"),

     path('delete-message/<str:pk>/',views.deletemessage, name="delete-message"),

    
]
 

#  <str/int/slug>--- these datatype we use