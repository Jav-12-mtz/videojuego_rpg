"""
clases/clases_concretas.py
===========================
Clases concretas del videojuego: Guerrero, Mago, Arquero y Sanador.

Cada una combina, mediante HERENCIA MÚLTIPLE:
  - La clase abstracta  Personaje        (estado y comportamiento común).
  - Las interfaces       I...             (contratos que cumple).
  - Los mixins           LogMixin,
                         InventarioMixin  (funcionalidad transversal).

Como IHabilidadEspecial deriva de IAtacante, toda clase que implemente
IHabilidadEspecial cumple también el contrato de IAtacante; por eso no se
vuelve a listar IAtacante en la herencia (se evita así un conflicto de MRO).

Autor: Javier Martínez Andrade
Materia: Programación Orientada a Objetos (SCD-1020-2026B)
"""

import random

from .personaje import Personaje
from .interfaces import IDefensor, ICurable, IHabilidadEspecial
from .mixins import LogMixin, InventarioMixin


# ====================================================================== #
#  GUERRERO                                                              #
# ====================================================================== #
class Guerrero(Personaje, IDefensor, IHabilidadEspecial,
               LogMixin, InventarioMixin):
    """Alto ataque y defensa, poca salud. Especialista en combate cuerpo a cuerpo."""

    def obtener_clase(self) -> str:
        return "Guerrero"

    def atacar(self, objetivo) -> None:
        factor = 2 if getattr(self, "_golpe_aplastante", False) else 1
        dano = int(self.ataque_base * 1.5 * factor)
        self._golpe_aplastante = False          # se consume el efecto
        self._guardia_baja = False
        extra = " con un GOLPE APLASTANTE" if factor == 2 else ""
        self.log(f"⚔️ ataca a {objetivo.nombre}{extra} ({dano} de daño).")
        objetivo.recibir_dano(dano)

    def usar_habilidad_especial(self) -> None:
        self._golpe_aplastante = True           # el próximo ataque hace daño doble
        self._guardia_baja = True               # pero baja la guardia un turno
        self.log("💢 prepara un GOLPE APLASTANTE: su próximo ataque hará daño "
                 "doble, pero su defensa baja por un turno.")

    def obtener_costo_habilidad(self) -> int:
        return 20

    def obtener_defensa_total(self) -> int:
        defensa = self.defensa_base
        if self._defendiendo:
            defensa *= 2
        if getattr(self, "_guardia_baja", False):
            defensa //= 2
        return defensa


