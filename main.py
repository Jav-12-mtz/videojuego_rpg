"""
main.py
=======
Programa principal del Sistema de Personajes de Videojuego (RPG por turnos).

Incluye:
  - La función POLIMÓRFICA batalla(): simula un combate por turnos entre dos
    equipos sin usar condicionales de tipo (sin isinstance). Cada personaje
    responde al mensaje tomar_turno() según su propia clase.
  - Un menú interactivo para crear personajes, verlos, simular batallas y
    consultar estadísticas, con validaciones y manejo de errores.

Autor: Javier Martínez Andrade
Materia: Programación Orientada a Objetos (SCD-1020-2026B)
"""

import random
import sys

# Asegura que la consola pueda imprimir los emojis (UTF-8) en cualquier sistema.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from clases import Guerrero, Mago, Arquero, Sanador


# Tipos de personaje disponibles y las estadísticas base sugeridas para cada uno
# (salud_maxima, ataque_base, defensa_base). El usuario puede modificarlas.
TIPOS = {
    "1": ("Guerrero", Guerrero, (120, 25, 20)),
    "2": ("Mago",     Mago,     (80,  30, 8)),
    "3": ("Arquero",  Arquero,  (100, 28, 10)),
    "4": ("Sanador",  Sanador,  (140, 12, 15)),
}


# ====================================================================== #
#  FUNCIÓN POLIMÓRFICA: batalla()                                        #
# ====================================================================== #
def batalla(equipo1, equipo2, max_turnos: int = 50) -> None:
    """Simula una batalla por turnos entre dos equipos (polimorfismo puro).

    No usa condicionales de tipo (isinstance): a cada personaje se le envía el
    mismo mensaje, ``tomar_turno()``, y cada clase decide qué hacer (atacar,
    curar, revivir...) según su propia implementación.
    """
    print("\n" + "=" * 55)
    print("⚔️  ¡COMIENZA LA BATALLA!")
    print("=" * 55)

    turno = 1
    while (any(p.esta_vivo() for p in equipo1)
           and any(p.esta_vivo() for p in equipo2)
           and turno <= max_turnos):
        print(f"\n{'=' * 55}")
        print(f"⚔️  TURNO {turno}")
        print(f"{'=' * 55}")

        # Turno del equipo 1
        for personaje in equipo1:
            if personaje.esta_vivo() and any(e.esta_vivo() for e in equipo2):
                personaje.tomar_turno(equipo1, equipo2)

        # Turno del equipo 2
        for personaje in equipo2:
            if personaje.esta_vivo() and any(e.esta_vivo() for e in equipo1):
                personaje.tomar_turno(equipo2, equipo1)

        turno += 1

    # Determinar el resultado de la batalla
    print(f"\n{'=' * 55}")
    vivos1 = any(p.esta_vivo() for p in equipo1)
    vivos2 = any(p.esta_vivo() for p in equipo2)
    if vivos1 and not vivos2:
        print("🏆 ¡EQUIPO 1 GANA!")
    elif vivos2 and not vivos1:
        print("🏆 ¡EQUIPO 2 GANA!")
    else:
        print("🤝 La batalla termina en empate (se alcanzó el límite de turnos).")
    print("=" * 55)


