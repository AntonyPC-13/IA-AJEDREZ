import tkinter as tk
from tkinter import messagebox, ttk
import random
import copy
from typing import List, Tuple, Optional

class Ajedrez960:
    def __init__(self):
        # Valores de las piezas para evaluación
        self.valores_piezas = {
            'K': 100, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1,
            'k': -100, 'q': -9, 'r': -5, 'b': -3, 'n': -3, 'p': -1
        }
        
        # Inicializar el estado del juego
        self.resetear_juego()
        
    def resetear_juego(self):
        """Inicializa un nuevo juego de Ajedrez 960"""
        # Generar posición inicial aleatoria para Ajedrez 960
        self.tablero = self.generar_posicion_960()
        
        # Estado del juego
        self.turno = 'B'  # B para Blanco (humano), N para Negro (máquina)
        self.movimientos_blanco = 20
        self.movimientos_negro = 20
        self.rey_blanco_jaque = False
        self.rey_negro_jaque = False
        self.rey_blanco_destino = False
        self.rey_negro_destino = False
        self.historial_movimientos = []
        self.juego_terminado = False
        self.resultado = None
        
    def generar_posicion_960(self):
        """Genera una posición inicial aleatoria válida para Ajedrez 960"""
        # Crear tablero vacío
        tablero = [['.' for _ in range(8)] for _ in range(8)]
        
        # Colocar peones
        for i in range(8):
            tablero[1][i] = 'P'  # Peones negros
            tablero[6][i] = 'p'  # Peones blancos
        
        # Generar posición aleatoria para las piezas principales
        piezas_principales = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        random.shuffle(piezas_principales)
        
        # Asegurar que el rey esté entre las torres (regla de Ajedrez 960)
        while True:
            pos_rey = piezas_principales.index('K')
            pos_torres = [i for i, pieza in enumerate(piezas_principales) if pieza == 'R']
            if pos_torres[0] < pos_rey < pos_torres[1]:
                break
            random.shuffle(piezas_principales)
        
        # Colocar las piezas principales
        for i, pieza in enumerate(piezas_principales):
            tablero[0][i] = pieza  # Fila de piezas negras
            tablero[7][i] = pieza.lower()  # Fila de piezas blancas
        
        return tablero
    
    def obtener_movimientos_validos(self, fila: int, col: int) -> List[Tuple[int, int]]:
        """Obtiene todos los movimientos válidos para una pieza en la posición dada"""
        if self.tablero[fila][col] == '.':
            return []
        
        pieza = self.tablero[fila][col]
        movimientos = []
        
        # Determinar si es pieza blanca o negra
        es_blanca = pieza.islower()
        es_negro = pieza.isupper()
        
        # Verificar que sea el turno correcto
        if (es_blanca and self.turno != 'B') or (es_negro and self.turno != 'N'):
            return []
        
        pieza_tipo = pieza.upper()
        
        if pieza_tipo == 'P':  # Peón
            movimientos = self.movimientos_peon(fila, col, es_blanca)
        elif pieza_tipo == 'R':  # Torre
            movimientos = self.movimientos_torre(fila, col)
        elif pieza_tipo == 'N':  # Caballo
            movimientos = self.movimientos_caballo(fila, col)
        elif pieza_tipo == 'B':  # Alfil
            movimientos = self.movimientos_alfil(fila, col)
        elif pieza_tipo == 'Q':  # Reina
            movimientos = self.movimientos_reina(fila, col)
        elif pieza_tipo == 'K':  # Rey
            movimientos = self.movimientos_rey(fila, col)
        
        # Filtrar movimientos que dejan al rey en jaque
        movimientos_validos = []
        for mov_fila, mov_col in movimientos:
            if self.es_movimiento_seguro(fila, col, mov_fila, mov_col):
                movimientos_validos.append((mov_fila, mov_col))
        
        return movimientos_validos
    
    def movimientos_peon(self, fila: int, col: int, es_blanca: bool) -> List[Tuple[int, int]]:
        """Calcula los movimientos válidos para un peón"""
        movimientos = []
        direccion = -1 if es_blanca else 1
        fila_inicial = 6 if es_blanca else 1
        
        # Movimiento hacia adelante
        nueva_fila = fila + direccion
        if 0 <= nueva_fila <= 7 and self.tablero[nueva_fila][col] == '.':
            movimientos.append((nueva_fila, col))
            
            # Movimiento doble desde la posición inicial
            if fila == fila_inicial:
                nueva_fila = fila + 2 * direccion
                if 0 <= nueva_fila <= 7 and self.tablero[nueva_fila][col] == '.':
                    movimientos.append((nueva_fila, col))
        
        # Capturas diagonales
        for dc in [-1, 1]:
            nueva_col = col + dc
            if 0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7:
                pieza_destino = self.tablero[nueva_fila][nueva_col]
                if pieza_destino != '.' and ((es_blanca and pieza_destino.isupper()) or 
                                           (not es_blanca and pieza_destino.islower())):
                    movimientos.append((nueva_fila, nueva_col))
        
        return movimientos
    
    def movimientos_torre(self, fila: int, col: int) -> List[Tuple[int, int]]:
        """Calcula los movimientos válidos para una torre"""
        movimientos = []
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for df, dc in direcciones:
            for i in range(1, 8):
                nueva_fila, nueva_col = fila + i * df, col + i * dc
                if not (0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7):
                    break
                
                pieza_destino = self.tablero[nueva_fila][nueva_col]
                if pieza_destino == '.':
                    movimientos.append((nueva_fila, nueva_col))
                else:
                    # Puede capturar pieza enemiga
                    if self.es_pieza_enemiga(self.tablero[fila][col], pieza_destino):
                        movimientos.append((nueva_fila, nueva_col))
                    break
        
        return movimientos
    
    def movimientos_caballo(self, fila: int, col: int) -> List[Tuple[int, int]]:
        """Calcula los movimientos válidos para un caballo"""
        movimientos = []
        saltos = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        
        for df, dc in saltos:
            nueva_fila, nueva_col = fila + df, col + dc
            if 0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7:
                pieza_destino = self.tablero[nueva_fila][nueva_col]
                if pieza_destino == '.' or self.es_pieza_enemiga(self.tablero[fila][col], pieza_destino):
                    movimientos.append((nueva_fila, nueva_col))
        
        return movimientos
    
    def movimientos_alfil(self, fila: int, col: int) -> List[Tuple[int, int]]:
        """Calcula los movimientos válidos para un alfil"""
        movimientos = []
        direcciones = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for df, dc in direcciones:
            for i in range(1, 8):
                nueva_fila, nueva_col = fila + i * df, col + i * dc
                if not (0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7):
                    break
                
                pieza_destino = self.tablero[nueva_fila][nueva_col]
                if pieza_destino == '.':
                    movimientos.append((nueva_fila, nueva_col))
                else:
                    if self.es_pieza_enemiga(self.tablero[fila][col], pieza_destino):
                        movimientos.append((nueva_fila, nueva_col))
                    break
        
        return movimientos
    
    def movimientos_reina(self, fila: int, col: int) -> List[Tuple[int, int]]:
        """Calcula los movimientos válidos para una reina"""
        return self.movimientos_torre(fila, col) + self.movimientos_alfil(fila, col)
    
    def movimientos_rey(self, fila: int, col: int) -> List[Tuple[int, int]]:
        """Calcula los movimientos válidos para un rey"""
        movimientos = []
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for df, dc in direcciones:
            nueva_fila, nueva_col = fila + df, col + dc
            if 0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7:
                pieza_destino = self.tablero[nueva_fila][nueva_col]
                if pieza_destino == '.' or self.es_pieza_enemiga(self.tablero[fila][col], pieza_destino):
                    movimientos.append((nueva_fila, nueva_col))
        
        return movimientos
    
    def es_pieza_enemiga(self, pieza_origen: str, pieza_destino: str) -> bool:
        """Verifica si la pieza de destino es enemiga"""
        if pieza_destino == '.':
            return False
        return (pieza_origen.islower() and pieza_destino.isupper()) or \
               (pieza_origen.isupper() and pieza_destino.islower())
    
    def es_movimiento_seguro(self, fila_origen: int, col_origen: int, 
                           fila_destino: int, col_destino: int) -> bool:
        """Verifica si un movimiento no deja al rey en jaque"""
        # Crear una copia del tablero
        tablero_temp = copy.deepcopy(self.tablero)
        
        # Realizar el movimiento temporal
        pieza = tablero_temp[fila_origen][col_origen]
        tablero_temp[fila_destino][col_destino] = pieza
        tablero_temp[fila_origen][col_origen] = '.'
        
        # Verificar si el rey está en jaque después del movimiento
        return not self.rey_en_jaque(tablero_temp, self.turno)
    
    def rey_en_jaque(self, tablero: List[List[str]], turno: str) -> bool:
        """Verifica si el rey del jugador actual está en jaque"""
        # Encontrar la posición del rey
        rey = 'k' if turno == 'B' else 'K'
        rey_fila, rey_col = -1, -1
        
        for i in range(8):
            for j in range(8):
                if tablero[i][j] == rey:
                    rey_fila, rey_col = i, j
                    break
        
        if rey_fila == -1:
            return False
        
        # Verificar si alguna pieza enemiga puede atacar al rey
        piezas_enemigas = 'KQRBNP' if turno == 'B' else 'kqrbnp'
        
        for i in range(8):
            for j in range(8):
                if tablero[i][j] in piezas_enemigas:
                    if self.puede_atacar_posicion(tablero, i, j, rey_fila, rey_col):
                        return True
        
        return False
    
    def puede_atacar_posicion(self, tablero: List[List[str]], fila_origen: int, 
                            col_origen: int, fila_destino: int, col_destino: int) -> bool:
        """Verifica si una pieza puede atacar una posición específica"""
        pieza = tablero[fila_origen][col_origen].upper()
        
        if pieza == 'P':
            return self.peon_puede_atacar(fila_origen, col_origen, fila_destino, col_destino, 
                                        tablero[fila_origen][col_origen].islower())
        elif pieza == 'R':
            return self.torre_puede_atacar(fila_origen, col_origen, fila_destino, col_destino, tablero)
        elif pieza == 'N':
            return self.caballo_puede_atacar(fila_origen, col_origen, fila_destino, col_destino)
        elif pieza == 'B':
            return self.alfil_puede_atacar(fila_origen, col_origen, fila_destino, col_destino, tablero)
        elif pieza == 'Q':
            return (self.torre_puede_atacar(fila_origen, col_origen, fila_destino, col_destino, tablero) or
                   self.alfil_puede_atacar(fila_origen, col_origen, fila_destino, col_destino, tablero))
        elif pieza == 'K':
            return abs(fila_origen - fila_destino) <= 1 and abs(col_origen - col_destino) <= 1
        
        return False
    
    def peon_puede_atacar(self, fila_origen: int, col_origen: int, 
                         fila_destino: int, col_destino: int, es_blanca: bool) -> bool:
        """Verifica si un peón puede atacar una posición"""
        direccion = -1 if es_blanca else 1
        return (fila_destino == fila_origen + direccion and 
                abs(col_destino - col_origen) == 1)
    
    def torre_puede_atacar(self, fila_origen: int, col_origen: int, 
                          fila_destino: int, col_destino: int, tablero: List[List[str]]) -> bool:
        """Verifica si una torre puede atacar una posición"""
        if fila_origen != fila_destino and col_origen != col_destino:
            return False
        
        df = 1 if fila_destino > fila_origen else -1 if fila_destino < fila_origen else 0
        dc = 1 if col_destino > col_origen else -1 if col_destino < col_origen else 0
        
        fila, col = fila_origen + df, col_origen + dc
        while fila != fila_destino or col != col_destino:
            if tablero[fila][col] != '.':
                return False
            fila += df
            col += dc
        
        return True
    
    def caballo_puede_atacar(self, fila_origen: int, col_origen: int, 
                           fila_destino: int, col_destino: int) -> bool:
        """Verifica si un caballo puede atacar una posición"""
        df = abs(fila_destino - fila_origen)
        dc = abs(col_destino - col_origen)
        return (df == 2 and dc == 1) or (df == 1 and dc == 2)
    
    def alfil_puede_atacar(self, fila_origen: int, col_origen: int, 
                          fila_destino: int, col_destino: int, tablero: List[List[str]]) -> bool:
        """Verifica si un alfil puede atacar una posición"""
        if abs(fila_destino - fila_origen) != abs(col_destino - col_origen):
            return False
        
        df = 1 if fila_destino > fila_origen else -1
        dc = 1 if col_destino > col_origen else -1
        
        fila, col = fila_origen + df, col_origen + dc
        while fila != fila_destino or col != col_destino:
            if tablero[fila][col] != '.':
                return False
            fila += df
            col += dc
        
        return True
    
    def realizar_movimiento(self, fila_origen: int, col_origen: int, 
                          fila_destino: int, col_destino: int) -> bool:
        """Realiza un movimiento en el tablero"""
        movimientos_validos = self.obtener_movimientos_validos(fila_origen, col_origen)
        
        if (fila_destino, col_destino) not in movimientos_validos:
            return False
        
        # Realizar el movimiento
        pieza = self.tablero[fila_origen][col_origen]
        self.tablero[fila_destino][col_destino] = pieza
        self.tablero[fila_origen][col_origen] = '.'
        
        # Actualizar el historial
        self.historial_movimientos.append({
            'pieza': pieza,
            'desde': (fila_origen, col_origen),
            'hasta': (fila_destino, col_destino),
            'turno': self.turno
        })
        
        # Actualizar contadores de movimientos
        if self.turno == 'B':
            self.movimientos_blanco -= 1
        else:
            self.movimientos_negro -= 1
        
        # Verificar estado del rey
        if self.turno == 'B':
            self.rey_blanco_jaque = self.rey_en_jaque(self.tablero, 'B')
        else:
            self.rey_negro_jaque = self.rey_en_jaque(self.tablero, 'N')
        
        # Cambiar turno
        self.turno = 'N' if self.turno == 'B' else 'B'
        
        # Verificar condiciones de fin de juego
        self.verificar_fin_juego()
        
        return True
    
    def verificar_fin_juego(self):
        """Verifica si el juego ha terminado"""
        # Verificar si hay movimientos válidos para el jugador actual
        movimientos_disponibles = self.obtener_todos_movimientos_validos()
        
        if not movimientos_disponibles:
            if self.rey_blanco_jaque and self.turno == 'B':
                self.resultado = "Victoria para el negro"
            elif self.rey_negro_jaque and self.turno == 'N':
                self.resultado = "Victoria para el blanco"
            else:
                self.resultado = "Empate"
            self.juego_terminado = True
        elif self.movimientos_blanco <= 0 or self.movimientos_negro <= 0:
            self.resultado = "Empate"
            self.juego_terminado = True
    
    def obtener_todos_movimientos_validos(self) -> List[Tuple[int, int, int, int]]:
        """Obtiene todos los movimientos válidos para el jugador actual"""
        movimientos = []
        for i in range(8):
            for j in range(8):
                if self.tablero[i][j] != '.':
                    movimientos_pieza = self.obtener_movimientos_validos(i, j)
                    for fila, col in movimientos_pieza:
                        movimientos.append((i, j, fila, col))
        return movimientos
    
    def evaluar_tablero(self) -> float:
        """Evalúa la posición actual del tablero"""
        puntuacion = 0
        
        for i in range(8):
            for j in range(8):
                pieza = self.tablero[i][j]
                if pieza != '.':
                    puntuacion += self.valores_piezas.get(pieza, 0)
        
        return puntuacion
    
    def obtener_mejor_movimiento_ia(self, nivel_dificultad: str) -> Optional[Tuple[int, int, int, int]]:
        """Obtiene el mejor movimiento según el nivel de dificultad de la IA"""
        movimientos_validos = self.obtener_todos_movimientos_validos()
        
        if not movimientos_validos:
            return None
        
        if nivel_dificultad == "Principiante":
            return random.choice(movimientos_validos)
        elif nivel_dificultad == "Normal":
            return self.movimiento_voraz(movimientos_validos)
        elif nivel_dificultad == "Experto":
            return self.minimax_alfa_beta(movimientos_validos, profundidad=3)
        
        return random.choice(movimientos_validos)
    
    def movimiento_voraz(self, movimientos_validos: List[Tuple[int, int, int, int]]) -> Tuple[int, int, int, int]:
        """Selecciona el movimiento que maximiza la evaluación inmediata"""
        mejor_movimiento = None
        mejor_evaluacion = float('-inf')
        
        for movimiento in movimientos_validos:
            # Crear copia del tablero
            tablero_temp = copy.deepcopy(self.tablero)
            
            # Realizar movimiento temporal
            fila_origen, col_origen, fila_destino, col_destino = movimiento
            pieza = tablero_temp[fila_origen][col_origen]
            tablero_temp[fila_destino][col_destino] = pieza
            tablero_temp[fila_origen][col_origen] = '.'
            
            # Evaluar posición resultante
            evaluacion = self.evaluar_tablero_temporal(tablero_temp)
            
            if evaluacion > mejor_evaluacion:
                mejor_evaluacion = evaluacion
                mejor_movimiento = movimiento
        
        return mejor_movimiento if mejor_movimiento else movimientos_validos[0]
    
    def evaluar_tablero_temporal(self, tablero: List[List[str]]) -> float:
        """Evalúa un tablero temporal"""
        puntuacion = 0
        
        for i in range(8):
            for j in range(8):
                pieza = tablero[i][j]
                if pieza != '.':
                    puntuacion += self.valores_piezas.get(pieza, 0)
        
        return puntuacion
    
    def minimax_alfa_beta(self, movimientos_validos: List[Tuple[int, int, int, int]], 
                         profundidad: int) -> Tuple[int, int, int, int]:
        """Implementa el algoritmo Minimax con poda Alfa-Beta"""
        mejor_movimiento = None
        mejor_evaluacion = float('-inf')
        alfa = float('-inf')
        beta = float('inf')
        
        for movimiento in movimientos_validos:
            # Crear copia del tablero
            tablero_temp = copy.deepcopy(self.tablero)
            
            # Realizar movimiento temporal
            fila_origen, col_origen, fila_destino, col_destino = movimiento
            pieza = tablero_temp[fila_origen][col_origen]
            tablero_temp[fila_destino][col_destino] = pieza
            tablero_temp[fila_origen][col_origen] = '.'
            
            # Evaluar con minimax
            evaluacion = self.minimax_recursivo(tablero_temp, profundidad - 1, alfa, beta, False)
            
            if evaluacion > mejor_evaluacion:
                mejor_evaluacion = evaluacion
                mejor_movimiento = movimiento
            
            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break
        
        return mejor_movimiento if mejor_movimiento else movimientos_validos[0]
    
    def minimax_recursivo(self, tablero: List[List[str]], profundidad: int, 
                         alfa: float, beta: float, es_maximizador: bool) -> float:
        """Función recursiva del algoritmo Minimax"""
        if profundidad == 0:
            return self.evaluar_tablero_temporal(tablero)
        
        # Generar movimientos para el tablero temporal
        movimientos = self.generar_movimientos_temporales(tablero, es_maximizador)
        
        if not movimientos:
            return self.evaluar_tablero_temporal(tablero)
        
        if es_maximizador:
            max_eval = float('-inf')
            for movimiento in movimientos:
                # Crear nuevo tablero temporal
                nuevo_tablero = copy.deepcopy(tablero)
                fila_origen, col_origen, fila_destino, col_destino = movimiento
                pieza = nuevo_tablero[fila_origen][col_origen]
                nuevo_tablero[fila_destino][col_destino] = pieza
                nuevo_tablero[fila_origen][col_origen] = '.'
                
                eval = self.minimax_recursivo(nuevo_tablero, profundidad - 1, alfa, beta, False)
                max_eval = max(max_eval, eval)
                alfa = max(alfa, eval)
                if beta <= alfa:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for movimiento in movimientos:
                # Crear nuevo tablero temporal
                nuevo_tablero = copy.deepcopy(tablero)
                fila_origen, col_origen, fila_destino, col_destino = movimiento
                pieza = nuevo_tablero[fila_origen][col_origen]
                nuevo_tablero[fila_destino][col_destino] = pieza
                nuevo_tablero[fila_origen][col_origen] = '.'
                
                eval = self.minimax_recursivo(nuevo_tablero, profundidad - 1, alfa, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alfa:
                    break
            return min_eval
    
    def generar_movimientos_temporales(self, tablero: List[List[str]], es_maximizador: bool) -> List[Tuple[int, int, int, int]]:
        """Genera movimientos válidos para un tablero temporal"""
        movimientos = []
        piezas_buscar = 'kqrbnp' if es_maximizador else 'KQRBNP'
        
        for i in range(8):
            for j in range(8):
                if tablero[i][j] in piezas_buscar:
                    # Implementación simplificada - en una versión completa se necesitaría
                    # implementar la lógica de movimientos para el tablero temporal
                    movimientos_pieza = self.obtener_movimientos_validos_temporales(tablero, i, j)
                    for fila, col in movimientos_pieza:
                        movimientos.append((i, j, fila, col))
        
        return movimientos
    
    def obtener_movimientos_validos_temporales(self, tablero: List[List[str]], fila: int, col: int) -> List[Tuple[int, int]]:
        """Obtiene movimientos válidos para una pieza en un tablero temporal"""
        # Implementación simplificada - retorna movimientos básicos
        # En una implementación completa, se necesitaría replicar toda la lógica de movimientos
        movimientos = []
        pieza = tablero[fila][col]
        
        if pieza.upper() == 'P':  # Peón
            direccion = -1 if pieza.islower() else 1
            nueva_fila = fila + direccion
            if 0 <= nueva_fila <= 7 and tablero[nueva_fila][col] == '.':
                movimientos.append((nueva_fila, col))
        elif pieza.upper() == 'K':  # Rey
            for df in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if df == 0 and dc == 0:
                        continue
                    nueva_fila, nueva_col = fila + df, col + dc
                    if 0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7:
                        if tablero[nueva_fila][nueva_col] == '.' or \
                           ((pieza.islower() and tablero[nueva_fila][nueva_col].isupper()) or
                            (pieza.isupper() and tablero[nueva_fila][nueva_col].islower())):
                            movimientos.append((nueva_fila, nueva_col))
        
        return movimientos
