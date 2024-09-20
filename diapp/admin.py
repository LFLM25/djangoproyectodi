from django.contrib import admin

from .models import Cliente, Empleado, Producto, CategoriaProducto, CategoriaServicio, Usuario

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Producto)
admin.site.register(CategoriaProducto)
admin.site.register(CategoriaServicio)