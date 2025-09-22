#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archivo de Configuración para Ajedrez 960
Permite personalizar varios aspectos del juego
"""

# Configuración de la IA
CONFIG_IA = {
    # Profundidad de búsqueda para el algoritmo Minimax
    'profundidad_minimax': 3,
    
    # Tiempo máximo de reflexión para la IA (en segundos)
    'tiempo_maximo_ia': 5.0,
    
    # Valores de las piezas para evaluación
    'valores_piezas': {
        'K': 100,  # Rey
        'Q': 9,    # Reina
        'R': 5,    # Torre
        'B': 3,    # Alfil
        'N': 3,    # Caballo
        'P': 1,    # Peón
        'k': -100, 'q': -9, 'r': -5, 'b': -3, 'n': -3, 'p': -1
    },
    
    # Niveles de dificultad disponibles
    'niveles_dificultad': [
        "Principiante",
        "Normal", 
        "Experto"
    ],
    
    # Nivel por defecto
    'nivel_por_defecto': "Normal"
}

# Configuración de la interfaz gráfica
CONFIG_INTERFAZ = {
    # Tamaño de la ventana
    'ancho_ventana': 800,
    'alto_ventana': 700,
    
    # Tamaño del tablero
    'tamaño_casilla': 60,
    'ancho_tablero': 480,
    'alto_tablero': 480,
    
    # Colores del tablero
    'colores': {
        'casilla_clara': '#F0D9B5',
        'casilla_oscura': '#B58863',
        'casilla_seleccionada': '#FFD700',
        'casilla_posible': '#90EE90',
        'texto_principal': '#2C3E50',
        'texto_secundario': '#7F8C8D'
    },
    
    # Fuentes
    'fuentes': {
        'principal': ('Arial', 12, 'bold'),
        'secundaria': ('Arial', 10),
        'piezas': ('Arial', 24, 'bold'),
        'titulo': ('Arial', 18, 'bold')
    },
    
    # Símbolos Unicode para las piezas
    'simbolos_piezas': {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
    }
}

# Configuración del juego
CONFIG_JUEGO = {
    # Número de movimientos por jugador
    'movimientos_por_jugador': 20,
    
    # Reglas especiales
    'habilitar_enroque': False,  # En Ajedrez 960, el enroque es complejo
    'habilitar_captura_al_paso': True,
    'habilitar_promocion_peon': True,
    
    # Configuración de Ajedrez 960
    'verificar_rey_entre_torres': True,
    'generar_posicion_aleatoria': True,
    
    # Configuración de fin de juego
    'condiciones_empate': {
        'sin_movimientos': True,
        'repeticion_tres_veces': True,
        'regla_50_movimientos': False  # Opcional en Ajedrez 960
    }
}

# Configuración de debug y logging
CONFIG_DEBUG = {
    'habilitar_debug': False,
    'mostrar_movimientos_ia': False,
    'mostrar_evaluaciones': False,
    'guardar_historial': True,
    'nivel_log': 'INFO'  # DEBUG, INFO, WARNING, ERROR
}

# Configuración de rendimiento
CONFIG_RENDIMIENTO = {
    'usar_multiprocessing': False,  # Para IA más avanzada
    'cache_evaluaciones': True,
    'limitar_tiempo_ia': True,
    'optimizar_generacion_movimientos': True
}

def obtener_configuracion():
    """Retorna toda la configuración del juego"""
    return {
        'ia': CONFIG_IA,
        'interfaz': CONFIG_INTERFAZ,
        'juego': CONFIG_JUEGO,
        'debug': CONFIG_DEBUG,
        'rendimiento': CONFIG_RENDIMIENTO
    }

def actualizar_configuracion(seccion, clave, valor):
    """Actualiza una configuración específica"""
    configs = {
        'ia': CONFIG_IA,
        'interfaz': CONFIG_INTERFAZ,
        'juego': CONFIG_JUEGO,
        'debug': CONFIG_DEBUG,
        'rendimiento': CONFIG_RENDIMIENTO
    }
    
    if seccion in configs and clave in configs[seccion]:
        configs[seccion][clave] = valor
        return True
    return False

def obtener_valor(seccion, clave, valor_por_defecto=None):
    """Obtiene un valor de configuración específico"""
    configs = {
        'ia': CONFIG_IA,
        'interfaz': CONFIG_INTERFAZ,
        'juego': CONFIG_JUEGO,
        'debug': CONFIG_DEBUG,
        'rendimiento': CONFIG_RENDIMIENTO
    }
    
    if seccion in configs and clave in configs[seccion]:
        return configs[seccion][clave]
    return valor_por_defecto

# Ejemplo de uso
if __name__ == "__main__":
    print("Configuración del Ajedrez 960:")
    print("=" * 40)
    
    config = obtener_configuracion()
    
    print(f"Nivel por defecto: {config['ia']['nivel_por_defecto']}")
    print(f"Profundidad Minimax: {config['ia']['profundidad_minimax']}")
    print(f"Movimientos por jugador: {config['juego']['movimientos_por_jugador']}")
    print(f"Tamaño de ventana: {config['interfaz']['ancho_ventana']}x{config['interfaz']['alto_ventana']}")
    print(f"Debug habilitado: {config['debug']['habilitar_debug']}")
