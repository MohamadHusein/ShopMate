from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib import admin
from ShopMate import settings
from django.views.decorators.cache import cache_page



app_name = 'home'
urlpatterns = [
    path('' , cache_page(60 * 1)(views.Home.as_view()) , name='home'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)