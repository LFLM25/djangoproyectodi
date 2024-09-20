from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class Usuario(AbstractUser):
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
    )
        
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',
        blank=True,
    )

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categoria_producto'

    def __str__(self):
        return self.nombre


class CategoriaServicio(models.Model):
    nombre = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categoria_servicio'

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    duracion = models.DurationField(help_text="Duración del servicio (HH:MM:SS)")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(CategoriaServicio, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'servicios'

    def __str__(self):
        return self.nombre


class Cliente(Usuario):
    n_documento = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'clientes'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Empleado(Usuario):
    n_documento = models.CharField(max_length=50, unique=True)
    cargo = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_contratacion = models.DateTimeField(default=timezone.now)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'empleados'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Cita(models.Model):
    fecha_hora = models.DateTimeField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    estado_cita = models.CharField(max_length=20, choices=[('Agendada', 'Agendada'), ('Completada', 'Completada'), ('Cancelada', 'Cancelada')], default='Agendada')
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'citas'

    def __str__(self):
        return f'Cita de {self.cliente} para {self.servicio} el {self.fecha_hora}'

class Producto(models.Model):
    codigo_barras = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    lleva_impuesto = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    stock_min = models.PositiveIntegerField(default=1)
    stock = models.PositiveIntegerField()
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)

    class Meta:
        db_table = 'productos'

    def __str__(self):
        return '{self.nombre}{self.precio_venta}'


class Inventario(models.Model): 
    nombre = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,  null=True, blank=True)

    class Meta:
        db_table = 'inventarios'

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    n_documento = models.CharField(max_length=50, unique=True)
    razon_social = models.CharField(max_length=100)
    representante = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    correo_electronico = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=20)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'proveedores'

    def __str__(self):
        return self.razon_social


class Compra(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'compras'

    def __str__(self):
        return f'Compra #{self.id}'


class DetalleCompra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()

    class Meta:
        db_table = 'detalle_compras'


class Venta(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ventas'

    def __str__(self):
        return f'Venta #{self.id}'


class DetalleVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()

    class Meta:
        db_table = 'detalle_ventas'





class Asignacion(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    class Meta:
        db_table = 'asignaciones'
        unique_together = ('servicio', 'empleado')

    def __str__(self):
        return f'{self.empleado} - {self.servicio}'


class Solicitud(models.Model):
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'solicitudes'

