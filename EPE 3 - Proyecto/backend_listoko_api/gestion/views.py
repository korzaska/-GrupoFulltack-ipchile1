import logging
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Q
from .models import ProductoBodega, MovimientoInventario, CategoriaInsumo
from .forms import MovimientoForm, ProductoForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductoSerializer, MovimientoSerializer, CategoriaSerializer

logger = logging.getLogger('gestion')


@staff_member_required(login_url='/admin/login/')
def resumen(request):
    total_productos = ProductoBodega.objects.count()
    total_categorias = CategoriaInsumo.objects.count()
    stock_total = ProductoBodega.objects.aggregate(t=Sum('stock_actual'))['t'] or 0

    resumen_categorias = []
    for cat in CategoriaInsumo.objects.all():
        prods = ProductoBodega.objects.filter(categoria=cat)
        stock = prods.aggregate(t=Sum('stock_actual'))['t'] or 0
        resumen_categorias.append({
            'nombre': cat.nombre,
            'productos': prods.count(),
            'stock': stock,
        })

    ultimos_movimientos = MovimientoInventario.objects.select_related('producto').order_by('-fecha')[:10]

    return render(request, 'gestion/resumen.html', {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'stock_total': stock_total,
        'resumen_categorias': resumen_categorias,
        'ultimos_movimientos': ultimos_movimientos,
    })


@staff_member_required(login_url='/admin/login/')
def productos(request):
    q = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    productos_qs = ProductoBodega.objects.select_related('categoria').order_by('codigo')

    if q:
        productos_qs = productos_qs.filter(
            Q(nombre__icontains=q) | Q(codigo__icontains=q)
        )
    if categoria_id:
        productos_qs = productos_qs.filter(categoria_id=categoria_id)

    categorias = CategoriaInsumo.objects.all()

    return render(request, 'gestion/productos.html', {
        'productos': productos_qs,
        'categorias': categorias,
        'q': q,
        'categoria_id': categoria_id,
    })


@staff_member_required(login_url='/admin/login/')
def producto_nuevo(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'gestion/producto_form.html', {'form': form})


@staff_member_required(login_url='/admin/login/')
def movimientos(request):
    movimientos_qs = MovimientoInventario.objects.select_related('producto').order_by('-fecha')[:50]
    return render(request, 'gestion/movimientos.html', {'movimientos': movimientos_qs})


@staff_member_required(login_url='/admin/login/')
def movimiento_nuevo(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            mov = form.save(commit=False)
            producto = mov.producto
            if mov.tipo == 'ENTRADA':
                producto.stock_actual += mov.cantidad
            else:
                producto.stock_actual = max(0, producto.stock_actual - mov.cantidad)
            producto.save()
            mov.save()
            return redirect('resumen')
    else:
        form = MovimientoForm()
    return render(request, 'gestion/movimiento_form.html', {'form': form})


# ─── API REST ───────────────────────────────────────────────────────────────

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = CategoriaInsumo.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if not request_is_authenticated(self.request):
            logger.warning(f"Acceso no autorizado a CategoriaViewSet desde {self.request.META.get('REMOTE_ADDR')}")
        return super().handle_exception(exc)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = ProductoBodega.objects.all().order_by('codigo')
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if not request_is_authenticated(self.request):
            logger.warning(f"Acceso no autorizado a ProductoViewSet desde {self.request.META.get('REMOTE_ADDR')}")
        return super().handle_exception(exc)


class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all().order_by('-fecha')
    serializer_class = MovimientoSerializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if not request_is_authenticated(self.request):
            logger.warning(f"Acceso no autorizado a MovimientoViewSet desde {self.request.META.get('REMOTE_ADDR')}")
        return super().handle_exception(exc)


def request_is_authenticated(request):
    return request.user and request.user.is_authenticated