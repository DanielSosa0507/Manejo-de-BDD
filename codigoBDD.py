import sqlite3

def conectarBD():
    return sqlite3.connect('empleados.db')


def crearTabla():
        bd = conectarBD()
        cursor = bd.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             nro_legajo INTEGER NOT NULL UNIQUE,
             dni INTEGER NOT NULL UNIQUE,
             nombre TEXT NOT NULL,
             apellido TEXT NOT NULL,
             area TEXT NOT NULL
            )
        ''')
        bd.commit()
        print('la tabla se creó exitosamente')
        bd.close()


def insertarEmpleado():
    try:
        nro_legajo = int(input("Ingrese el número de legajo: "))
        dni = int(input("Ingrese el DNI: "))
        nombre = input("Ingrese el nombre: ")
        apellido = input("Ingrese el apellido: ")
        area = input("Ingrese el área: ")

        conexion = conectarBD()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO empleados (nro_legajo, dni, nombre, apellido, area)
            VALUES (?, ?, ?, ?, ?)
        ''', (nro_legajo, dni, nombre, apellido, area))
        conexion.commit()
        print("Empleado agregado exitosamente.")
    except sqlite3.IntegrityError as e:
        print("Error: El número de legajo o DNI ya existe en la base de datos.")
    finally:
        conexion.close()


def seleccionarEmpleadoPorDNI():
    dni = int(input("Ingrese el DNI del empleado que desea consultar: "))
    conexion = conectarBD()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados WHERE dni = ?", (dni,))
    empleado = cursor.fetchone()
    conexion.close()

    if empleado:
        print("Empleado encontrado:", empleado)
    else:
        print("No se encontró un empleado con el DNI especificado.")

def seleccionarTodosLosEmpleados():
    conexion = conectarBD()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    conexion.close()

    if empleados:
        print("Lista de empleados:")
        for empleado in empleados:
            print(empleado)
    else:
        print("No hay empleados en la base de datos.")

def modificarArea():
    nro_legajo = int(input("Ingrese el número de legajo del empleado que desea modificar: "))
    nueva_area = input("Ingrese el nuevo área: ")
    
    conexion = conectarBD()
    cursor = conexion.cursor()
    cursor.execute("UPDATE empleados SET area = ? WHERE nro_legajo = ?", (nueva_area, nro_legajo))
    conexion.commit()
    conexion.close()

    if cursor.rowcount > 0:
        print("Área actualizada exitosamente.")
    else:
        print("No se encontró un empleado con el número de legajo especificado.")


def eliminarEmpleado():
    nro_legajo = int(input("Ingrese el número de legajo del empleado que desea eliminar: "))
    
    conexion = conectarBD()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM empleados WHERE nro_legajo = ?", (nro_legajo,))
    conexion.commit()
    conexion.close()

    if cursor.rowcount > 0:
        print("Empleado eliminado exitosamente.")
    else:
        print("No se encontró un empleado con el número de legajo especificado.")


def main():
    crearTabla()  
    
    while True:
        print("\nSeleccione una opción:")
        print("1. Insertar un registro de empleado")
        print("2. Seleccionar un empleado por DNI")
        print("3. Seleccionar todos los empleados")
        print("4. Modificar el área de un empleado por número de legajo")
        print("5. Eliminar un empleado por número de legajo")
        print("6. Finalizar")

        opcion = input("Ingrese la opción: ")
        
        if opcion == '1':
            insertarEmpleado()
        elif opcion == '2':
            seleccionarEmpleadoPorDNI()
        elif opcion == '3':
            seleccionarTodosLosEmpleados()
        elif opcion == '4':
            modificarArea()
        elif opcion == '5':
            eliminarEmpleado()
        elif opcion == '6':
            print("Finalizando el programa.")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()
