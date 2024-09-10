from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('', views.home, name="home"), 
    path('thread/<str:thread_pk>/', views.thread, name="thread"), 
    path('thread/<str:thread_pk>/post/<str:post_pk>/', views.post, name="post"), 
    path('create-thread/', views.create_thread, name="create-thread"), 
    path('update-thread/<str:thread_pk>', views.update_thread, name="update-thread"), 
    path('create-post/', views.create_post, name="create-post"), 
    path('update-post/<str:post_pk>', views.update_post, name="update-post"), 
    path('delete-post/<str:post_pk>', views.delete_post, name="delete-post")
]