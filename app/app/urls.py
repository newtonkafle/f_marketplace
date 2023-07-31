from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from core import views
# from marketplace import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('accounts/', include('accounts.urls')),
    path('vendor/', include('vendor.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('search/', views.search, name='search'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
