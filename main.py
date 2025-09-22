#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajedrez 960 - Humano vs Máquina
Implementación completa con tres niveles de dificultad de IA

Autor: Sistema de IA
Fecha: 2024
"""

import sys
import os
from interfaz_ajedrez import InterfazAjedrez

def main():
    """Función principal del programa"""
    try:
        print("Iniciando Ajedrez 960...")
        print("=" * 50)
        print("Bienvenido al Ajedrez 960 - Humano vs Máquina")
        print("=" * 50)
        print()
        print("Instrucciones:")
        print("- Eres las piezas blancas (minúsculas)")
        print("- La máquina juega con las piezas negras (mayúsculas)")
        print("- Haz clic en una pieza para seleccionarla")
        print("- Haz clic en una casilla verde para mover")
        print("- Puedes cambiar la dificultad en cualquier momento")
        print("- ¡Buena suerte!")
        print()
        
        # Crear y ejecutar la interfaz
        app = InterfazAjedrez()
        app.ejecutar()
        
    except Exception as e:
        print(f"Error al ejecutar el programa: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
