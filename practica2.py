import json
import os

class Proveedor:
    def __init__(self, id: str, nombre: str, ruc: str, direccion: str, telefono: str, correo: str, activo=True):
        self.id: str = id
        self.nombre: str = nombre
        self.ruc: str = ruc
        self.direccion: str = direccion
        self.telefono: str = telefono
        self.correo: str = correo
        self.activo: bool = activo

    def to_dict(self):
        return self.__dict__

class Crudproveedor:

    def __init__(self, archivo="proveedores.json"):
        self.archivo = archivo
        self.proveedores = self.cargar_proveedores()

    def cargar_proveedores(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as file:
                return [Proveedor(**data) for data in json.load(file)]
        return []
    
    def guardar_proveedores(self):
        with open(self.archivo, "w") as file:
            json.dump([proveedor.to_dict() for proveedor in self.proveedores], file, indent=4)
    
    def agregar_proveedor(self, proveedor: Proveedor):
        self.proveedores.append(proveedor)
        self.guardar_proveedores()

    def eliminar_proveedor(self, id: str):
        self.proveedores = [proveedor for proveedor in self.proveedores if proveedor.id != id]
        self.guardar_proveedores()

class Producto:
    def __init__(self, id: str, nombre: str, descripcion: str, precio_unitario: float, stock_actual=0, activo=True):
        self.id: str = id
        self.nombre: str = nombre
        self.descripcion: str = descripcion
        self.precio_unitario: float = precio_unitario
        self.stock_actual: int = stock_actual
        self.activo: bool = activo

    def to_dict(self):
        return self.__dict__

class Crudproducto:
    def __init__(self, archivo="productos.json"):
        self.archivo = archivo
        self.productos = self.cargar_productos()
    
    def cargar_productos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as file:
                return [Producto(**data) for data in json.load(file)]
        return []
    
    def guardar_productos(self):
        with open(self.archivo, "w") as file:
            json.dump([producto.to_dict() for producto in self.productos], file, indent=4)
        
    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)
        self.guardar_productos()

    def eliminar_producto(self, id: str):
        self.productos = [producto for producto in self.productos if producto.id != id]
        self.guardar_productos()  

class CabeceraCompra:
    def __init__(self, id: str, proveedor: Proveedor, fecha_compra: str, numero_factura: str):
        self.id: str = id
        self.proveedor: Proveedor = proveedor
        self.fecha_compra: str = fecha_compra
        self.numero_factura: str = numero_factura
        self.detalles = []
        self.subtotal: float = 0
        self.iva: float = 0
        self.total: float = 0

class DetalleCompra:
    def __init__(self, id: str, producto: Producto, cantidad: int, precio_unitario: float):
        self.id: str = id
        self.producto: Producto = producto
        self.cantidad: int = cantidad
        self.precio_unitario: float = precio_unitario

class MENU:
    def __init__(self):
        self.crud_proveedor = Crudproveedor()
        self.crud_producto = Crudproducto()  # Inicialización de Crudproducto
        self.proveedor = None
        self.producto = None
        self.cabecera_compra = None
        self.detalle_compra = None

    def menu_principal(self):
        while True:
            print("1. Proveedores")
            print("2. Productos")
            print("3. Compras")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.menu_proveedores()
            elif opcion == "2":
                self.menu_productos()
            elif opcion == "3":
                self.menu_compras()
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_proveedores(self):
        while True:
            print("\n--- Menú Proveedores ---")
            print("1. Agregar Proveedor")
            print("2. Eliminar Proveedor")
            print("3. Listar Proveedores")
            print("4. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                id = input("ID: ")
                nombre = input("Nombre: ")
                ruc = input("RUC: ")
                direccion = input("Dirección: ")
                telefono = input("Teléfono: ")
                correo = input("Correo: ")
                proveedor = Proveedor(id, nombre, ruc, direccion, telefono, correo)
                self.crud_proveedor.agregar_proveedor(proveedor)
                print("Proveedor agregado exitosamente.")
            elif opcion == "2":
                id = input("ID del proveedor a eliminar: ")
                self.crud_proveedor.eliminar_proveedor(id)
                print("Proveedor eliminado exitosamente.")
            elif opcion == "3":
                print("\n--- Lista de Proveedores ---")
                for proveedor in self.crud_proveedor.proveedores:
                    print(proveedor.to_dict())
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_productos(self):
        while True:
            print("\n--- Menú Productos ---")
            print("1. Agregar Producto")
            print("2. Eliminar Producto")
            print("3. Listar Productos")
            print("4. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                id = input("ID: ")
                nombre = input("Nombre: ")
                descripcion = input("Descripción: ")
                precio_unitario = float(input("Precio Unitario: "))
                producto = Producto(id, nombre, descripcion, precio_unitario)
                self.crud_producto.agregar_producto(producto)
                print("Producto agregado exitosamente.")
            elif opcion == "2":
                id = input("ID del producto a eliminar: ")
                self.crud_producto.eliminar_producto(id)
                print("Producto eliminado exitosamente.")
            elif opcion == "3":
                print("\n--- Lista de Productos ---")
                for producto in self.crud_producto.productos:
                    print(producto.to_dict())
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_compras(self):
        print("Funcionalidad de compras no implementada aún.")

if __name__ == "__main__":
    menu = MENU()
    menu.menu_principal()
