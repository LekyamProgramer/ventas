from components import Menu, Valida
from components import Provedor
from components import Compra
from utilities import borrarPantalla, gotoxy
from utilities import (
    reset_color,
    red_color,
    green_color,
    yellow_color,
    blue_color,
    purple_color,
    cyan_color,
)
from clsJson import JsonFile
from company import Company
from customer import RegularClient
from sales import Sale
from product import Product
from iCrud import ICrud
import datetime
import time, os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))


# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        borrarPantalla()
        print("\033c", end="")
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Registro de Cliente" + reset_color)
        validar = Valida()

        gotoxy(10, 4)
        print("Nombre:")
        gotoxy(18, 4)
        nombre = input()
        gotoxy(10, 6)
        print("Apellido:")
        gotoxy(20, 6)
        apellido = input()
        gotoxy(10, 8)
        print("Cédula:")
        gotoxy(10, 8)
        dni = validar.solo_numeros("Error: Solo números", 20, 8)

        json_file = JsonFile(path + "/archivos/clients.json")
        data = json_file.read()
        if any(c["dni"] == dni for c in data):
            gotoxy(10, 8)
            print(red_color + "❌ Cliente ya existe" + reset_color)
        else:
            data.append({"nombre": nombre, "apellido": apellido, "dni": dni})
            json_file.save(data)
            gotoxy(10, 8)
            print(green_color + "✔ Cliente guardado exitosamente" + reset_color)
        time.sleep(2)

    def update(self):
        borrarPantalla()
        print("\033c", end="")
        validar = Valida()
        gotoxy(10, 2)
        print("Ingrese cédula del cliente a modificar:")
        dni = validar.solo_numeros("Error: Solo números", 50, 2)

        json_file = JsonFile(path + "/archivos/clients.json")
        data = json_file.read()
        actualizado = False
        for client in data:
            if client["dni"] == dni:
                gotoxy(10, 4)
                print("Nuevo nombre:")
                gotoxy(23, 4)
                client["nombre"] = input()
                gotoxy(10, 5)
                print("Nuevo apellido:")
                gotoxy(25, 5)
                client["apellido"] = input()
                json_file.save(data)
                gotoxy(10, 7)
                print(green_color + "✔ Cliente actualizado" + reset_color)
                actualizado = True
                break
        if not actualizado:
            gotoxy(10, 7)
            print(red_color + "❌ Cliente no encontrado" + reset_color)
        time.sleep(2)
        borrarPantalla()

    def delete(self):
        borrarPantalla()
        print("\033c", end="")
        validar = Valida()
        gotoxy(10, 2)
        print("Ingrese cédula del cliente a eliminar:")
        dni = validar.solo_numeros("Error: Solo números", 50, 2)

        json_file = JsonFile(path + "/archivos/clients.json")
        data = json_file.read()
        nuevo = [c for c in data if c["dni"] != dni]
        if len(nuevo) < len(data):
            json_file.save(nuevo)
            gotoxy(10, 4)
            print(green_color + "✔ Cliente eliminado" + reset_color)
        else:
            gotoxy(10, 4)
            print(red_color + "❌ Cliente no encontrado" + reset_color)
        time.sleep(2)

    def consult(self):
        borrarPantalla()
        print("\033c", end="")
        gotoxy(10, 2)
        print("Consulta de clientes:")
        json_file = JsonFile(path + "/archivos/clients.json")
        data = json_file.read()
        y = 4
        for c in data:
            gotoxy(10, y)
            print(f"{c['nombre']} {c['apellido']} - Cédula: {c['dni']}")
            y += 1
        input("Presione una tecla para continuar...")


