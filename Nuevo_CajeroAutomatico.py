import datetime

class Usuario:
    def __init__(self, identificador_usuario, nombre, saldo, contraseña):
        self.identificador_usuario = identificador_usuario
        self.nombre = nombre
        self.saldo = saldo
        self.contraseña = contraseña
        self.transacciones = []
        
    def verificar_contraseña(self, contraseña):
        return self.contraseña == contraseña
    
    def depositar(self, cantidad, billetes):
        self.saldo += cantidad
        self.transacciones.append((datetime.datetime.now(), "Deposito" , cantidad))
        return True
    
    def retirar(self, cantidad):
        if cantidad <= self.saldo:
            self.saldo -= cantidad
            self.transacciones.append((datetime.datetime.now(), "Retiro" , -cantidad))
            return True
        return False
    
    def transferir(self, cantidad, receptor):
        if cantidad <= self.saldo:
            self.saldo -= cantidad
            receptor.saldo += cantidad
            self.transacciones.append((datetime.datetime.now(), "Transferencia Saliente", -cantidad))
            receptor.transacciones.append((datetime.datetime.now(), "Transferencia Entrante", cantidad))
            print(f"Transferencia de {cantidad} realizada con éxito a {receptor.nombre}.")
            return True
        else:
            print(f"Saldo insuficiente. No se puede transferir {cantidad}.")
            return False

    
    def pagar_servicio(self, cantidad, tipo_servicio):
        if cantidad <= self.saldo:
            self.saldo -= cantidad
            self.transacciones.append((datetime.datetime.now(), f"Pago de {tipo_servicio}", -cantidad))
            return True
        return False
    
    def consultar_saldo(self):
        return self.saldo
    
    def consultar_transacciones(self):
        return self.transacciones
    
