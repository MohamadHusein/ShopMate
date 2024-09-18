from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login' , views.UserLogin.as_view(), name='user_login'),
    path('otplogin' , views.OtpLoginView.as_view(), name='user_otp_login'),
    path('checkotp' , views.CheckOtpView.as_view(), name='check_otp'),
    path('add/address' , views.AddAddressView.as_view(), name='add_address'),
    path('logout' , views.user_logout, name='user_logout'),
]