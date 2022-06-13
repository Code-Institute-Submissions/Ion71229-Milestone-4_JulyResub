from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import Dashboard, OrderDetails


urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('order/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('add/', views.add_product, name='add_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)