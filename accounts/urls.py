from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup_success/', views.SignUpSuccessView.as_view(), name='signup_success'),
    path('top/', views.TopView.as_view(), name='top'),
    path('user_logout/', views.logout_view, name='user_logout'),
    path('user_profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('userchange/<int:pk>', views.UserChangeView.as_view(), name='user_change'),
    path('user_password_change/', views.UserChangePasswordView.as_view(), name='user_change_password'),
    path('user_password_change_done/', views.UserPasswordChangeDoneView.as_view(), name='user_change_password_done')

]