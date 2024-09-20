from .carrito import Carrito

def total_carrito(request):
    carrito = Carrito(request)
    total = carrito.obtener_total()  # Obtiene el total del carrito
    return {'total_carrito': total}

    
        