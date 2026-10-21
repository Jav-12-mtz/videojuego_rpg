"""
clases/mixins.py
================
Mixins: funcionalidad transversal reutilizable mediante herencia múltiple.

Un *mixin* es una clase pequeña que NO está pensada para instanciarse por sí
sola, sino para "mezclarse" con otras y aportarles capacidades extra. Aquí se
añaden, sin tocar la jerarquía principal:

  - LogMixin        -> registro de acciones en consola.
  - InventarioMixin -> gestión de un inventario de objetos.

Autor: Javier Martínez Andrade
Materia: Programación Orientada a Objetos (SCD-1020-2026B)
"""


class LogMixin:
    """Añade la capacidad de registrar mensajes con el nombre de la clase."""

    def log(self, mensaje: str) -> None:
        """Imprime un mensaje anteponiendo el nombre de la clase concreta."""
        print(f"📜 [{type(self).__name__}] {mensaje}")


class InventarioMixin:
    """Añade un inventario sencillo de objetos (lista de ítems)."""

    def _asegurar_inventario(self) -> None:
        """Crea la lista de inventario la primera vez que se usa (lazy init)."""
        if not hasattr(self, "_inventario"):
            self._inventario = []

    def agregar_item(self, item: str) -> None:
        """Agrega un ítem al inventario."""
        self._asegurar_inventario()
        self._inventario.append(item)
        print(f"🎒 {getattr(self, 'nombre', 'El personaje')} guarda '{item}'.")

    def usar_item(self, item: str) -> bool:
        """Usa (y retira) un ítem del inventario. Devuelve True si lo tenía."""
        self._asegurar_inventario()
        if item in self._inventario:
            self._inventario.remove(item)
            print(f"🎒 {getattr(self, 'nombre', 'El personaje')} usa '{item}'.")
            return True
        print(f"🎒 '{item}' no está en el inventario.")
        return False

    def listar_inventario(self) -> None:
        """Muestra el contenido del inventario."""
        self._asegurar_inventario()
        if self._inventario:
            print(f"🎒 Inventario de {getattr(self, 'nombre', 'personaje')}: "
                  f"{', '.join(self._inventario)}.")
        else:
            print(f"🎒 {getattr(self, 'nombre', 'El personaje')} no lleva objetos.")
