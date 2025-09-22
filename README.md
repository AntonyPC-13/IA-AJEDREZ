# Ajedrez 960 - Humano vs Máquina curso de IA

## Descripción

Este proyecto implementa un juego completo de Ajedrez 960 (también conocido como Chess960 o Fischer Random Chess) donde un jugador humano compite contra una máquina con tres niveles diferentes de dificultad.

## Características Principales

### 🎯 Ajedrez 960
- **Posición inicial aleatoria**: Cada partida comienza con una disposición única de las piezas principales
- **Reglas estándar**: Mantiene todas las reglas del ajedrez tradicional
- **Rey entre torres**: El rey siempre está posicionado entre las dos torres (regla fundamental del Ajedrez 960)

### 🤖 Inteligencia Artificial
El sistema incluye tres niveles de dificultad:

1. **Principiante**: Selección aleatoria de movimientos
2. **Normal**: Algoritmo voraz que evalúa movimientos inmediatos
3. **Experto**: Algoritmo Minimax con poda Alfa-Beta para búsqueda profunda

### 🎮 Interfaz Gráfica
- **Interfaz intuitiva**: Diseño moderno y fácil de usar
- **Visualización clara**: Piezas Unicode y colores distintivos
- **Información en tiempo real**: Estado del juego, movimientos restantes, historial
- **Controles completos**: Nuevo juego, rendirse, cambio de dificultad

## Estructura del Proyecto

```
PROYECTO IA/
├── main.py              # Archivo principal para ejecutar el juego
├── ajedrez_960.py       # Lógica del juego y algoritmos de IA
├── interfaz_ajedrez.py  # Interfaz gráfica con Tkinter
└── README.md           # Este archivo
```

## Instalación y Ejecución

### Requisitos
- Python 3.7 o superior
- Tkinter (incluido con Python por defecto)

### Ejecutar el Juego
```bash
cd "PROYECTO IA"
python main.py
```

## Cómo Jugar

### Controles Básicos
1. **Seleccionar pieza**: Haz clic en una de tus piezas (letras minúsculas)
2. **Mover pieza**: Haz clic en una casilla verde (movimiento válido)
3. **Cancelar selección**: Haz clic en otra pieza o casilla vacía

### Niveles de Dificultad
- **Principiante**: Ideal para aprender las reglas
- **Normal**: Desafío moderado con evaluación táctica
- **Experto**: Desafío máximo con búsqueda profunda

### Información del Juego
- **Turno actual**: Indica si es tu turno o el de la máquina
- **Estado de los reyes**: Muestra si algún rey está en jaque
- **Movimientos restantes**: Contador de movimientos disponibles
- **Historial**: Lista de todos los movimientos realizados

## Algoritmos de IA Implementados

### 1. Nivel Principiante (Aleatorio)
```python
def movimiento_aleatorio(jugadas_posibles):
    return random.choice(jugadas_posibles)
```

### 2. Nivel Normal (Voraz)
- Evalúa cada movimiento posible
- Selecciona el que maximiza la evaluación inmediata
- Considera valores de piezas y posición

### 3. Nivel Experto (Minimax con Poda Alfa-Beta)
- Búsqueda profunda en el árbol de movimientos
- Optimización con poda Alfa-Beta
- Evaluación estratégica avanzada

## Estructura del Estado del Juego

### Tablero (T)
```python
tablero = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],  # Fila 1 (negro)
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],  # Fila 2 (negro)
    ['.', '.', '.', '.', '.', '.', '.', '.'],  # Fila 3
    ['.', '.', '.', '.', '.', '.', '.', '.'],  # Fila 4
    ['.', '.', '.', '.', '.', '.', '.', '.'],  # Fila 5
    ['.', '.', '.', '.', '.', '.', '.', '.'],  # Fila 6
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],  # Fila 7 (blanco)
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']   # Fila 8 (blanco)
]
```

### Variables de Estado
- `turno`: 'B' para Blanco (humano), 'N' para Negro (máquina)
- `movimientos_blanco`: Contador de movimientos restantes para el blanco
- `movimientos_negro`: Contador de movimientos restantes para el negro
- `rey_blanco_jaque`: Indica si el rey blanco está en jaque
- `rey_negro_jaque`: Indica si el rey negro está en jaque

## Condiciones de Victoria

### Victoria
- El oponente no tiene movimientos válidos
- El rey está en jaque y no puede escapar

### Empate
- Ambos jugadores se quedan sin movimientos válidos
- Se agotan los movimientos disponibles

## Características Técnicas

### Generación de Posiciones 960
- Algoritmo que garantiza posiciones válidas
- Verificación de la regla "rey entre torres"
- Distribución aleatoria de piezas principales

### Validación de Movimientos
- Verificación completa de reglas de ajedrez
- Detección de jaque y jaque mate
- Prevención de movimientos que dejan al rey en jaque

### Optimización de Rendimiento
- Poda Alfa-Beta para reducir exploración
- Evaluación eficiente de posiciones
- Generación inteligente de movimientos

## Personalización

### Modificar Dificultad
Puedes ajustar la profundidad de búsqueda en el algoritmo Minimax:
```python
# En ajedrez_960.py, línea del minimax_alfa_beta
return self.minimax_alfa_beta(movimientos_validos, profundidad=3)  # Cambiar profundidad
```

### Ajustar Valores de Piezas
```python
# En ajedrez_960.py
self.valores_piezas = {
    'K': 100, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1,
    'k': -100, 'q': -9, 'r': -5, 'b': -3, 'n': -3, 'p': -1
}
```

## Solución de Problemas

### Error de Importación
Si tienes problemas con las importaciones, asegúrate de que todos los archivos estén en el mismo directorio.

### Problemas de Rendimiento
- Reduce la profundidad del Minimax en niveles altos
- El nivel Experto puede ser lento en computadoras menos potentes

### Problemas Visuales
- Asegúrate de que tu sistema soporte caracteres Unicode
- Verifica que Tkinter esté instalado correctamente

## Contribuciones

Este proyecto está diseñado para ser educativo y extensible. Puedes:
- Añadir nuevos niveles de dificultad
- Implementar algoritmos de IA más avanzados
- Mejorar la interfaz gráfica
- Añadir características como guardar/cargar partidas

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

---

¡Disfruta jugando Ajedrez 960! 🎮♟️

