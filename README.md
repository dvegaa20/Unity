# Unity

Repositorio colaborativo para la realización del proyecto de la materia Modelación de sistemas multiagentes con gráficas computacionales (Ago-Dic, 2023)

## Autores

- [@dembA7](https://github.com/dembA7)
- [@Riosmena](https://github.com/Riosmena)
- [@dvegaa20](https://github.com/dvegaa20)

## Descripción de la evidencia

### Descripción
El reto consiste en desarrollar un sistema multiagente para resolver una tarea cooperativa en un entorno 20x20 dinámicamente cambiante. El entorno del sistema multiagente es un mundo similar a una cuadrícula donde los agentes pueden moverse de su posición a una celda vecina si ya no hay ningún agente en esa ranura. En este entorno, la comida puede aparecer en cualquier celda menos en una. La celda especial, en la que no puede aparecer comida, se considera un depósito donde los agentes pueden traer y almacenar su comida. Un agente puede sólo puede saber si hay comida en una celda, si está visitándola. Inicialmente, la comida se coloca en algunas celdas aleatorias. Durante la ejecución, puede aparecer comida adicional dinámicamente en celdas seleccionadas al azar, excepto en la celda del depósito. Los agentes pueden tener/desempeñar diferentes roles (como explorador o recolector), comunicarse y cooperar para encontrar y recolectar alimentos de manera eficiente y efectiva.

### Puntos a considerar
- Inicialmente no hay comida en el entorno.
- La semilla para generación de números aleatorios será 12345.
- El depósito será generado al azar.
- Cada 5 segundos se colocará una unidad de comida en algunas celdas.
- La cantidad de celdas en las que colocará una unidad comida será definida al azar (entre 2 y 5 celdas).
- Se colocará un total de 47 unidades de comida.
- Número total de pasos (steps): 1500.
- La cantidad total de alimentos que se puede almacenar en el depósito es infinito.
- Hay un total de 5 agentes.
- Cuando una unidad de comida es encontrado por un explorador o por un agente que ya lleva la comida, la posición de la comida se marca y se comunica a otros agentes.
- Cuando un recolector encuentra una unidad comida, lo carga (gráficamente deberá cambia su forma para indicar que lleva comida). La capacidad máxima de comida que puede llevar un agentes es UNA unidad de comida.
- Inicialmente, los agentes no son informados sobre la posición del depósito, pero una vez que lo encuentran, todos saben dónde está.

### Criterios de evaluación
Los criterios que se utilizarán para evaluar sus soluciones y seleccionar a los tres primeros ganadores son los siguientes:
- Aplicación original, innovadora y efectiva de algoritmos computacionales para resolver problemas específicos.
- El rendimiento de la implementación. El rendimiento de la implementación ejecutable se medirá en función de la cantidad de alimentos que recolecte el sistema multiagente en una cantidad de pasos de simulación.
- La calidad de la descripción de análisis, diseño e implementación del sistema multiagente, la elegancia de su diseño e implementación.

## Documentation

[Documentation](https://linktodocumentation)


