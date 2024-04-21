import redis

# Conexión a Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# Función para agregar una nueva receta
# Función para agregar una nueva receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos de la receta: ")

    # Convertir ingredientes a lista
    ingredientes_lista = ingredientes.split(',')

    nueva_receta = {
        'nombre': nombre,
        'ingredientes': ','.join(ingredientes_lista),  # Convertir lista de ingredientes a string
        'pasos': pasos
    }

    # Convertir valores del diccionario a bytes
    nueva_receta_bytes = {k: v.encode() if isinstance(v, str) else str(v).encode() for k, v in nueva_receta.items()}

    redis_client.hset(f"receta:{nombre}", mapping=nueva_receta_bytes)
    print("Receta agregada con éxito.")



# Función para actualizar una receta existente
def actualizar_receta():
    nombre = input("Ingrese el nombre de la receta que desea actualizar: ")
    receta = redis_client.hgetall(f"receta:{nombre}")

    if receta:
        print(f"Receta actual: {receta}")
        nombre = input("Nuevo nombre de la receta (deje en blanco para no cambiar): ") or receta[b'nombre'].decode()
        ingredientes = input("Nuevos ingredientes (deje en blanco para no cambiar): ") or receta[
            b'ingredientes'].decode()
        pasos = input("Nuevos pasos de la receta (deje en blanco para no cambiar): ") or receta[b'pasos'].decode()

        nueva_receta = {
            'nombre': nombre,
            'ingredientes': ingredientes.split(','),
            'pasos': pasos
        }

        redis_client.hmset(f"receta:{nombre}", nueva_receta)
        print("Receta actualizada con éxito.")
    else:
        print("Receta no encontrada.")


# Función para eliminar una receta existente
def eliminar_receta():
    nombre = input("Ingrese el nombre de la receta que desea eliminar: ")

    if redis_client.exists(f"receta:{nombre}"):
        redis_client.delete(f"receta:{nombre}")
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")


# Función para ver un listado de recetas
def ver_listado_recetas():
    recetas = redis_client.keys("receta:*")

    if recetas:
        print("Listado de recetas:")
        for receta_key in recetas:
            receta = redis_client.hgetall(receta_key)
            print(
                f"Nombre: {receta[b'nombre'].decode()}, Ingredientes: {', '.join(receta[b'ingredientes'].decode().split(','))}, Pasos: {receta[b'pasos'].decode()}")
    else:
        print("No hay recetas en el libro.")


# Función principal
def menu_principal():
    while True:
        print("\n--- Menú ---")
        print("a) Agregar nueva receta")
        print("c) Actualizar receta existente")
        print("d) Eliminar receta existente")
        print("e) Ver listado de recetas")
        print("f) Salir")

        opcion = input("Ingrese la opción deseada: ").lower()

        if opcion == 'a':
            agregar_receta()
        elif opcion == 'c':
            actualizar_receta()
        elif opcion == 'd':
            eliminar_receta()
        elif opcion == 'e':
            ver_listado_recetas()
        elif opcion == 'f':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")


if __name__ == "__main__":
    menu_principal()
