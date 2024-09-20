from django.urls import path
from . import carrito
from . import views
from .views import ActualizarCategoriaProducto, ActualizarCategoriaServicio, ActualizarCita, ActualizarEmpleado, ActualizarInventario, ActualizarServicio, ActualizarSolicitud, ActualizarVenta, CrearCategoriaProducto,\
    CrearCategoriaServicio, CrearCita, CrearCitaDesdeDashboard, CrearCitaDesdePrincipal, CrearEmpleado, CrearInventario, CrearServicio, CrearSolicitud, CrearSolicitudDesdeDashboard, CrearSolicitudDesdePrincipal, CrearVenta, DetalleCategoriaProducto, DetalleCategoriaServicio, DetalleCita,DetalleEmpleado, DetalleInventario,\
    DetalleServicio, DetalleSolicitud, DetalleVenta, EliminarCategoriaProducto, EliminarCategoriaServicio, EliminarCita, EliminarInventario, EliminarServicio, EliminarSolicitud, EliminarVenta, ListarCategoriaProducto,\
    ListarCategoriaServicio, ListarCita, ListarEmpelado, Eliminarcliente, \
    EliminarEmpleado, CrearProducto, ActualizarProducto, ListarInventario, ListarProducto, DetalleProducto, EliminarProducto, \
    CustomLoginView, ListarServicio, ListarSolicitud, ListarVenta, actualizar_asignacion, crear_asignacion, crear_cliente_dashboard, crear_cliente_principal, eliminar_asignacion, generar_reporte_clientes,\
    register_cliente, register_empleado, logoutView,ListarUsuario,EliminarUsuario

