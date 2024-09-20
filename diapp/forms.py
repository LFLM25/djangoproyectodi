from django import forms
from django.contrib.auth.models import Group

from .models import Asignacion, CategoriaProducto, CategoriaServicio, Cita, Cliente, DetalleVenta, Inventario, Producto, Servicio, Solicitud, Usuario, Venta
from .models import Empleado
from django.contrib.auth.forms import AuthenticationForm


class ClienteRegisterForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['username', 'password', 'n_documento', 'first_name', 'last_name', 'telefono', 'direccion', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }

class EmpleadoRegisterForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['username', 'password', 'n_documento', 'first_name', 'last_name', 'cargo', 'salario', 'fecha_contratacion', 'email', 'telefono', 'direccion']
        widgets = {
            'password': forms.PasswordInput(),
            'fecha_creacion': forms.HiddenInput(), 
            'fecha_contratacion': forms.DateInput(attrs={'type': 'date'}),
            'salario': forms.NumberInput(attrs={'step': '0.01'}),
        }
        

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', max_length=254)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'fecha_creacion': forms.HiddenInput(), 
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = '__all__' 
        widgets = {
            'fecha_creacion': forms.HiddenInput(), 
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }
        

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'
        widgets = {
            'fecha_creacion': forms.HiddenInput(),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }

class CategoriaServicioForm(forms.ModelForm):
    class Meta:
        model = CategoriaServicio
        fields = '__all__'
        widgets = {
            'fecha_creacion': forms.HiddenInput(), 
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }
        
class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = '__all__'
        widgets = {
            'fecha_creacion': forms.HiddenInput(), 
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }
        
class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = '__all__'
        widgets = {
            'fecha_creacion': forms.HiddenInput(), 
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }
        
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'fecha_creacion': forms.HiddenInput(), 
            'fecha_hora': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # Selector de fecha y hora
            }),
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }
        
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'
        widgets = {
             'fecha_creacion': forms.HiddenInput(), 
            'estado': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = '__all__'
        widgets = {
        }
  
class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = '__all__'
        widgets = {
        }      
