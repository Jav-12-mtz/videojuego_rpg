"""
clases/personaje.py
===================
Clase abstracta base de la jerarquía de personajes.

Aplica los conceptos del Tema 4 (Unidad 4):
  - Clase abstracta: Personaje(ABC) no puede instanciarse.
  - Métodos abstractos: atacar(), usar_habilidad_especial(), obtener_clase().
  - Métodos concretos: comportamiento común a todos los personajes.
  - Polimorfismo: tomar_turno() permite que cada clase actúe a su manera.

Autor: Javier Martínez Andrade
Materia: Programación Orientada a Objetos (SCD-1020-2026B)
"""

import random
from abc import ABC, abstractmethod


class Personaje(ABC):
    """Clase base abstracta para cualquier personaje del videojuego.

    No puede instanciarse directamente: representa el concepto genérico de
    "personaje". Cobra vida a través de sus clases derivadas (Guerrero, Mago,
    Arquero, Sanador), que están obligadas a implementar los métodos abstractos.
    """

    def __init__(self, nombre: str, salud_maxima: int,
                 ataque_base: int, defensa_base: int):
        """Construye un personaje validando sus estadísticas.

        - nivel inicia en 1.
        - salud inicia a tope (salud == salud_maxima).
        - _defendiendo (protegido) inicia en False.
        - Valida que nombre no esté vacío y que las estadísticas sean positivas.
        """
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del personaje no puede estar vacío.")
        for etiqueta, valor in (("salud máxima", salud_maxima),
                                ("ataque base", ataque_base),
                                ("defensa base", defensa_base)):
            if not isinstance(valor, int) or valor <= 0:
                raise ValueError(f"La {etiqueta} debe ser un entero positivo.")

        self.nombre = nombre.strip()        # atributo público
        self.nivel = 1                      # atributo público (inicia en 1)
        self.salud_maxima = salud_maxima    # atributo público
        self.salud = salud_maxima           # atributo público (a tope)
        self.ataque_base = ataque_base      # atributo público
        self.defensa_base = defensa_base    # atributo público
        self._defendiendo = False           # atributo protegido

    # ------------------------------------------------------------------ #
    #  Métodos ABSTRACTOS (cada clase derivada DEBE implementarlos)        #
    # ------------------------------------------------------------------ #
    @abstractmethod
    def atacar(self, objetivo) -> None:
        """Cada clase define su propia forma de atacar (polimorfismo)."""
        raise NotImplementedError

    @abstractmethod
    def usar_habilidad_especial(self) -> None:
        """Cada clase tiene su habilidad especial característica."""
        raise NotImplementedError

    @abstractmethod
    def obtener_clase(self) -> str:
        """Devuelve el nombre de la clase ('Guerrero', 'Mago', ...)."""
        raise NotImplementedError

    # ------------------------------------------------------------------ #
    #  Métodos CONCRETOS (compartidos por todos los personajes)           #
    # ------------------------------------------------------------------ #
    def recibir_dano(self, cantidad: int, ignorar_defensa: bool = False) -> None:
        """Reduce la salud del personaje.

        Si el personaje está defendiendo, el daño se reduce a la mitad (salvo
        que el ataque ignore la defensa). El modo defensa se consume tras
        recibir el golpe.
        """
        dano = max(0, int(cantidad))
        if self._defendiendo and not ignorar_defensa:
            dano //= 2
            print(f"   🛡️  {self.nombre} se defiende y reduce el daño a la mitad.")
        self._defendiendo = False
        self.salud = max(0, self.salud - dano)
        print(f"   💥 {self.nombre} recibe {dano} de daño "
              f"(salud: {self.salud}/{self.salud_maxima}).")
        if not self.esta_vivo():
            print(f"   ☠️  ¡{self.nombre} ha caído en combate!")

    def defender(self) -> None:
        """Activa el modo defensa para el siguiente golpe recibido."""
        self._defendiendo = True
        print(f"🛡️  {self.nombre} se pone en guardia.")

    def curar(self, cantidad: int) -> None:
        """Aumenta la salud sin superar la salud máxima."""
        cantidad = max(0, int(cantidad))
        self.salud = min(self.salud_maxima, self.salud + cantidad)
        print(f"   ✨ {self.nombre} recupera {cantidad} de salud "
              f"(salud: {self.salud}/{self.salud_maxima}).")

    def subir_nivel(self) -> None:
        """Sube de nivel y mejora las estadísticas base."""
        self.nivel += 1
        self.salud_maxima += 15
        self.ataque_base += 5
        self.defensa_base += 3
        self.salud = self.salud_maxima      # se cura al subir de nivel
        print(f"⬆️  {self.nombre} sube al nivel {self.nivel} "
              f"(ataque {self.ataque_base}, defensa {self.defensa_base}).")

    def esta_vivo(self) -> bool:
        """True si al personaje le queda salud."""
        return self.salud > 0

    def mostrar_info(self) -> None:
        """Imprime la ficha con el estado actual del personaje."""
        estado = "VIVO" if self.esta_vivo() else "DERROTADO"
        print(f"  [{self.obtener_clase():<8}] {self.nombre:<12} "
              f"Nv.{self.nivel} | Salud {self.salud}/{self.salud_maxima} | "
              f"ATK {self.ataque_base} | DEF {self.defensa_base} | {estado}")

    def tomar_turno(self, aliados, enemigos) -> None:
        """Acción por defecto en una batalla: atacar a un enemigo al azar.

        Es un método concreto pensado para ser REDEFINIDO por las clases que
        actúan distinto (p. ej. el Sanador cura). La función batalla() lo invoca
        de forma polimórfica, sin preguntar el tipo del objeto.
        """
        vivos = [e for e in enemigos if e.esta_vivo()]
        if vivos:
            self.atacar(random.choice(vivos))

    def __str__(self) -> str:
        """Representación legible del personaje."""
        return (f"{self.obtener_clase()} {self.nombre} "
                f"(Nv.{self.nivel}, {self.salud}/{self.salud_maxima} HP)")
