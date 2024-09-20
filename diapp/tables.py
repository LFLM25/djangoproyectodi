import django_tables2 as tables
from .models import Cliente, Empleado, Producto

class ClienteTable(tables.Table):
    class Meta:
        model = Cliente
        template_name = 'django_tables2/bootstrap.html'
        fields = ('nombre', 'apellido', 'telefono', 'direccion', 'correo_electronico', 'estado', 'fecha_creacion')

class EmpleadoTable(tables.Table):
    class Meta:
        model = Empleado
        template_name = 'django_tables2/bootstrap.html'
        fields = ('nombre', 'apellido', 'telefono', 'direccion', 'correo_electronico', 'estado', 'fecha_creacion')

class ProductoTable(tables.Table):
    class Meta:
        model = Producto
        template_name = 'django_tables2/bootstrap.html'
        fields = ('nombre', 'descripcion', 'precio', 'stock', 'categoria')
