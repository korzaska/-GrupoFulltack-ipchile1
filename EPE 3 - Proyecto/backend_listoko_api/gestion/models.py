from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MinLengthValidator


class CategoriaInsumo(models.Model):
    nombre = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


class ProductoBodega(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    stock_actual = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    categoria = models.ForeignKey(CategoriaInsumo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [('ENTRADA', 'Entrada'), ('SALIDA', 'Salida')]
    producto = models.ForeignKey(ProductoBodega, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    responsable = models.CharField(max_length=100, blank=True, default='')
    observacion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-fecha']


class Solicitud(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Solicitud'
        verbose_name_plural = 'Solicitudes'
