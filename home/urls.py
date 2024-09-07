from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib import admin
from ShopMate import settings




app_name = 'home'
urlpatterns = [
    path('' , views.Home.as_view() , name='home'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)