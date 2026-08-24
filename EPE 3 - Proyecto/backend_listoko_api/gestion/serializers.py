from rest_framework import serializers
from .models import ProductoBodega, MovimientoInventario, CategoriaInsumo


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaInsumo
        fields = '__all__'

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre de la categoría no puede estar vacío.")
        if CategoriaInsumo.objects.filter(nombre__iexact=value.strip()).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Ya existe una categoría con ese nombre.")
        return value.strip()


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoBodega
        fields = '__all__'

    def validate_codigo(self, value):
        if not value.strip():
            raise serializers.ValidationError("El código del producto no puede estar vacío.")
        qs = ProductoBodega.objects.filter(codigo__iexact=value.strip())
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un producto con ese código.")
        return value.strip()

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre del producto no puede estar vacío.")
        return value.strip()

    def validate_stock_actual(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value


class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        return value

    def validate(self, data):
        tipo = data.get('tipo')
        cantidad = data.get('cantidad')
        producto = data.get('producto')
        if tipo == 'SALIDA' and producto and cantidad:
            if cantidad > producto.stock_actual:
                raise serializers.ValidationError(
                    f"No hay suficiente stock. Stock actual: {producto.stock_actual}."
                )
        return data
