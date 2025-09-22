#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo del Sistema de Ajedrez 960
Muestra las capacidades de la IA en diferentes niveles
"""

from ajedrez_960 import Ajedrez960
import time

def demo_generacion_posiciones():
    """Demuestra la generación de posiciones 960"""
    print("=" * 60)
    print("DEMO: Generación de Posiciones Ajedrez 960")
    print("=" * 60)
    
    juego = Ajedrez960()
    
    print("Posición inicial generada:")
    print_tablero(juego.tablero)
    print()
    
    # Generar algunas posiciones más
    print("Generando 3 posiciones adicionales...")
    for i in range(3):
        juego.resetear_juego()
        print(f"\nPosición {i+2}:")
        print_tablero(juego.tablero)

def demo_niveles_ia():
    """Demuestra los diferentes niveles de IA"""
    print("\n" + "=" * 60)
    print("DEMO: Niveles de Inteligencia Artificial")
    print("=" * 60)
    
    juego = Ajedrez960()
    niveles = ["Principiante", "Normal", "Experto"]
    
    for nivel in niveles:
        print(f"\n--- Nivel: {nivel} ---")
        
        # Obtener movimientos válidos
        movimientos = juego.obtener_todos_movimientos_validos()
        print(f"Movimientos válidos disponibles: {len(movimientos)}")
        
        if movimientos:
            # Obtener mejor movimiento según el nivel
            inicio = time.time()
            mejor_movimiento = juego.obtener_mejor_movimiento_ia(nivel)
            tiempo = time.time() - inicio
            
            if mejor_movimiento:
                fila_origen, col_origen, fila_destino, col_destino = mejor_movimiento
                pieza = juego.tablero[fila_origen][col_origen]
                print(f"Mejor movimiento: {pieza} desde ({fila_origen},{col_origen}) a ({fila_destino},{col_destino})")
                print(f"Tiempo de decisión: {tiempo:.3f} segundos")
                
                # Evaluar la posición
                evaluacion = juego.evaluar_tablero()
                print(f"Evaluación de la posición: {evaluacion}")

def demo_validacion_movimientos():
    """Demuestra la validación de movimientos"""
    print("\n" + "=" * 60)
    print("DEMO: Validación de Movimientos")
    print("=" * 60)
    
    juego = Ajedrez960()
    
    print("Posición inicial:")
    print_tablero(juego.tablero)
    print(f"Turno actual: {'Blanco' if juego.turno == 'B' else 'Negro'}")
    
    # Mostrar movimientos válidos para algunas piezas
    print("\nMovimientos válidos para piezas blancas:")
    for i in range(8):
        for j in range(8):
            if juego.tablero[i][j] != '.' and juego.tablero[i][j].islower():
                movimientos = juego.obtener_movimientos_validos(i, j)
                if movimientos:
                    pieza = juego.tablero[i][j]
                    print(f"{pieza.upper()} en ({i},{j}): {len(movimientos)} movimientos")

def demo_estado_juego():
    """Demuestra el estado del juego"""
    print("\n" + "=" * 60)
    print("DEMO: Estado del Juego")
    print("=" * 60)
    
    juego = Ajedrez960()
    
    print("Estado inicial del juego:")
    print(f"- Turno: {'Blanco (Humano)' if juego.turno == 'B' else 'Negro (Máquina)'}")
    print(f"- Movimientos restantes Blanco: {juego.movimientos_blanco}")
    print(f"- Movimientos restantes Negro: {juego.movimientos_negro}")
    print(f"- Rey Blanco en jaque: {juego.rey_blanco_jaque}")
    print(f"- Rey Negro en jaque: {juego.rey_negro_jaque}")
    print(f"- Juego terminado: {juego.juego_terminado}")
    print(f"- Resultado: {juego.resultado or 'En progreso'}")

def print_tablero(tablero):
    """Imprime el tablero en formato legible"""
    print("   a b c d e f g h")
    for i, fila in enumerate(tablero):
        print(f"{8-i}  ", end="")
        for pieza in fila:
            if pieza == '.':
                print("· ", end="")
            else:
                print(f"{pieza} ", end="")
        print(f" {8-i}")
    print("   a b c d e f g h")

def main():
    """Función principal del demo"""
    print("DEMO DEL SISTEMA DE AJEDREZ 960")
    print("Este demo muestra las capacidades del sistema implementado")
    print()
    
    try:
        # Ejecutar demos
        demo_generacion_posiciones()
        demo_niveles_ia()
        demo_validacion_movimientos()
        demo_estado_juego()
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETADO")
        print("=" * 60)
        print("Para jugar el juego completo, ejecuta: python main.py")
        
    except Exception as e:
        print(f"Error durante el demo: {e}")

if __name__ == "__main__":
    main()
