from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import Dashboard, OrderDetails, Menu, MenuSearch


urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('order/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:menuitem>/', views.edit_product, name='edit_product'),
    path('delete/<int:menuitem>/', views.delete_product, name='delete_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)