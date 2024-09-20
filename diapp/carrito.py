class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito = carrito
    def contar_productos(self):
        total_productos = sum(item['cantidad'] for item in self.carrito.values())
        return total_productos
    def agregar(self, producto):
        producto_id = str(producto.id)
        if str(producto_id) not in self.carrito.keys():
            self.carrito[producto_id] = {
                "producto_id": producto_id,
                'nombre': producto.nombre,
                'precio_venta': float(producto.precio_venta),
                'cantidad': 1,
                'imagen': producto.imagen.url if producto.imagen else None,
                "total_producto": float(producto.precio_venta) 
            }
        else:
            self.carrito[producto_id]["cantidad"] += 1
            self.carrito[producto_id]["total_producto"] = (
                self.carrito[producto_id]['cantidad'] * self.carrito[producto_id]['precio_venta']
            )

        self.guardar_carrito()  
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
                
    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar_carrito()

    def restar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            self.carrito[producto_id]["cantidad"] -= 1
            if self.carrito[producto_id]["cantidad"] <= 0:
                self.eliminar(producto)
            else:
                self.carrito[producto_id]["total_producto"] = self.carrito[producto_id]["cantidad"] * float(producto.precio_venta)
                self.guardar_carrito()
        
    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
    
    def obtener_total(self):
        total = 0
        for item in self.carrito.values():
            total += item["total_producto"]
        return total
    