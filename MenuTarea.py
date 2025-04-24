from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        borrarPantalla()
        gotoxy(10, 2); print("Registro de Cliente")
        valida = Valida()
        nombre = valida.solo_letras("Nombre:", "Error: Solo letras")
        apellido = valida.solo_letras("Apellido:", "Error: Solo letras")
        dni = valida.cedula("Cedula inválida", 10, 5)
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        new_client = {"nombre": nombre, "apellido": apellido, "dni": dni}
        clients.append(new_client)
        json_file.save(clients)
        print("✅ Cliente registrado con éxito")
        time.sleep(2)
 
    def update():
        borrarPantalla()
        gotoxy(10, 2); print("Actualizar Cliente")
        dni = input("Ingrese la cédula del cliente: ")
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        for c in clients:
            if c["dni"] == dni:
                c["nombre"] = input("Nuevo nombre: ")
                c["apellido"] = input("Nuevo apellido: ")
                json_file.save(clients)
                print("✅ Cliente actualizado con éxito")
                break
        else:
            print("❌ Cliente no encontrado")
        time.sleep(2)
        
    def delete(self):
        borrarPantalla()
        gotoxy(10, 2); print("Eliminar Cliente")
        dni = input("Ingrese la cédula del cliente: ")
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        clients = [c for c in clients if c["dni"] != dni]
        json_file.save(clients)
        print("✅ Cliente eliminado (si existía)")
        time.sleep(2)
    
    def consult(self):
        borrarPantalla()
        gotoxy(10, 2); print("Consulta Clientes")
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        for client in clients:
            print(f"{client['dni']} | {client['nombre']} {client['apellido']}")
        input("Presione una tecla para continuar...")

class CrudProducts(ICrud):
    def create(self):
        borrarPantalla()
        gotoxy(10, 2); print("Registro de Producto")
        valida = Valida()
        id = int(valida.solo_numeros("ID inválido", 10, 5))
        descripcion = input("Descripción: ")
        precio = float(valida.solo_decimales("Precio:", "Error"))
        stock = int(valida.solo_numeros("Stock:", 10, 6))
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        new_product = {"id": id, "descripcion": descripcion, "precio": precio, "stock": stock}
        products.append(new_product)
        json_file.save(products)
        print("✅ Producto registrado")
        time.sleep(2)

    def update(self):
        borrarPantalla()
        gotoxy(10, 2); print("Actualizar Producto")
        id = int(input("ID del producto: "))
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        for p in products:
            if p["id"] == id:
                p["descripcion"] = input("Nueva descripción: ")
                p["precio"] = float(input("Nuevo precio: "))
                p["stock"] = int(input("Nuevo stock: "))
                json_file.save(products)
                print("✅ Producto actualizado")
                break
        else:
            print("❌ Producto no encontrado")
        time.sleep(2)

    def delete(self):
        borrarPantalla()
        gotoxy(10, 2); print("Eliminar Producto")
        id = int(input("ID del producto: "))
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        products = [p for p in products if p["id"] != id]
        json_file.save(products)
        print("✅ Producto eliminado (si existía)")
        time.sleep(2)

    def consult(self):
        borrarPantalla()
        gotoxy(10, 2); print("Consulta Productos")
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
        for p in products:
            print(f"{p['id']} | {p['descripcion']} | {p['precio']} | {p['stock']}")
        input("Presione una tecla para continuar...")


class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    
    
    def update():
        pass
    
    def delete():
        pass
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x=input("presione una tecla para continuar...")    

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla() 
            sales = CrudSales()
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                sales.create()
            elif opc1 == "2":
                sales.update()
            elif opc1 == "3":
                sales.delete()
            elif opc1 == "4":
                sales.consult()

            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                pass
            elif opc2 == "2":
                pass
            elif opc2 == "3":
                pass
            elif opc2 == "4":
                pass
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
                
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()

input("Presione una tecla para salir...")
borrarPantalla()