# ====================================================================== #
#  UTILIDADES DE ENTRADA (con validación y manejo de errores)            #
# ====================================================================== #
def leer_texto(mensaje: str) -> str:
    """Lee una cadena no vacía."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  ⚠️  El valor no puede estar vacío. Inténtalo de nuevo.")


def leer_entero(mensaje: str, minimo: int = 1, maximo: int = None) -> int:
    """Lee un entero dentro del rango [minimo, maximo]."""
    while True:
        try:
            valor = int(input(mensaje).strip())
        except ValueError:
            print("  ⚠️  Debes escribir un número entero.")
            continue
        if valor < minimo:
            print(f"  ⚠️  El valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"  ⚠️  El valor debe ser menor o igual a {maximo}.")
        else:
            return valor


# ====================================================================== #
#  OPCIONES DEL MENÚ                                                      #
# ====================================================================== #
def crear_personaje(personajes: list) -> None:
    """Opción 1: crea un personaje del tipo elegido y lo agrega a la lista."""
    print("\n── Crear personaje ──")
    for clave, (nombre, _clase, stats) in TIPOS.items():
        print(f"  {clave}) {nombre:<9} (sugerido  "
              f"salud {stats[0]}, ataque {stats[1]}, defensa {stats[2]})")

    opcion = leer_texto("  Elige el tipo (1-4): ")
    if opcion not in TIPOS:
        print("  ⚠️  Tipo no válido. Debe ser 1, 2, 3 o 4.")
        return

    nombre_tipo, clase, (s_def, a_def, d_def) = TIPOS[opcion]
    nombre = leer_texto("  Nombre del personaje: ")
    print("  Introduce las estadísticas base (números positivos):")
    salud = leer_entero(f"    Salud máxima [{s_def}]: ")
    ataque = leer_entero(f"    Ataque base  [{a_def}]: ")
    defensa = leer_entero(f"    Defensa base [{d_def}]: ")

    try:
        personaje = clase(nombre, salud, ataque, defensa)
    except ValueError as error:
        print(f"  ⚠️  No se pudo crear el personaje: {error}")
        return

    personaje.agregar_item("Poción de vida")   # demuestra el InventarioMixin
    personajes.append(personaje)
    print(f"  ✅ {nombre_tipo} '{nombre}' creado con éxito.")


def ver_personajes(personajes: list) -> None:
    """Opción 2: muestra todos los personajes creados."""
    print("\n── Personajes creados ──")
    if not personajes:
        print("  (Todavía no hay personajes. Usa la opción 1 para crear uno.)")
        return
    for personaje in personajes:
        personaje.mostrar_info()


def simular_batalla(personajes: list) -> None:
    """Opción 3: arma dos equipos aleatorios y simula la batalla."""
    print("\n── Simular batalla ──")
    if len(personajes) < 2:
        print("  ⚠️  Necesitas al menos 2 personajes. Crea más con la opción 1.")
        return

    maximo_por_equipo = len(personajes) // 2
    n = leer_entero(f"  ¿Cuántos personajes por equipo? (1-{maximo_por_equipo}): ",
                    minimo=1, maximo=maximo_por_equipo)

    seleccionados = random.sample(personajes, 2 * n)
    equipo1 = seleccionados[:n]
    equipo2 = seleccionados[n:]

    print("\n  EQUIPO 1:", ", ".join(str(p) for p in equipo1))
    print("  EQUIPO 2:", ", ".join(str(p) for p in equipo2))

    # Se restaura la salud de los combatientes antes de pelear.
    for personaje in equipo1 + equipo2:
        personaje.salud = personaje.salud_maxima

    batalla(equipo1, equipo2)


def ver_estadisticas(personajes: list) -> None:
    """Opción 4: cuenta cuántos personajes hay de cada tipo."""
    print("\n── Estadísticas ──")
    if not personajes:
        print("  (No hay personajes registrados.)")
        return
    conteo = {}
    for personaje in personajes:
        clase = personaje.obtener_clase()
        conteo[clase] = conteo.get(clase, 0) + 1
    for nombre_tipo, _clase, _stats in TIPOS.values():
        print(f"  {nombre_tipo:<9}: {conteo.get(nombre_tipo, 0)}")
    print(f"  {'TOTAL':<9}: {len(personajes)}")


# ====================================================================== #
#  PROGRAMA PRINCIPAL                                                     #
# ====================================================================== #
def main() -> None:
    print("╔" + "═" * 50 + "╗")
    print("║" + "SISTEMA DE PERSONAJES DE VIDEOJUEGO (RPG)".center(50) + "║")
    print("╚" + "═" * 50 + "╝")

    personajes = []
    opciones = {
        "1": crear_personaje,
        "2": ver_personajes,
        "3": simular_batalla,
        "4": ver_estadisticas,
    }

    while True:
        print("\n──────────── MENÚ ────────────")
        print("  1) Crear personaje")
        print("  2) Ver personajes")
        print("  3) Simular batalla")
        print("  4) Ver estadísticas")
        print("  5) Salir")
        opcion = input("  Elige una opción (1-5): ").strip()

        if opcion == "5":
            print("\n¡Gracias por jugar! Hasta la próxima aventura. ⚔️🎮")
            break
        accion = opciones.get(opcion)
        if accion is None:
            print("  ⚠️  Opción no válida. Escribe un número del 1 al 5.")
            continue
        try:
            accion(personajes)
        except Exception as error:          # red de seguridad del menú
            print(f"  ⚠️  Ocurrió un error inesperado: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario. ¡Vuelve pronto!")
