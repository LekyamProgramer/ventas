# Modelo: Registro de Crédito por Venta
import json
import os

class CreditoVenta:
    def __init__(self, id: str, cabecera_venta: str, total_credito: float, estado="Pendiente"):
        self.id: str = id
        self.cabecera_venta: str = cabecera_venta  # Objeto tipo CabVenta
        self.total_credito: float = total_credito
        self.saldo_credito: float = total_credito
        self.estado = estado  # "Pendiente", "Parcial", "Pagado"
        self.pagos = []  # Lista de PagosCredito

    def to_dict(self):
        return {
            "id": self.id,
            "cabecera_venta": self.cabecera_venta,
            "total_credito": self.total_credito,
            "saldo_credito": self.saldo_credito,
            "estado": self.estado,
            "pagos": self.pagos,
        }

    @staticmethod
    def from_dict(data):
        credito = CreditoVenta(
            id=data["id"],
            cabecera_venta=data["cabecera_venta"],
            total_credito=data["total_credito"],
            estado=data["estado"],
        )
        credito.saldo_credito = data["saldo_credito"]
        credito.pagos = data["pagos"]
        return credito


class CrudCredito:
    def __init__(self, archivo="credito.json"):
        self.archivo = archivo
        self.credito = self.cargar_credito()

    def cargar_credito(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as file:
                return [CreditoVenta.from_dict(data) for data in json.load(file)]
        return []

    def guardar_credito(self):
        with open(self.archivo, "w") as file:
            json.dump([creditos.to_dict() for creditos in self.credito], file, indent=4)

    def agregar_credito(self, creditoVenta: CreditoVenta):
        self.credito.append(creditoVenta)
        self.guardar_credito()

    def eliminar_credito(self, id: str):
        self.credito = [creditos for creditos in self.credito if creditos.id != id]
        self.guardar_credito()


# Modelo: Pagos realizados por la venta a crédito
class PagoCredito:
    def __init__(self, id: str, fecha_pago: str, valor: float):
        self.id: str = id
        self.fecha_pago: str = fecha_pago
        self.valor: float = valor

        #--------Crud pago de credito-----------

# class CrudPagoCredito:
#     def __init__(self, archivo="credito.json"):
#         self.archivo = archivo
#         self.credito = self.cargar_credito()

#     def cargar_credito(self):
#         if os.path.exists(self.archivo):
#             with open(self.archivo, "r") as file:
#                 return [CreditoVenta.from_dict(data) for data in json.load(file)]
#         return []

#     def guardar_credito(self):
#         with open(self.archivo, "w") as file:
#             json.dump([creditos.to_dict() for creditos in self.credito], file, indent=4)

#     def agregar_credito(self, creditoVenta: CreditoVenta):
#         self.credito.append(creditoVenta)
#         self.guardar_credito()

#     def eliminar_credito(self, id: str):
#         self.credito = [creditos for creditos in self.credito if creditos.id != id]
#         self.guardar_credito()

class Menu:
    def __init__(self):
        self.crud_credito = CrudCredito()

    def menu_principal(self):
        while True:
            print("\n--- Menú Principal ---")
            print("1. Crédito Ventas")
            print("2. Pago Crédito")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.menu_credito_ventas()
            elif opcion == "2":
                print("OPCIÓN NO HABILITADA")
            elif opcion == "3":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def menu_credito_ventas(self):
        while True:
            print("\n--- Menú Crédito Ventas ---")
            print("1. Agregar crédito")
            print("2. Eliminar crédito")
            print("3. Listar créditos")
            print("4. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                id = input("Id: ")
                cabecera = input("Cabecera venta: ")
                total_de_credito = float(input("Total de crédito: "))
                Estado = input("estado: pendiente, completo, parcial:   ")
                credito = CreditoVenta(id, cabecera, total_de_credito,Estado)
                self.crud_credito.agregar_credito(credito)
                print("Crédito agregado exitosamente.")
            elif opcion == "2":
                id = input("ID del crédito a eliminar: ")
                self.crud_credito.eliminar_credito(id)
                print("Crédito eliminado exitosamente.")
            elif opcion == "3":
                print("\n--- Lista de Créditos ---")
                for credito in self.crud_credito.credito:
                    print(credito.to_dict())
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu = Menu()
    menu.menu_principal()
