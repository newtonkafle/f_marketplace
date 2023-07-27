from django.urls import path, include
from . import views
from accounts import views as accountViews

urlpatterns = [
    path('profile/', views.profile, name='v_profile'),
    path('', accountViews.vendorDashboard, name='vendor'),

    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/',
         views.productsByCategory, name="products_by_category"),

    # url for the category
    path('menu-builder/category/add/', views.addCategory, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/',
         views.editCategory, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/',
         views.deleteCategory, name='delete_category'),

    # url for the food items]
    path('menu-builder/products/add_product/',
         views.addProduct, name='add_product'),
    path('menu-builder/products/edit_product/<int:product_id>/',
         views.editProduct, name='edit_product'),
    path('menu-builder/products/delete_product/<int:product_id>/',
         views.deleteProduct, name='delete_product'),

]
