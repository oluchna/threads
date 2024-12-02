from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('', views.home, name="home"), 
    path('thread/<str:thread_pk>/', views.thread, name="thread"), 
    path('thread/<str:thread_pk>/post/<str:post_pk>/', views.post, name="post"), 
    path('profile/<str:pk>/', views.user_profile, name="profile"),
    path('create-thread/', views.create_thread, name="create-thread"), 
    path('update-thread/<str:thread_pk>', views.update_thread, name="update-thread"), 
    path('create-post/', views.create_post, name="create-post"), 
    path('update-post/<str:post_pk>', views.update_post, name="update-post"), 
    path('delete-post/<str:post_pk>', views.delete_post, name="delete-post"), 
    path('load-more-comments/<str:post_id>/', views.load_more_comments, name='load_more_comments'), 
    path('settings/<str:pk>/', views.settings, name="settings")
]
