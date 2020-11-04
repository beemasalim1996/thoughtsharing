
from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('signup/', views.signup, name="sign_up"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard_view/', views.dashboard_view, name="dashboard_view"),
    path('profile/', views.profile, name="profile"),
    path('thoughts_view/', views.thoughts_view, name="thoughts_view"),
    path('thoughts_add/', views.thoughts_add, name="thoughts_add"),
]