"""
clases/interfaces.py
====================
Interfaces del Sistema de Personajes de Videojuego.

En Python no existe la palabra reservada ``interface``; una interfaz se modela
como una **clase abstracta pura**: solo declara métodos abstractos (contratos)
y no aporta implementación ni estado.

Interfaces definidas:
  - IAtacante         -> contrato para atacar.
  - IDefensor         -> contrato para defender.
  - ICurable          -> contrato para curar y revivir aliados.
  - IHabilidadEspecial-> HERENCIA DE INTERFACES: deriva de IAtacante y añade
                         el contrato de las habilidades especiales.

Autor: Javier Martínez Andrade
Materia: Programación Orientada a Objetos (SCD-1020-2026B)
"""

from abc import ABC, abstractmethod


class IAtacante(ABC):
    """Interfaz: todo lo que puede atacar a un objetivo."""

    @abstractmethod
    def atacar(self, objetivo) -> None:
        """Realiza un ataque contra 'objetivo' (otro personaje)."""
        raise NotImplementedError


class IDefensor(ABC):
    """Interfaz: todo lo que puede defenderse y reportar su defensa."""

    @abstractmethod
    def defender(self) -> None:
        """Activa el modo defensa para el siguiente turno."""
        raise NotImplementedError

    @abstractmethod
    def obtener_defensa_total(self) -> int:
        """Devuelve la defensa efectiva del personaje."""
        raise NotImplementedError


class ICurable(ABC):
    """Interfaz: todo lo que puede sanar o revivir a un aliado."""

    @abstractmethod
    def curar_aliado(self, aliado, cantidad: int) -> None:
        """Restaura puntos de salud a 'aliado'."""
        raise NotImplementedError

    @abstractmethod
    def revivir(self, aliado) -> None:
        """Devuelve a la vida a un 'aliado' que haya caído."""
        raise NotImplementedError


class IHabilidadEspecial(IAtacante):
    """Interfaz DERIVADA (herencia de interfaces).

    Hereda de :class:`IAtacante`, por lo que toda clase que la implemente queda
    obligada también a cumplir el contrato de ``atacar()``. Sobre esa base
    añade el contrato propio de las habilidades especiales.
    """

    @abstractmethod
    def usar_habilidad_especial(self) -> None:
        """Ejecuta la habilidad especial característica de la clase."""
        raise NotImplementedError

    @abstractmethod
    def obtener_costo_habilidad(self) -> int:
        """Devuelve el costo (energía/maná) de la habilidad especial."""
        raise NotImplementedError
