from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('customer/', include('customer.urls')),
    path('vendor/', include('vendor.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
