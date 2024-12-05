# Main.py
import re
import datetime
import os
import csv
import hashlib


def registrar_usuario():
    print("\nPor favor, ingrese los siguientes datos para registrarse:")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    cedula = input("Cédula: ").strip()
    fecha_nacimiento = input("Fecha de nacimiento (DD/MM/AAAA): ").strip()
    domicilio = input("Domicilio: ").strip()
    telefono = input("Teléfono: ").strip()
    contraseña = input("Contraseña: ").strip()
    confirmacion_contraseña = input("Confirmar contraseña: ").strip()

    # Validar que las contraseñas coincidan
    if contraseña != confirmacion_contraseña:
        print("\nError: Las contraseñas no coinciden. Intente nuevamente.")
        return

    # Validar que todos los campos estén llenos
    if not all([nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono, contraseña]):
        print("\nError: Todos los campos son obligatorios. Por favor, complete todos los datos.")
        return

    # Validar los datos ingresados
    if not validar_datos(nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono):
        return

    # Validar que la cédula no esté ya registrada
    if verificar_cedula_duplicada(cedula):
        print("\nError: Esta cédula ya se encuentra registrada en el sistema.")
        return

    # Guardar los datos del usuario
    guardar_usuario(nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono, contraseña)
    print("\nRegistro exitoso. ¡Bienvenido al sistema!")

def validar_datos(nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono):
    # Validar que el nombre y apellido solo contengan letras
    if not nombre.isalpha():
        print("\nError: El nombre solo debe contener letras.")
        return False
    if not apellido.isalpha():
        print("\nError: El apellido solo debe contener letras.")
        return False

    # Validar que la cédula sea numérica
    if not cedula.isdigit():
        print("\nError: La cédula debe contener solo números.")
        return False

    # Validar formato de fecha
    try:
        datetime.datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
    except ValueError:
        print("\nError: La fecha de nacimiento no tiene el formato correcto (DD/MM/AAAA).")
        return False

    # Validar que el teléfono sea numérico
    if not telefono.isdigit():
        print("\nError: El teléfono debe contener solo números.")
        return False

    # Validar longitud mínima del domicilio
    if len(domicilio) < 5:
        print("\nError: El domicilio es demasiado corto.")
        return False

    return True

def verificar_cedula_duplicada(cedula, archivo_usuarios="usuarios.csv"):
    if not os.path.exists(archivo_usuarios):
        return False  # No hay usuarios registrados aún

    with open(archivo_usuarios, "r", newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            if fila and fila[2] == cedula:
                return True  # Cédula duplicada
    return False

def guardar_usuario(nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono, contraseña, archivo_usuarios="usuarios.csv"):
    # Encriptar la contraseña
    contraseña_encriptada = hashlib.sha256(contraseña.encode()).hexdigest()

    with open(archivo_usuarios, "a", newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([nombre, apellido, cedula, fecha_nacimiento, domicilio, telefono, contraseña_encriptada])

def main():
    print("Bienvenido al Sistema de Registro de Usuarios")
    registrar_usuario()

if __name__ == "__main__":
    main()
