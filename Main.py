import re
import datetime
import os
import csv
import hashlib

# Constantes para mensajes
MSG_ERROR_CAMPOS_OBLIGATORIOS = "Error: Todos los campos son obligatorios. Por favor, complete todos los datos."
MSG_ERROR_CEDULA_DUPLICADA = "Error: Esta cédula ya se encuentra registrada en el sistema."
MSG_ERROR_FORMATO_FECHA = "Error: La fecha de nacimiento no tiene el formato correcto (DD/MM/AAAA)."
MSG_ERROR_NOMBRE_APELLIDO = "Error: El nombre y apellido solo deben contener letras."
MSG_ERROR_TELEFONO = "Error: El teléfono debe contener solo números."
MSG_ERROR_CONTRASEÑAS_NO_COINCIDEN = "Error: Las contraseñas no coinciden. Intente nuevamente."
MSG_REGISTRO_EXITOSO = "Registro exitoso. ¡Bienvenido al sistema!"

def registrar_usuario(archivo_usuarios="usuarios.csv"):
    print("\nPor favor, ingrese los siguientes datos para registrarse:")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    cedula = input("Cédula: ").strip()
    fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ").strip()
    domicilio = input("Domicilio: ").strip()
    telefono = input("Teléfono: ").strip()
    contraseña = input("Contraseña: ").strip()
    confirmacion_contraseña = input("Confirmar contraseña: ").strip()

    if contraseña != confirmacion_contraseña:
        print(f"\n{MSG_ERROR_CONTRASEÑAS_NO_COINCIDEN}")
        return

    if not all([nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono, contraseña]):
        print(f"\n{MSG_ERROR_CAMPOS_OBLIGATORIOS}")
        return

    if not validar_datos(nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono):
        return

    if verificar_cedula_duplicada(cedula, archivo_usuarios):
        print(f"\n{MSG_ERROR_CEDULA_DUPLICADA}")
        return

    guardar_usuario(nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono, contraseña, archivo_usuarios)
    print(f"\n{MSG_REGISTRO_EXITOSO}")

def validar_datos(nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono):
    if not nombre.isalpha() or not apellido.isalpha():
        print(f"\n{MSG_ERROR_NOMBRE_APELLIDO}")
        return False

    if not cedula.isdigit():
        print("\nError: La cédula debe contener solo números.")
        return False

    try:
        datetime.datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
    except ValueError:
        print(f"\n{MSG_ERROR_FORMATO_FECHA}")
        return False

    if not telefono.isdigit():
        print(f"\n{MSG_ERROR_TELEFONO}")
        return False

    if len(domicilio) < 5:
        print("\nError: El domicilio es demasiado corto.")
        return False

    return True

def verificar_cedula_duplicada(cedula, archivo_usuarios="usuarios.csv"):
    if not os.path.exists(archivo_usuarios):
        return False

    with open(archivo_usuarios, "r", newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            if fila and fila[2] == cedula:
                return True
    return False

def guardar_usuario(nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono, contraseña, archivo_usuarios="usuarios.csv"):
    contraseña_encriptada = hashlib.sha256(contraseña.encode()).hexdigest()

    with open(archivo_usuarios, "a", newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono, contraseña_encriptada])

def main():
    print("Bienvenido al Sistema de Registro de Usuarios")
    registrar_usuario()

if __name__ == "__main__":
    main()
