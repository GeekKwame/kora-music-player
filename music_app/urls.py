from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    path('search/', views.search, name='search'),
    path('artist/<str:artist_id>/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('update-avatar/', views.update_avatar, name='update_avatar'),
]
