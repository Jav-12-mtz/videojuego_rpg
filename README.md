# Sistema de Personajes de Videojuego (RPG)

Actividad 2 — Unidad 4 de **Programación Orientada a Objetos** (SCD-1020-2026B).

Sistema de un videojuego de rol por turnos que aplica **clases abstractas**,
**métodos abstractos**, **interfaces**, **herencia de interfaces**, **mixins**
(herencia múltiple) y **polimorfismo**. Existe una clase abstracta `Personaje`
y cuatro clases concretas (`Guerrero`, `Mago`, `Arquero`, `Sanador`) que combinan
distintas interfaces y mixins. La batalla se simula con una función **100 %
polimórfica** (sin `isinstance`).

## Estructura del proyecto

```
videojuego_rpg/
│
├── main.py                 # Menú interactivo + función polimórfica batalla()
└── clases/
    ├── __init__.py         # Reexporta las clases públicas del paquete
    ├── personaje.py        # Clase abstracta Personaje
    ├── interfaces.py       # IAtacante, IDefensor, ICurable, IHabilidadEspecial
    ├── mixins.py           # LogMixin, InventarioMixin
    └── clases_concretas.py # Guerrero, Mago, Arquero, Sanador
```

## Cómo ejecutarlo

Requiere **Python 3.10+**. Desde la carpeta `videojuego_rpg/`:

```bash
python main.py
```

El menú permite **crear personajes** (Guerrero, Mago, Arquero, Sanador),
**verlos**, **simular una batalla** por turnos entre dos equipos y **consultar
estadísticas**.

## Conceptos de POO aplicados

| Concepto | Dónde se aplica |
|---|---|
| **Clase abstracta** | `Personaje(ABC)` no puede instanciarse |
| **Métodos abstractos** | `atacar()`, `usar_habilidad_especial()`, `obtener_clase()` |
| **Métodos concretos** | `recibir_dano()`, `defender()`, `curar()`, `subir_nivel()`, `esta_vivo()`, `__str__()` |
| **Interfaces** | `IAtacante`, `IDefensor`, `ICurable`, `IHabilidadEspecial` (clases abstractas puras) |
| **Herencia de interfaces** | `IHabilidadEspecial` deriva de `IAtacante` |
| **Herencia múltiple** | cada clase concreta hereda de `Personaje` + interfaces + mixins |
| **Mixins** | `LogMixin` (log) e `InventarioMixin` (inventario) en todas las clases concretas |
| **Polimorfismo puro** | `batalla()` invoca `tomar_turno()` sin usar `isinstance` |
| **Manejo de errores** | validaciones con `try/except` y re-intentos en el menú |
| **Diseño extensible** | añadir un nuevo tipo de personaje no obliga a modificar el código existente |

## Autor

Javier Martínez Andrade — Ingeniería en Sistemas Computacionales (TecNM, modalidad a distancia).
