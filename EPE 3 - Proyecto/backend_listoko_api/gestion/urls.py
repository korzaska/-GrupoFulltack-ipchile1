from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/productos', views.ProductoViewSet)
router.register(r'api/movimientos', views.MovimientoViewSet)
router.register(r'api/categorias', views.CategoriaViewSet)

urlpatterns = [
    path('', views.resumen, name='resumen'),
    path('productos/', views.productos, name='productos'),
    path('productos/nuevo/', views.producto_nuevo, name='producto_nuevo'),
    path('movimientos/', views.movimientos, name='movimientos'),
    path('movimientos/nuevo/', views.movimiento_nuevo, name='movimiento_nuevo'),
    path('', include(router.urls)),
]
