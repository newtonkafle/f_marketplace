from django.urls import path, include
from . import views
from accounts import views as accountViews

urlpatterns = [
    path('profile/', views.profile, name='v_profile'),
    path('', accountViews.vendorDashboard, name='vendor'),
]