class CrudProducts(ICrud):
    def create(self):
        borrarPantalla()
        print("\033c", end="")
        validar = Valida()
        gotoxy(10, 2)
        print("Ingrese ID del producto:")
        id_ = int(validar.solo_numeros("Error", 35, 2))
        gotoxy(10, 3)
        print("Descripción:")
        gotoxy(23, 3)
        descrip = input()
        gotoxy(10, 4)
        print("Precio:")
        gotoxy(13, 4)
        preci = float(validar.solo_numeros("Error", 18, 4))
        gotoxy(10, 5)
        print("Stock:")
        stock = int(validar.solo_numeros("Error", 18, 5))

        json_file = JsonFile(path + "/archivos/products.json")
        data = json_file.read()
        if any(p["id"] == id_ for p in data):
            gotoxy(10, 7)
            print(red_color + "❌ Producto ya existe" + reset_color)
        else:
            data.append(
                {"id": id_, "descripcion": descrip, "precio": preci, "stock": stock}
            )
            json_file.save(data)
            gotoxy(10, 7)
            print(green_color + "✔ Producto guardado" + reset_color)
        time.sleep(2)

    def update(self):
        borrarPantalla()
        print("\033c", end="")
        validar = Valida()
        gotoxy(10, 2)
        print("Ingrese ID del producto a modificar:")
        id_ = int(validar.solo_numeros("Error", 50, 2))

        json_file = JsonFile(path + "/archivos/products.json")
        data = json_file.read()
        for prod in data:
            if prod["id"] == id_:
                gotoxy(10, 4)
                print("Nueva descripción:")
                prod["descripcion"] = input()
                gotoxy(10, 5)
                print("Nuevo precio:")
                prod["precio"] = float(validar.solo_numeros("Error", 35, 5))
                gotoxy(10, 6)
                print("Nuevo stock:")
                prod["stock"] = int(validar.solo_numeros("Error", 35, 6))
                json_file.save(data)
                gotoxy(10, 8)
                print(green_color + "✔ Producto actualizado" + reset_color)
                break
        else:
            gotoxy(10, 8)
            print(red_color + "❌ Producto no encontrado" + reset_color)
        time.sleep(2)

    def delete(self):
        borrarPantalla()
        print("\033c", end="")
        validar = Valida()
        gotoxy(10, 2)
        print("Ingrese ID del producto a eliminar:")
        id_ = int(validar.solo_numeros("Error", 50, 2))

        json_file = JsonFile(path + "/archivos/products.json")
        data = json_file.read()
        nuevo = [p for p in data if p["id"] != id_]
        if len(nuevo) < len(data):
            json_file.save(nuevo)
            gotoxy(10, 4)
            print(green_color + "✔ Producto eliminado" + reset_color)
        else:
            gotoxy(10, 4)
            print(red_color + "❌ Producto no encontrado" + reset_color)
        time.sleep(2)

    def consult(self):
        borrarPantalla()
        print("\033c", end="")
        gotoxy(10, 2)
        print("Consulta de productos:")
        json_file = JsonFile(path + "/archivos/products.json")
        data = json_file.read()
        y = 4
        for p in data:
            gotoxy(10, y)
            print(
                f"ID: {p['id']} - {p['descripcion']} - ${p['precio']} - Stock: {p['stock']}"
            )
            y += 1
        input("Presione una tecla para continuar...")


