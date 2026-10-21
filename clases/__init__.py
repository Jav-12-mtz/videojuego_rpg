"""
clases/__init__.py
==================
Paquete con la jerarquía de clases del Sistema de Personajes de Videojuego.

Reexporta las clases públicas para poder importarlas cómodamente:

    from clases import Guerrero, Mago, Arquero, Sanador
"""

from .personaje import Personaje
from .interfaces import (
    IAtacante, IDefensor, ICurable, IHabilidadEspecial,
)
from .mixins import LogMixin, InventarioMixin
from .clases_concretas import Guerrero, Mago, Arquero, Sanador

__all__ = [
    "Personaje",
    "IAtacante", "IDefensor", "ICurable", "IHabilidadEspecial",
    "LogMixin", "InventarioMixin",
    "Guerrero", "Mago", "Arquero", "Sanador",
]
