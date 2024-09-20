from pyexpat.errors import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from .models import Asignacion, Producto
from .carrito import Carrito
from .models import CategoriaProducto, CategoriaServicio, Cita, Cliente, Inventario, Producto, Servicio, Solicitud, Usuario, Venta
from .forms import CategoriaProductoForm, CategoriaServicioForm, CitaForm, DetalleVentaForm, InventarioForm, ProductoForm, CustomAuthenticationForm, EmpleadoRegisterForm, \
    ClienteRegisterForm, ServicioForm, SolicitudForm, VentaForm
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from .models import Empleado
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import inlineformset_factory
from .models import Venta, DetalleVenta
from  .import carrito
DetalleVentaFormSet = inlineformset_factory(Venta, DetalleVenta, form=DetalleVentaForm, extra=1)

def inicio(request):
    return render(request, 'paginas/inicio.html')
def nosotros(request):
    return render(request, 'paginas/nosotros.html')
def das (request):
    return render(request, 'dashboard.html')
def productos(request):
    productos = Producto.objects.all()
    return render(request, 'paginas/productos.html', {'productos':productos})
def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect('productos')
def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect('carrito')
def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect('carrito')
from django.shortcuts import redirect

def limpiar_carrito(request):
    # Verificar si el carrito existe en la sesión
    if 'carrito' in request.session:
        # Limpiar el carrito
        request.session['carrito'] = {}
        # Asegurar que la sesión se marque como modificada
        request.session.modified = True
    return redirect('carrito')

def vista_carrito(request):
    carrito = Carrito(request)
    total = carrito.obtener_total()  # Calcular el total del carrito
    return render(request, 'carrito.html', 
                  {'total_carrito': total, 
                   'carrito': carrito.carrito})

#clientes

def cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/vista.html', {'clientes': clientes})

from django.shortcuts import render, redirect
from .forms import ClienteRegisterForm

def crear_cliente_dashboard(request):
    if request.method == 'POST':
        form = ClienteRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')  # Redirigir a la lista de clientes
    else:
        form = ClienteRegisterForm()
    return render(request, 'clientes/crear_cliente_dashboard.html', {'form': form})

def crear_cliente_principal(request):
    if request.method == 'POST':
        form = ClienteRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes')  # Redirigir a la lista de clientes
    else:
        form = ClienteRegisterForm()
    return render(request, 'clientes/crear_cliente_principal.html', {'form': form})



def actualizar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteRegisterForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')
    else:
        form = ClienteRegisterForm(instance=cliente)
    return render(request, 'clientes/actualizar.html', {'form': form, 'cliente': cliente})



class Eliminarcliente(DeleteView):
    model = Cliente
    template_name = "clientes/eliminar.html"
    success_url = reverse_lazy('clientes')



#Crud para empleado
class CrearEmpleado(CreateView):
    model = Empleado
    form_class = EmpleadoRegisterForm
    template_name = "empleado/crear_empleado.html"
    success_url = reverse_lazy('listaEmpleado')

class ActualizarEmpleado(UpdateView):
    model = Empleado
    form_class = EmpleadoRegisterForm
    template_name = "empleados/actualizar_empleado.html"

class ListarEmpelado(ListView):
    model = Empleado
    form_class = EmpleadoRegisterForm
    template_name = "empleados/listar_empleado.html"

class DetalleEmpleado(DetailView):
        model = Empleado
        template_name = "empleados/detalle_empleado.html"

class EliminarEmpleado(DeleteView):
    model = Empleado
    template_name = "empleados/eliminar_empleado.html"
    success_url = reverse_lazy('listaEmpleado')