class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print("\033c", end="")
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Registro de Compra")
        gotoxy(17, 3)
        print(blue_color + Company.get_business_name())
        gotoxy(5, 4)
        print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66, 4)
        print("Subtotal:")
        gotoxy(66, 6)
        print("Iva     :")
        gotoxy(66, 7)
        print("Total   :")
        gotoxy(15, 6)
        print("Ruc")
        ruc = validar.solo_numeros("Error: Solo numeros", 23, 6)
        json_file = JsonFile(path + "/archivos/provedor.json")
        provedor = json_file.find("ruc", ruc)
        if not provedor:
            gotoxy(35, 6)
            print("provedor no existe")
            return
        provedor = provedor[0]
        cli = Provedor(
            provedor["nombre"],
            provedor["ruc"],
            provedor["direccion"],
            provedor["telefono"],
            provedor["email"],
        )
        sale = Compra(cli)
        gotoxy(35, 6)
        print(cli.nombre)
        gotoxy(2, 8)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(5, 9)
        print(purple_color + "Linea")
        gotoxy(12, 9)
        print("Id_Articulo")
        gotoxy(24, 9)
        print("Descripcion")
        gotoxy(38, 9)
        print("Precio")
        gotoxy(48, 9)
        print("Cantidad")
        gotoxy(58, 9)
        print("Subtotal")
        gotoxy(70, 9)
        print("n->Terminar Venta)" + reset_color)
        # detalle de la venta
        follow = "s"
        line = 1
        while follow.lower() == "s":
            gotoxy(7, 9 + line)
            print(line)
            gotoxy(15, 9 + line)
            id = int(validar.solo_numeros("Error: Solo numeros", 15, 9 + line))
            json_file = JsonFile(path + "/archivos/products.json")
            prods = json_file.find("id", id)
            if not prods:
                gotoxy(24, 9 + line)
                print("Producto no existe")
                time.sleep(5)
                gotoxy(24, 9 + line)
                print(" " * 20)
            else:
                prods = prods[0]
                product = Product(
                    prods["id"], prods["descripcion"], prods["precio"], prods["stock"]
                )
                gotoxy(24, 9 + line)
                print(product.descrip)
                gotoxy(38, 9 + line)
                print(product.preci)
                gotoxy(49, 9 + line)
                qyt = int(validar.solo_numeros("Error:Solo numeros", 49, 9 + line))
                gotoxy(59, 9 + line)
                print(product.preci * qyt)
                sale.add_detail(product, qyt)
                gotoxy(76, 4)
                print(round(sale.subtotal, 2))
                gotoxy(76, 6)
                print(round(sale.iva, 2))
                gotoxy(76, 7)
                print(round(sale.total, 2))
                gotoxy(74, 9 + line)
                follow = input() or "s"
                gotoxy(76, 9 + line)
                print(green_color + "✔" + reset_color)
                line += 1
        gotoxy(15, 9 + line)
        print(red_color + "Esta seguro de grabar la venta(s/n):")
        gotoxy(54, 9 + line)
        procesar = input().lower()
        if procesar == "s":
            gotoxy(15, 10 + line)
            print("😊 Venta Grabada satisfactoriamente 😊" + reset_color)
            # print(sale.getJson())
            json_file = JsonFile(path + "/archivos/invoices.json")
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"] + 1
            data = sale.getJson()
            data["factura"] = ult_invoices
            invoices.append(data)
            json_file = JsonFile(path + "/archivos/invoices.json")
            json_file.save(invoices)
        else:
            gotoxy(20, 10 + line)
            print("🤣 Venta Cancelada 🤣" + reset_color)
        time.sleep(2)

    def update(self):
        borrarPantalla()
        validar = Valida()
        gotoxy(10, 2)
        print("Ingrese el número de factura a modificar:")
        factura = int(validar.solo_numeros("Error: Solo números", 50, 2))

        json_file = JsonFile(path + "/archivos/invoices.json")
        ventas = json_file.read()

        for venta in ventas:
            if venta["factura"] == factura:
                gotoxy(10, 4)
                print("Factura encontrada:")
                gotoxy(10, 5)
                print(f"Cliente: {venta['cliente']}")
                gotoxy(10, 6)
                print("Desea modificar esta venta? (s/n):")
                confirm = input().lower()

                if confirm == "s":
                    # Por simplicidad, eliminamos la venta original y volvemos a crearla
                    ventas.remove(venta)
                    json_file.save(ventas)
                    gotoxy(10, 8)
                    print("✔ Ingrese los nuevos datos de la venta")
                    time.sleep(2)
                    self.create()  # Reutilizamos create para volver a registrar
                else:
                    gotoxy(10, 8)
                    print("❌ Modificación cancelada")
                break
        else:
            gotoxy(10, 7)
            print("❌ Factura no encontrada")

        time.sleep(2)

    def delete(self):
        borrarPantalla()
        validar = Valida()
        gotoxy(10, 2)
        print("Ingrese el número de factura a eliminar:")
        factura = int(validar.solo_numeros("Error: Solo números", 50, 2))

        json_file = JsonFile(path + "/archivos/invoices.json")
        ventas = json_file.read()

        for venta in ventas:
            if venta["factura"] == factura:
                gotoxy(10, 4)
                print("Factura encontrada:")
                gotoxy(10, 5)
                print(f"Cliente: {venta['cliente']}")
                gotoxy(10, 6)
                print("¿Está seguro que desea eliminarla? (s/n):")
                confirm = input().lower()
                if confirm == "s":
                    ventas.remove(venta)
                    json_file.save(ventas)
                    gotoxy(10, 8)
                    print("🗑️ Venta eliminada correctamente")
                else:
                    gotoxy(10, 8)
                    print("❌ Eliminación cancelada")
                break
        else:
            gotoxy(10, 7)
            print("❌ Factura no encontrada")

        time.sleep(2)

    def consult(self):
        print("\033c", end="")
        gotoxy(2, 1)
        print(green_color + "█" * 90)
        gotoxy(2, 2)
        print("██" + " " * 34 + "Consulta de Venta" + " " * 35 + "██")
        gotoxy(2, 4)
        invoice = input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path + "/archivos/invoices.json")
            invoices = json_file.find("factura", invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:
            json_file = JsonFile(path + "/archivos/invoices.json")
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(
                    f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}"
                )

            suma = reduce(
                lambda total, invoice: round(total + invoice["total"], 2), invoices, 0
            )
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(
                filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices)
            )

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ", total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x = input("presione una tecla para continuar...")