class Cajero:
    
    def __init__(self):
        self.usuarios = {}
        self.dispensador = {200: 0, 100: 0, 50: 0, 20: 0}
        
    def agregar_usuario(self, usuario):
        self.usuarios[usuario.identificador_usuario] = usuario
        
    def buscar_usuario(self, identificador_usuario):
        return self.usuarios.get(identificador_usuario)
    
    def cargar_dispensador(self, denominacion, cantidad):
        if denominacion in self.dispensador:
            self.dispensador[denominacion] += cantidad
            return True
        return False
    
    def dispensador_dinero(self, cantidad):
        resultado = {}
        for denominacion in sorted(self.dispensador.keys(), reverse=True):
            if cantidad >= denominacion:
                num_billetes = min(cantidad // denominacion, self.dispensador[denominacion])
                if num_billetes > 0:
                    resultado[denominacion] = num_billetes
                    cantidad -= denominacion * num_billetes
                    self.dispensador[denominacion] -= num_billetes
        if cantidad == 0:
            return resultado
        return None
    
    def consultar_total_dinero(self):
        total = sum(denom * cantidad for denom, cantidad in self.dispensador.items())
        return total
    
    def mostrar_menu(self):
        print("===Cajero Automático===")
        print("1. Registrar usuario: ")
        print("2. Deposito: ")
        print("3. Retiro: ")
        print("4. Transferencia: ")
        print("5. Pago de servicios: ")
        print("6. Consulta de Saldo: ")
        print("7. Consulta de transacciones: ")
        print("8. Cargar dinero al cajero")
        print("9. Consultar dinero al cajero")
        print("10. Salir")
        
    def mostrar_menu_servicios(self):
        print("===Pago de Servicios===")
        print("1. Agua")
        print("2. Luz")
        print("3. Gas")
        print("4. Internet")
        print("5. Telefonia")
        print("6. Volver al menu principal")
        
    def solicitar_contraseña(self):
        return input("Ingrese la contraseña de 4 digitos: ")
    
    def validar_contraseña(self, contraseña):
        return contraseña.isdigit() and len(contraseña) == 4
    
    def validar_identificador_usuario(self, identificador_usuario):
        return identificador_usuario.isdigit()
    
    def validar_nombre(self, nombre):
        return all(x.isalpha() or x.isspace() for x in nombre)
    
    def validar_saldo(self, saldo):
        try:
            float(saldo)
            return True
        except ValueError:
            return False

cajero = Cajero()
    
while True:
    cajero.mostrar_menu()
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        identificador_usuario = input("Ingrese el ID del usuario: ")
        if not cajero.validar_identificador_usuario(identificador_usuario):
            print("El ID del usuario es invalido")
            continue
        nombre = input("Ingrese nombre del usuario: ")
        if not cajero.validar_nombre(nombre):
            print("El nombre del usuario es invalido")
            continue
        saldo = input("Ingrese saldo inicial del usuario: ")
        if not cajero.validar_saldo(saldo):
            print("Saldo invalido")
            continue
        saldo = float(saldo)
        while True:
            contraseña = cajero.solicitar_contraseña()
            if cajero.validar_contraseña(contraseña):
                break
            else:
                print("Contraseña invalida")
        usuario = Usuario(identificador_usuario, nombre, saldo, contraseña)
        cajero.agregar_usuario(usuario)
        print("Usuario registrado con exito")
        
    elif opcion == "2":
        identificador_usuario = input("Ingrese ID del usuario: ")
        if not cajero.validar_identificador_usuario(identificador_usuario):
            print("El ID del usuario es invalido")
            continue
        usuario = cajero.buscar_usuario(identificador_usuario)
        if usuario:
            contraseña = cajero.solicitar_contraseña()
            if usuario.verificar_contraseña(contraseña):
                cantidad = input("Ingrese cantidad a depositar: ")
                if not cajero.validar_saldo(cantidad):
                    print("Cantidad inválida")
                    continue
                cantidad = float(cantidad)
                billetes = {}
                total_depositado = 0
                while total_depositado < cantidad:
                    denom = int(input("Ingrese denominacion del billete: "))
                    num_billetes = int(input("Ingrese cantidad de billetes: "))
                    total_depositado += denom * num_billetes
                    billetes[denom] = num_billetes
                usuario.depositar(total_depositado, billetes)
                for denom, num_billetes in billetes.items():
                    cajero.cargar_dispensador(denom, num_billetes)
                print("Deposito realizado con exito")
            else:
                print("Contraseña incorrecta")
        else:
            print("Usuario no encontrado")
        
    elif opcion == "3":
        identificador_usuario = input("Ingrese ID del usuario: ")
        if not cajero.validar_identificador_usuario(identificador_usuario):
            print("El ID del usuario es incorrecto")
            continue
        usuario = cajero.buscar_usuario(identificador_usuario)
        if usuario:
            contraseña = cajero.solicitar_contraseña()
            if usuario.verificar_contraseña(contraseña):
                cantidad = input("Ingrese la cantidad a retirar: ")
                if not cajero.validar_saldo(cantidad):
                    print("Cantidad invalida")
                    continue
                cantidad = float(cantidad)
                if usuario.retirar(cantidad):
                    billetes = cajero.dispensador_dinero(cantidad)
                    if billetes:
                        print("Retiro realizado con exito")
                    else:
                        print("Disculpe, la caja no cuenta con suficientes billetes")
                else:
                    print("Saldo insuficiente")
            else:
                print("Contraseña incorrecta")
        else:
            print("Usuario no encontrado")
                
    elif opcion == "4":
        id_origen = input("Ingrese ID del usuario original: ")
        if not cajero.validar_identificador_usuario(id_origen):
            print("El ID es invalido")
            continue
        usuario_origen = cajero.buscar_usuario(id_origen)
        if usuario_origen:
            contraseña = cajero.solicitar_contraseña()
            if usuario_origen.verificar_contraseña(contraseña):
                id_destino = input("Ingrese ID del usuario destino: ")
                if not cajero.validar_identificador_usuario(id_destino):
                    print("El ID del usuario destino es invalido")
                    continue
                usuario_destino = cajero.buscar_usuario(id_destino)
                if usuario_destino:
                    cantidad = input("Ingrese cantidad a transferir: ")
                    if not cajero.validar_saldo(cantidad):
                        print("La cantidad es invalida")
                        continue
                    cantidad = float(cantidad)
                    if cantidad <= 0:
                        print("La cantidad a transferir debe ser mayor que 0.")
                        continue
                    if usuario_origen.transferir(cantidad, usuario_destino):
                        print("Transferencia realizada con exito")
                else:
                    print("Usuario destino no encontrado")
            else:
                print("Contraseña incorrecta")
        else:
            print("Usuario origen no encontrado")
        
    elif opcion == "5":
        while True:
            cajero.mostrar_menu_servicios()
            opcion_servicio = input("Seleccion el servicio a pagar: ")
            if opcion_servicio in ["1", "2", "3", "4", "5"]:
                servicios = ["Agua","Luz","Gas","Internet","Telefonia"]
                tipo_servicio = servicios[int(opcion_servicio)-1]
                identificador_usuario = input("Ingrese ID del usuario: ")
                if not cajero.validar_identificador_usuario(identificador_usuario):
                    print("El ID del usuario es invalido")
                    continue
                usuario = cajero.buscar_usuario(identificador_usuario)
                if usuario:
                    contraseña = cajero.solicitar_contraseña()
                    if usuario.verificar_contraseña(contraseña):
                        cantidad = input(f"Ingrese la cantidad del pago de {tipo_servicio}: ")
                        if not cajero.validar_saldo(cantidad):
                            print("Cantidad invalida")
                            continue
                        cantidad = float(cantidad)
                        if usuario.pagar_servicio(cantidad, tipo_servicio):
                            print(f"Pago de {tipo_servicio} realizado con exito")
                        else:
                            print("Saldo insuficiente")
                    else:
                        print("Contraseña incorrecta")
                else:
                    print("Usuario no encontrado")
            elif opcion_servicio == "6":
                break
            else:
                print("Opcion no valida, intente otra vez")
                
    elif opcion == "6":
        identificador_usuario = input("Ingrese ID del usuario: ")
        if not cajero.validar_identificador_usuario(identificador_usuario):
            print("El ID del usuario es invalido")
            continue
        usuario = cajero.buscar_usuario(identificador_usuario)
        if usuario:
            contraseña = cajero.solicitar_contraseña()
            if usuario.verificar_contraseña(contraseña):
                print(f"El saldo del usuario es: {usuario.consultar_saldo()}")
            else:
                print("Contraseña incorrecta")
        else:
            print("Usuario no encontrado")
                    
    elif opcion == "7":
        identificador_usuario = input("Ingrese ID del usuario: ")
        if not cajero.validar_identificador_usuario(identificador_usuario):
            print("El ID del usuario es invalido")
            continue
        usuario = cajero.buscar_usuario(identificador_usuario)
        if usuario:
            contraseña = cajero.solicitar_contraseña()
            if usuario.verificar_contraseña(contraseña):
                transacciones = usuario.consultar_transacciones()
                for trans in transacciones:
                    color = "\033[91m" if trans[2] < 0 else "\033[94m"
                    print(f"{color}Fecha: {trans[0]}, Tipo: {trans[1]}, Cantidad: {trans[2]}\033[0m")
            else:
                print("Contraseña incorrecta")
        else:
            print("Usuario no encontrado")
                        
    elif opcion == "8":
        try:
            denominacion = int(input("Ingrese la denominación del billete: "))
            cantidad = int(input("Ingrese la cantidad de billetes: "))
            if cajero.cargar_dispensador(denominacion, cantidad):
                print("Dispensador cargado con exito")
            else:
                print("Denominacion de billete no válida")
        except ValueError:
            print("La entrada invalida")
                
    elif opcion == "9":
        total_dinero = cajero.consultar_total_dinero()
        print(f"La cantidad total de dinero en el cajero es: {total_dinero}")
                    
    elif opcion == "10":
        print("Gracias por usar nuestro cajero automático")
        break
    else:
        print("Opcion no valida, porfavor intente otra vez")