#Crud para producto
class CrearProducto(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/crear_producto.html"
    success_url = reverse_lazy('listaProducto')

class ActualizarProducto(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/actualizar_producto.html"
    success_url = reverse_lazy('listaProducto')

class ListarProducto(ListView):
    model = Producto
    template_name = "productos/listar_producto.html"

class DetalleProducto(DetailView):
    model = Producto
    template_name = "productos/detalle_producto.html"

class EliminarProducto(DeleteView):
    model = Producto
    template_name = "productos/eliminar_producto.html"
    success_url = reverse_lazy('listaProducto')
    
from django.contrib.auth.decorators import login_required

def dashboard_empleado(request):
    if hasattr(request.user, 'empleado'):  
        citas = Cita.objects.filter(empleado=request.user.empleado)  
        
        return render(request, 'dashboard_empleado.html', {'citas': citas})
    else:
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('inicio')


from django.views.decorators.cache import never_cache

@never_cache
def logoutView (request):
    logout(request)
    return redirect('inicio')


def register_cliente(request):
    if request.method == 'POST':
        form = ClienteRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('login') 
    else:
        form = ClienteRegisterForm()
    return render(request, 'registration/register_cliente.html', {'form': form})

def register_empleado(request):
    if request.method == 'POST':
        form = EmpleadoRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('listaEmpleado')  
    else:
        form = EmpleadoRegisterForm()
    return render(request, 'registration/register_empleado.html', {'form': form})

class ListarUsuario(ListView):
    model = Usuario
    template_name = 'usuarios/listar_usuario.html'
    context_object_name = 'usuarios' 


class EliminarUsuario(DeleteView):
    model = Usuario
    template_name = "usuarios/eliminar_usuario.html"
    success_url = reverse_lazy('listaUsuario')
    

#crud solicitud
class CrearSolicitud(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = "Solicitudes/crear_solicitud.html"
    success_url = reverse_lazy('inicio')
    success_message = "Categoría de servicio creada con éxito."
    
class CrearSolicitudDesdeDashboard(CrearSolicitud):
    template_name = "Solicitudes/crear_solicitud_dashboard.html"  

class CrearSolicitudDesdePrincipal(CrearSolicitud):
    template_name = "Solicitudes/crear_solicitud_principal.html" 

    def form_valid(self, form):
        return super().form_valid(form)
   
class ActualizarSolicitud(UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = "solicitudes/actualizar_solicitud.html"
    success_url = reverse_lazy('listasolicitud')

class ListarSolicitud(ListView):
    model = Solicitud
    template_name = "solicitudes/listar_solicitud.html"

class DetalleSolicitud(DetailView):
    model = Solicitud
    template_name = "solicitudes/detalle_solicitud.html"

class EliminarSolicitud(DeleteView):
    model = Solicitud
    template_name = "solicitudes/eliminar_solicitud.html"
    success_url = reverse_lazy('listasolicitud')
  
#Crud para Servicio  
class CrearServicio(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = "servicios/crear_servicio.html"
    success_url = reverse_lazy('listaservicio')
    success_message = "Categoría de servicio creada con éxito."
    def form_valid(self, form):
        return super().form_valid(form)
   
class ActualizarServicio(UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = "servicios/actualizar_servicio.html"
    success_url = reverse_lazy('listaservicio')

class ListarServicio(ListView):
    model = Servicio
    template_name = "servicios/listar_servicio.html"

class DetalleServicio(DetailView):
    model = Servicio
    template_name = "servicios/detalle_servicio.html"

class EliminarServicio(DeleteView):
    model = Servicio
    template_name = "servicios/eliminar_servicio.html"
    success_url = reverse_lazy('listaservicio')
    
#categoriaservicio
class CrearCategoriaServicio(SuccessMessageMixin, CreateView):
    model = CategoriaServicio
    form_class = CategoriaServicioForm
    template_name = "categoria_servicios/crear_categoriaservicio.html"
    context_object_name = 'categoria'
    success_url = reverse_lazy('listacategoriaservicio')
    success_message = "Categoría de servicio creada con éxito."

    def form_valid(self, form):
        return super().form_valid(form)

class ActualizarCategoriaServicio(UpdateView):
    model = CategoriaServicio
    form_class = CategoriaServicioForm
    template_name = "categoria_servicios/actualizar_categoriaservicio.html"
    success_url = reverse_lazy('listacategoriaservicio')

class ListarCategoriaServicio(ListView):
    model = CategoriaServicio
    template_name = "categoria_servicios/listar_categoriaservicio.html"
    
class DetalleCategoriaServicio(DetailView):
    model = CategoriaServicio
    template_name = "categoria_servicios/detalle_categoriaservicio.html"

class EliminarCategoriaServicio(DeleteView):
    model = CategoriaServicio
    template_name = "categoria_servicios/eliminar_categoriaservicio.html"
    success_url = reverse_lazy('listacategoriaservicio')
    
#categoriaproducto
class CrearCategoriaProducto(SuccessMessageMixin, CreateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = "categoria_productos/crear_categoriaproducto.html"
    context_object_name = 'producto'
    success_url = reverse_lazy('listacategoriaproducto')
    success_message = "Categoría de producto creada con éxito."

    def form_valid(self, form):
        return super().form_valid(form)

class ActualizarCategoriaProducto(UpdateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = "categoria_productos/actualizar_categoriaproducto.html"
    success_url = reverse_lazy('listacategoriaproducto')

class ListarCategoriaProducto(ListView):
    model = CategoriaProducto
    template_name = "categoria_productos/listar_categoriaproducto.html"
    
class DetalleCategoriaProducto(DetailView):
    model = CategoriaProducto
    template_name = "categoria_productos/detalle_categoriaproducto.html"

class EliminarCategoriaProducto(DeleteView):
    model = CategoriaProducto
    template_name = "categoria_productos/eliminar_categoriaproducto.html"
    success_url = reverse_lazy('listacategoriaproducto')

#INVENTARIO 

class CrearInventario(SuccessMessageMixin, CreateView):
    model = Inventario
    template_name = "inventarios/crear_inventario.html"
    form_class = InventarioForm
    success_url = reverse_lazy('listainventario')
    success_message = "Inventario creado con exito."

    def form_valid(self, form):
        return super().form_valid(form)
    
class ActualizarInventario(UpdateView):
    model = Inventario
    template_name = "inventarios/actualizar_inventario.html"
    form_class = InventarioForm
    success_url = reverse_lazy('listainventario')
    
class ListarInventario(ListView):
    model = Inventario
    template_name = "inventarios/listar_inventario.html"
    
class DetalleInventario(DetailView):    
    model = Inventario
    template_name = "inventarios/detalle_inventario.html"  

class EliminarInventario(DeleteView):   
    model = Inventario
    template_name = "inventarios/eliminar_inventario.html"
    success_url = reverse_lazy('listainventario')
    
#Cita

class CrearCita(SuccessMessageMixin, CreateView):
    model = Cita
    template_name = "citas/crear_cita.html"
    form_class = CitaForm
    success_url = reverse_lazy('listacita')
    success_message = "Cita creada con exito."
    

    def form_valid(self, form):
        return super().form_valid(form)

class CrearCitaDesdeDashboard(CrearCita):
    template_name = "citas/crear_cita_dashboard.html"  

class CrearCitaDesdePrincipal(CrearCita):
    template_name = "citas/crear_cita_principal.html" 

    
class ActualizarCita(UpdateView):   
    model = Cita
    template_name = "citas/actualizar_cita.html"
    form_class = CitaForm
    success_url = reverse_lazy('listacita')
    
class ListarCita(ListView): 
    model = Cita
    template_name = "citas/listar_cita.html"
    context_object_name = 'citas'
    
class DetalleCita(DetailView):
    model = Cita
    template_name = "citas/detalle_cita.html"
    
class EliminarCita(DeleteView):
    model = Cita
    template_name = "citas/eliminar_cita.html"
    success_url = reverse_lazy('listacita')
    
#venta

class CrearVenta(CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'ventas/crear_venta.html'
    success_url = reverse_lazy('listaventa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['detalle_venta_formset'] = DetalleVentaFormSet(self.request.POST)
        else:
            context['detalle_venta_formset'] = DetalleVentaFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_venta_formset = context['detalle_venta_formset']

        if form.is_valid() and detalle_venta_formset.is_valid():
            # Guardar la venta
            venta = form.save()

            # Asignar la venta a cada detalle y guardar los detalles
            detalle_venta_formset.instance = venta
            detalle_venta_formset.save()

            return redirect(self.success_url)
        else:
            return self.form_invalid(form)
    
class ActualizarVenta(UpdateView):
    model = Venta
    template_name = "ventas/actualizar_venta.html"
    form_class = VentaForm
    success_url = reverse_lazy('listaventa')
    
class ListarVenta(ListView):
    model = Venta
    template_name = "ventas/listar_venta.html"
    context_object_name = 'ventas'
    
class DetalleVenta(DetailView):
    model = Venta
    template_name = "ventas/detalle_venta.html"
    
class EliminarVenta(DeleteView):
    model = Venta
    template_name = "ventas/eliminar_venta.html"
    success_url = reverse_lazy('listaventa')

class CarritoView(View):
    def get(self, request, *args, **kwargs):
        carrito = Carrito(request)
        contexto = {'carrito': carrito}
        return render(request, 'carrito.html', contexto)

def checkout(request):
    carrito = Carrito(request)
    if request.user.is_authenticated:
        try:
            cliente = Cliente.objects.get(id=request.user.id)
        except Cliente.DoesNotExist:
            return redirect('login')
    else:
        return redirect('login')
    total = carrito.obtener_total()   
    return render(request, 'checkout.html', {
        'cliente': cliente,
        'total_carrito': total, 
        'carrito': carrito.carrito,  
    })
    
def cancelar_compra(request):   
        request.session['carrito'] = {}   
        return redirect('inicio') 
    
def reportesview(request):
    return render(request, 'paginas/reportes.html')

import csv
from django.http import HttpResponse
from .models import Cliente

def generar_reporte_clientes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=clientes_report.csv'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Apellido', 'Email', 'Nº Documento', 'Teléfono', 'Dirección'])
    clientes = Cliente.objects.all()
    for cliente in clientes:
        writer.writerow([
            cliente.first_name, 
            cliente.last_name,   
            cliente.email,       
            cliente.n_documento,
            cliente.telefono,
            cliente.direccion or 'N/A' 
        ])

    return response

def generar_reporte_productos(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Código de Barras', 'Nombre', 'Descripción', 'Precio Compra', 'Precio Venta', 'Stock', 'Fecha Creación'])
    productos = Producto.objects.all()
    for producto in productos:
        writer.writerow([producto.codigo_barras, producto.nombre, producto.descripcion, producto.precio_compra, producto.precio_venta, producto.stock, producto.fecha_creacion])
    return response

def generar_reporte_citas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_citas.csv"'
    writer = csv.writer(response)
    writer.writerow(['Fecha y Hora', 'Cliente', 'Servicio', 'Empleado', 'Estado de la Cita', 'Estado', 'Fecha Creación'])
    citas = Cita.objects.all()
    for cita in citas:
        writer.writerow([cita.fecha_hora, cita.cliente, cita.servicio, cita.empleado, cita.estado_cita, cita.estado, cita.fecha_creacion])
    return response

def crear_asignacion(request):
    if request.method == 'POST':
        servicio_id = request.POST.get('servicio')
        empleado_id = request.POST.get('empleado')
        
        if Asignacion.objects.filter(servicio_id=servicio_id, empleado_id=empleado_id).exists():
            error_message = "La asignación ya existe."
            return render(request, 'asignaciones/crear_asignacion.html', {'servicios': Servicio.objects.all(), 'empleados': Empleado.objects.all(), 'error_message': error_message})

        try:
            Asignacion.objects.create(servicio_id=servicio_id, empleado_id=empleado_id)
            return redirect('lista_asignacion') 
        except IntegrityError:
            error_message = "Error al guardar la asignación."
            return render(request, 'crear_asignacion.html', {'servicios': Servicio.objects.all(), 'empleados': Empleado.objects.all(), 'error_message': error_message})

    return render(request, 'asignaciones/crear_asignacion.html', {'servicios': Servicio.objects.all(), 'empleados': Empleado.objects.all()})

def lista_asignacion(request):
    asignaciones = Asignacion.objects.all()
    return render(request, 'asignaciones/lista_asignacion.html', {'asignaciones': asignaciones})

def actualizar_asignacion(request, asignacion_id):
    asignacion = Asignacion.objects.get(id=asignacion_id)

    if request.method == 'POST':
        servicio_id = request.POST.get('servicio')
        empleado_id = request.POST.get('empleado')
        
        asignacion.servicio_id = servicio_id
        asignacion.empleado_id = empleado_id
        asignacion.save()
        
        return redirect('lista_asignacion')

    return render(request, 'asignaciones/actualizar_asignacion.html', {'asignacion': asignacion, 'servicios': Servicio.objects.all(), 'empleados': Empleado.objects.all()})

def eliminar_asignacion(request, asignacion_id):
    asignacion = Asignacion.objects.get(id=asignacion_id)
    asignacion.delete()
    return redirect('lista_asignacion')