class CrudCompras(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print("\033c", end="")
        gotoxy(2, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Registro de Compra")
        gotoxy(17, 3)
        print(blue_color + Company.get_business_name())
        gotoxy(5, 4)
        print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66, 4)
        print("Subtotal:")
        gotoxy(66, 6)
        print("Iva     :")
        gotoxy(66, 7)
        print("Total   :")
        gotoxy(15, 6)
        print("Ruc")
        ruc = validar.solo_numeros("Error: Solo numeros", 23, 6)
        json_file = JsonFile(path + "/archivos/provedor.json")
        provedor = json_file.find("ruc", ruc)
        if not provedor:
            gotoxy(35, 6)
            print("provedor no existe")
            return
        provedor = provedor[0]
        cli = Provedor(
            provedor["nombre"],
            provedor["ruc"],
            provedor["direccion"],
            provedor["telefono"],
            provedor["email"],
        )
        sale = Compra(cli)
        gotoxy(35, 6)
        print(cli.nombre)
        gotoxy(2, 8)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(5, 9)
        print(purple_color + "Linea")
        gotoxy(12, 9)
        print("Id_Articulo")
        gotoxy(24, 9)
        print("Descripcion")
        gotoxy(38, 9)
        print("Precio")
        gotoxy(48, 9)
        print("Cantidad")
        gotoxy(58, 9)
        print("Subtotal")
        gotoxy(70, 9)
        print("n->Terminar Venta)" + reset_color)
        # detalle de la venta
        follow = "s"
        line = 1
        while follow.lower() == "s":
            gotoxy(7, 9 + line)
            print(line)
            gotoxy(15, 9 + line)
            id = int(validar.solo_numeros("Error: Solo numeros", 15, 9 + line))
            json_file = JsonFile(path + "/archivos/products.json")
            prods = json_file.find("id", id)
            if not prods:
                gotoxy(24, 9 + line)
                print("Producto no existe")
                time.sleep(5)
                gotoxy(24, 9 + line)
                print(" " * 20)
            else:
                prods = prods[0]
                product = Product(
                    prods["id"], prods["descripcion"], prods["precio"], prods["stock"]
                )
                gotoxy(24, 9 + line)
                print(product.descrip)
                gotoxy(38, 9 + line)
                print(product.preci)
                gotoxy(49, 9 + line)
                qyt = int(validar.solo_numeros("Error:Solo numeros", 49, 9 + line))
                gotoxy(59, 9 + line)
                print(product.preci * qyt)
                sale.add_detail(product, qyt)
                gotoxy(76, 4)
                print(round(sale.subtotal, 2))
                gotoxy(76, 6)
                print(round(sale.iva, 2))
                gotoxy(76, 7)
                print(round(sale.total, 2))
                gotoxy(74, 9 + line)
                follow = input() or "s"
                gotoxy(76, 9 + line)
                print(green_color + "✔" + reset_color)
                line += 1
        gotoxy(15, 9 + line)
        print(red_color + "Esta seguro de grabar la venta(s/n):")
        gotoxy(54, 9 + line)
        procesar = input().lower()
        if procesar == "s":
            gotoxy(15, 10 + line)
            print("😊 Venta Grabada satisfactoriamente 😊" + reset_color)
            # print(sale.getJson())
            json_file = JsonFile(path + "/archivos/invoices.json")
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"] + 1
            data = sale.getJson()
            data["factura"] = ult_invoices
            invoices.append(data)
            json_file = JsonFile(path + "/archivos/invoices.json")
            json_file.save(invoices)
        else:
            gotoxy(20, 10 + line)
            print("🤣 Venta Cancelada 🤣" + reset_color)
        time.sleep(2)

    def update(self):
        pass

    def delete(self):
        pass

    def consult(self):
        pass


# Menu Proceso Principal

opc = ""
while opc != "4":
    borrarPantalla()
    menu_main = Menu(
        "Menu Facturacion",
        ["1) Clientes", "2) Productos", "3) Ventas", "4) Compra", "5) Salir"],
        20,
        10,
    )
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ""
        crud_clientes = CrudClients()
        while opc1 != "5":
            borrarPantalla()
            menu_clients = Menu(
                "Menu Cientes",
                [
                    "1) Ingresar",
                    "2) Actualizar",
                    "3) Eliminar",
                    "4) Consultar",
                    "5) Salir",
                ],
                20,
                10,
            )
            opc1 = menu_clients.menu()
            if opc1 == "1":
                crud_clientes.create()
            elif opc1 == "2":
                crud_clientes.update()
            elif opc1 == "3":
                crud_clientes.delete()
            elif opc1 == "4":
                crud_clientes.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)
    elif opc == "2":
        opc2 = ""
        crud_productos = CrudProducts()
        while opc2 != "5":
            borrarPantalla()
            menu_products = Menu(
                "Menu Productos",
                [
                    "1) Ingresar",
                    "2) Actualizar",
                    "3) Eliminar",
                    "4) Consultar",
                    "5) Salir",
                ],
                20,
                10,
            )
            opc2 = menu_products.menu()
            if opc2 == "1":
                crud_productos.create()
            elif opc2 == "2":
                crud_productos.update()
            elif opc2 == "3":
                crud_productos.delete()
            elif opc2 == "4":
                crud_productos.consult()
    elif opc == "3":
        opc3 = ""
        while opc3 != "5":
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu(
                "Menu Ventas",
                [
                    "1) Registro Venta",
                    "2) Consultar",
                    "3) Modificar",
                    "4) Eliminar",
                    "5) Salir",
                ],
                20,
                10,
            )
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()

            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()

    elif opc == "4":
        opc4 = ""
        while opc4 != "5":
            borrarPantalla()
            compra = CrudCompras()
            menu_sales = Menu(
                "Menu Compras",
                [
                    "1) Registro Compra",
                    "2) Consultar",
                    "3) Modificar",
                    "4) Eliminar",
                    "5) Salir",
                ],
                20,
                10,
            )
            opc4 = menu_sales.menu()
            if opc4 == "1":
                compra.create()

            elif opc4 == "2":
                compra.consult()
                time.sleep(2)
            elif opc4 == "3":
                compra.update()
            elif opc4 == "4":
                compra.delete()

    print("Regresando al menu Principal...")
    time.sleep(2)

borrarPantalla()

input("Presione una tecla para salir...")
borrarPantalla()
