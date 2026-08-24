from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import CategoriaInsumo, ProductoBodega, MovimientoInventario


class ProductoAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('testadmin', '', 'testpass')
        self.client.force_authenticate(user=self.user)
        self.categoria = CategoriaInsumo.objects.create(nombre='Materiales de aseo')
        self.producto = ProductoBodega.objects.create(
            codigo='ASE-001',
            nombre='Alcohol gel 1 litro',
            stock_actual=10,
            categoria=self.categoria
        )

    def test_listar_productos(self):
        response = self.client.get('/api/productos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_producto(self):
        data = {
            'codigo': 'ASE-999',
            'nombre': 'Producto de prueba',
            'stock_actual': 5,
            'categoria': self.categoria.id
        }
        response = self.client.post('/api/productos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtener_producto(self):
        response = self.client.get(f'/api/productos/{self.producto.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Alcohol gel 1 litro')

    def test_eliminar_producto(self):
        response = self.client.delete(f'/api/productos/{self.producto.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MovimientoAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('testadmin2', '', 'testpass')
        self.client.force_authenticate(user=self.user)
        self.categoria = CategoriaInsumo.objects.create(nombre='Materiales de aseo')
        self.producto = ProductoBodega.objects.create(
            codigo='ASE-001',
            nombre='Alcohol gel 1 litro',
            stock_actual=10,
            categoria=self.categoria
        )

    def test_listar_movimientos(self):
        response = self.client.get('/api/movimientos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_movimiento(self):
        data = {
            'producto': self.producto.id,
            'tipo': 'ENTRADA',
            'cantidad': 5,
            'responsable': 'Test',
            'observacion': ''
        }
        response = self.client.post('/api/movimientos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CategoriaAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('testadmin3', '', 'testpass')
        self.client.force_authenticate(user=self.user)

    def test_listar_categorias(self):
        response = self.client.get('/api/categorias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_categoria(self):
        data = {'nombre': 'Nueva categoria', 'descripcion': ''}
        response = self.client.post('/api/categorias/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