# ====================================================================== #
#  MAGO                                                                  #
# ====================================================================== #
class Mago(Personaje, ICurable, IHabilidadEspecial,
           LogMixin, InventarioMixin):
    """Ataque mágico potente que ignora la defensa, salud baja; puede curar."""

    def obtener_clase(self) -> str:
        return "Mago"

    def atacar(self, objetivo) -> None:
        factor = 1.5 if getattr(self, "_bola_fuego", False) else 1.0
        dano = int(self.ataque_base * 2.0 * factor)
        self._bola_fuego = False
        extra = " (BOLA DE FUEGO en área)" if factor != 1.0 else ""
        self.log(f"🔥 lanza un hechizo contra {objetivo.nombre}{extra} "
                 f"({dano} de daño, ignora la defensa).")
        objetivo.recibir_dano(dano, ignorar_defensa=True)

    def curar_aliado(self, aliado, cantidad: int) -> None:
        self.log(f"✨ conjura un hechizo de sanación sobre {aliado.nombre}.")
        aliado.curar(cantidad)

    def revivir(self, aliado) -> None:
        if aliado.esta_vivo():
            self.log(f"{aliado.nombre} sigue con vida; no hace falta revivirlo.")
            return
        aliado.salud = max(1, aliado.salud_maxima // 2)
        self.log(f"🪄 revive a {aliado.nombre} con media salud.")

    def usar_habilidad_especial(self) -> None:
        self._bola_fuego = True                 # potencia el próximo ataque
        self.log("🔥 canaliza una BOLA DE FUEGO: su próximo hechizo hará daño "
                 "en área.")

    def obtener_costo_habilidad(self) -> int:
        return 30

    def tomar_turno(self, aliados, enemigos) -> None:
        """El Mago cura a un aliado muy herido; si no, ataca (polimorfismo)."""
        heridos = [a for a in aliados
                   if a is not self and a.esta_vivo()
                   and a.salud < a.salud_maxima * 0.4]
        if heridos and random.random() < 0.5:
            objetivo = min(heridos, key=lambda a: a.salud)
            self.curar_aliado(objetivo, 25)
        else:
            super().tomar_turno(aliados, enemigos)


# ====================================================================== #
#  ARQUERO                                                               #
# ====================================================================== #
class Arquero(Personaje, IHabilidadEspecial, LogMixin, InventarioMixin):
    """Alto ataque a distancia, defensa baja, salud media; golpes críticos."""

    def obtener_clase(self) -> str:
        return "Arquero"

    def atacar(self, objetivo) -> None:
        # Un arquero ignora parte de la defensa gracias a su precisión.
        critico = getattr(self, "_critico_garantizado", False) or random.random() < 0.25
        dano = int(self.ataque_base * 1.2)
        if critico:
            dano *= 2
            self._critico_garantizado = False
            self.log(f"🏹 dispara una FLECHA CERTERA a {objetivo.nombre}: "
                     f"¡CRÍTICO! ({dano} de daño).")
        else:
            self.log(f"🏹 dispara una flecha a {objetivo.nombre} ({dano} de daño).")
        objetivo.recibir_dano(dano)

    def usar_habilidad_especial(self) -> None:
        self._critico_garantizado = True        # asegura el próximo crítico
        self.log("🎯 apunta con una FLECHA CERTERA: su próximo disparo será crítico.")

    def obtener_costo_habilidad(self) -> int:
        return 15


# ====================================================================== #
#  SANADOR                                                               #
# ====================================================================== #
class Sanador(Personaje, ICurable, IDefensor, IHabilidadEspecial,
              LogMixin, InventarioMixin):
    """Ataque bajo, defensa media, salud alta; el mejor apoyo del equipo."""

    def obtener_clase(self) -> str:
        return "Sanador"

    def atacar(self, objetivo) -> None:
        dano = max(1, int(self.ataque_base * 0.8))
        self.log(f"🔨 golpea con su báculo a {objetivo.nombre} ({dano} de daño).")
        objetivo.recibir_dano(dano)

    def curar_aliado(self, aliado, cantidad: int) -> None:
        self.log(f"💚 lanza un poderoso hechizo de curación sobre {aliado.nombre}.")
        aliado.curar(cantidad)

    def revivir(self, aliado) -> None:
        if aliado.esta_vivo():
            self.log(f"{aliado.nombre} sigue con vida; no hace falta revivirlo.")
            return
        aliado.salud = aliado.salud_maxima
        self.log(f"🙏 revive a {aliado.nombre} con toda su salud.")

    def usar_habilidad_especial(self) -> None:
        self.log("🌟 invoca una BENDICIÓN que reconforta y sana a los aliados.")
        self.curar(30)                          # al menos se sana a sí mismo

    def obtener_costo_habilidad(self) -> int:
        return 25

    def obtener_defensa_total(self) -> int:
        return self.defensa_base * (2 if self._defendiendo else 1)

    def tomar_turno(self, aliados, enemigos) -> None:
        """El Sanador revive, cura al más herido o, si no, ataca (polimorfismo)."""
        muertos = [a for a in aliados if a is not self and not a.esta_vivo()]
        heridos = [a for a in aliados
                   if a.esta_vivo() and a.salud < a.salud_maxima * 0.6]
        if muertos:
            self.revivir(muertos[0])
        elif heridos:
            objetivo = min(heridos, key=lambda a: a.salud)
            self.curar_aliado(objetivo, 30)
        else:
            super().tomar_turno(aliados, enemigos)
