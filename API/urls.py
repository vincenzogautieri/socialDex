"""API app URL configuration."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('json/', views.posts, name='json_post'),
    path('last-hour-posts', views.last_hour_posts, name='last_hour_posts'),
    path('search', views.search, name='search'),
    path('new-post', views.new_post, name='new_post'),
    path('count', views.count_post, name='count'),
    path('user<int:id>/', views.user_id, name='user_id'),
]