urlpatterns = [
    path('', views.inicio, name='root'),
    path('inicio/', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('dash/', views.das, name='dash'),
    path('carrito/', views.CarritoView.as_view(), name='carrito'),
    
    path('asignaciones/', views.crear_asignacion, name='crear_asignacion'),
    path('asignaciones/lista', views.lista_asignacion, name='lista_asignacion'),
    path('asignacion/actualizar/<int:asignacion_id>/', views.actualizar_asignacion, name='actualizar_asignacion'),
    path('asignacion/eliminar/<int:asignacion_id>/', views.eliminar_asignacion, name='eliminar_asignacion'),
    
    path('reportes/', views.reportesview, name='reportes'),
    path('reporte/clientes/', generar_reporte_clientes, name='reporte_clientes'),
    path('reporte/productos/', views.generar_reporte_productos, name='reporte_productos'),
    path('reporte/citas/', views.generar_reporte_citas, name='reporte_citas'),
    
    path('productos/', views.productos, name='productos'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('restar/<int:producto_id>/', views.restar_producto, name='restar_producto'),
    path('limpiar/', views.limpiar_carrito, name='limpiar_productos'),
    path('checkout/', views.checkout, name='checkout'),
    path('cancelar/', views.cancelar_compra, name='cancelar_compra'),

    path('clientes/vista/', views.cliente, name='clientes'),
    path('clientes/actualizar/<int:pk>/', views.actualizar, name='actualizar'),
    path('clientes/eliminar/<int:pk>/', Eliminarcliente.as_view(), name='eliminar'),
    path('crear_cliente_dashboard/', crear_cliente_dashboard, name='crear_cliente_dashboard'),
    path('crear_cliente_principal/', crear_cliente_principal, name='crear_cliente_principal'),

    path('empleado/crear', CrearEmpleado.as_view(), name='crearEmpleado'),
    path('empleado/actualizar/<int:pk>/', ActualizarEmpleado.as_view(), name='actualizarEmpleado'),
    path('empleado/detalle/<int:pk>', DetalleEmpleado.as_view(), name='detalleEmpleado'),
    path('empleado/lista', ListarEmpelado.as_view(), name='listaEmpleado'),
    path('empleado/eliminar/<int:pk>/', EliminarEmpleado.as_view(), name='eliminarEmpleado'),

    path('producto/crear', CrearProducto.as_view(), name='crearproducto'),
    path('producto/actualizar/<int:pk>/', ActualizarProducto.as_view(), name='actualizarproducto'),
    path('producto/detalle/<int:pk>', DetalleProducto.as_view(), name='detalleproducto'),
    path('producto/lista', ListarProducto.as_view(), name='listaProducto'),
    path('producto/eliminar/<int:pk>/', EliminarProducto.as_view(), name='eliminarproducto'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logoutView, name="logout"),
    path('register/cliente/', register_cliente, name='register_cliente'),
    path('register/empleado/', register_empleado, name='register_empleado'),
    path('registarme/', register_cliente, name='registrarme'),

    path('usuario/lista', ListarUsuario.as_view(), name='listaUsuario'),
    path('usuario/eliminar/<int:pk>/', EliminarUsuario.as_view(), name='eliminarUsuario'),
    path('dashboard/empleado/', views.dashboard_empleado, name='dashboard_empleado'),

    path('crear_solicitud_dashboard/', CrearSolicitudDesdeDashboard.as_view(), name='crear_solicitud_dashboard'),
    path('crear_solicitud_principal/', CrearSolicitudDesdePrincipal.as_view(), name='crear_solicitud_principal'),
    path('solicitudes/actualizar/<int:pk>/', ActualizarSolicitud.as_view(), name='actualizarsolicitud'),
    path('solicitudes/detalle/<int:pk>', DetalleSolicitud.as_view(), name='detallesolicitud'),
    path('solicitudes/lista', ListarSolicitud.as_view(), name='listasolicitud'),
    path('solicitudes/eliminar/<int:pk>/', EliminarSolicitud.as_view(), name='eliminarsolicitud'),

    path('servicios/crear/', CrearServicio.as_view(), name='crearservicio'),
    path('servicios/actualizar/<int:pk>/', ActualizarServicio.as_view(), name='actualizarservicio'),
    path('servicios/detalle/<int:pk>', DetalleServicio.as_view(), name='detalleservicio'),
    path('servicios/lista', ListarServicio.as_view(), name='listaservicio'),
    path('servicios/eliminar/<int:pk>/', EliminarServicio.as_view(), name='eliminarservicio'),

    path('categoriasproductos/crear/', CrearCategoriaProducto.as_view(), name='crearcategoriaproducto'),
    path('categoriasproductos/actualizar/<int:pk>/', ActualizarCategoriaProducto.as_view(), name='actualizarcategoriaproducto'),
    path('categoriasproductos/detalle/<int:pk>', DetalleCategoriaProducto.as_view(), name='detallecategoriaproducto'),
    path('categoriasproductos/lista', ListarCategoriaProducto.as_view(), name='listacategoriaproducto'),
    path('categoriasproductos/eliminar/<int:pk>/', EliminarCategoriaProducto.as_view(), name='eliminarcategoriaproducto'),

    path('categoriasservicios/crear/', CrearCategoriaServicio.as_view(), name='crearcategoriaservicio'),
    path('categoriasservicios/actualizar/<int:pk>/', ActualizarCategoriaServicio.as_view(), name='actualizarcategoriaservicio'),
    path('categoriasservicios/detalle/<int:pk>', DetalleCategoriaServicio.as_view(), name='detallecategoriaservicio'),
    path('categoriasservicios/lista', ListarCategoriaServicio.as_view(), name='listacategoriaservicio'),
    path('categoriasservicios/eliminar/<int:pk>/', EliminarCategoriaServicio.as_view(), name='eliminarcategoriaservicio'),
    
    path('inventarios/eliminar/<int:pk>/', EliminarInventario.as_view(), name='eliminarinventario'),
    path('inventarios/detalle/<int:pk>', DetalleInventario.as_view(), name='detalleinventario'),
    path('inventarios/crear/', CrearInventario.as_view(), name='crearinventario'),
    path('inventarios/actualizar/<int:pk>/', ActualizarInventario.as_view(), name='actualizarinventario'),
    path('inventarios/lista', ListarInventario.as_view(), name='listainventario'),

    path('citas/crear', CrearCita.as_view(), name='crearcita'),
    path('citas/eliminar/<int:pk>/', EliminarCita.as_view(), name='eliminarcita'),
    path('citas/actualizar/<int:pk>/', ActualizarCita.as_view(), name='actualizarcita'),
    path('citas/detalle/<int:pk>', DetalleCita.as_view(), name='detallecita'),
    path('citas/lista', ListarCita.as_view(), name='listacita'),
    path('crear-cita/dashboard/', CrearCitaDesdeDashboard.as_view(), name='crear_cita_dashboard'),
    path('crear-cita/principal/', CrearCitaDesdePrincipal.as_view(), name='crear_cita_principal'),

    path('ventas/crear', CrearVenta.as_view(), name='crearventa'),
    path('ventas/eliminar/<int:pk>/', EliminarVenta.as_view(), name='eliminarventa'),
    path('ventas/actualizar/<int:pk>/', ActualizarVenta.as_view(), name='actualizarventa'),
    path('ventas/detalle/<int:pk>', DetalleVenta.as_view(), name='detalleventa'),
    path('ventas/lista', ListarVenta.as_view(), name='listaventa'),
]   
