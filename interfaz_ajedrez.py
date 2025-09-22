import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
from ajedrez_960 import Ajedrez960

class InterfazAjedrez:
    def __init__(self):
        self.juego = Ajedrez960()
        self.nivel_dificultad = "Normal"
        self.color_humano = "Blanco"  # Color que juega el humano
        self.casilla_seleccionada = None
        self.movimientos_posibles = []
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Ajedrez 960 - Humano vs Máquina")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Actualizar display inicial
        self.actualizar_display()
    
    def configurar_estilo(self):
        """Configura el estilo visual de la interfaz"""
        self.colores = {
            'casilla_clara': '#F0D9B5',
            'casilla_oscura': '#B58863',
            'casilla_seleccionada': '#FFD700',
            'casilla_posible': '#90EE90',
            'texto_principal': '#2C3E50',
            'texto_secundario': '#7F8C8D'
        }
        
        # Configurar fuente
        self.fuente_principal = ('Arial', 12, 'bold')
        self.fuente_secundaria = ('Arial', 10)
        self.fuente_piezas = ('Arial', 24, 'bold')
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg='white')
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel superior con controles
        self.crear_panel_controles()
        
        # Panel del tablero
        self.crear_panel_tablero()
        
        # Panel de información
        self.crear_panel_informacion()
    
    def crear_panel_controles(self):
        """Crea el panel de controles superior"""
        self.frame_controles = tk.Frame(self.frame_principal, bg='white')
        self.frame_controles.pack(fill=tk.X, pady=(0, 10))
        
        # Título
        titulo = tk.Label(self.frame_controles, text="Ajedrez 960", 
                         font=('Arial', 18, 'bold'), fg=self.colores['texto_principal'], bg='white')
        titulo.pack(side=tk.LEFT)
        
        # Frame para controles
        self.frame_botones = tk.Frame(self.frame_controles, bg='white')
        self.frame_botones.pack(side=tk.RIGHT)
        
        # Selector de color
        tk.Label(self.frame_botones, text="Tu color:", font=self.fuente_secundaria, 
                fg=self.colores['texto_secundario'], bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        self.combo_color = ttk.Combobox(self.frame_botones, values=["Blanco", "Negro"],
                                      state="readonly", width=8)
        self.combo_color.set(self.color_humano)
        self.combo_color.pack(side=tk.LEFT, padx=(0, 10))
        self.combo_color.bind('<<ComboboxSelected>>', self.cambiar_color)
        
        # Selector de dificultad
        tk.Label(self.frame_botones, text="Dificultad:", font=self.fuente_secundaria, 
                fg=self.colores['texto_secundario'], bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        self.combo_dificultad = ttk.Combobox(self.frame_botones, values=["Principiante", "Normal", "Experto"],
                                           state="readonly", width=12)
        self.combo_dificultad.set(self.nivel_dificultad)
        self.combo_dificultad.pack(side=tk.LEFT, padx=(0, 10))
        self.combo_dificultad.bind('<<ComboboxSelected>>', self.cambiar_dificultad)
        
        # Botón nuevo juego
        self.btn_nuevo = tk.Button(self.frame_botones, text="Nuevo Juego", 
                                  command=self.nuevo_juego, font=self.fuente_secundaria,
                                  bg='#3498DB', fg='white', relief=tk.FLAT, padx=15, pady=5)
        self.btn_nuevo.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón rendirse
        self.btn_rendirse = tk.Button(self.frame_botones, text="Rendirse", 
                                     command=self.rendirse, font=self.fuente_secundaria,
                                     bg='#E74C3C', fg='white', relief=tk.FLAT, padx=15, pady=5)
        self.btn_rendirse.pack(side=tk.LEFT)
    
    def crear_panel_tablero(self):
        """Crea el panel del tablero de ajedrez"""
        self.frame_tablero = tk.Frame(self.frame_principal, bg='white')
        self.frame_tablero.pack(side=tk.LEFT, padx=(0, 20))
        
        # Canvas para el tablero
        self.canvas = tk.Canvas(self.frame_tablero, width=480, height=480, 
                               bg='white', highlightthickness=2, highlightbackground='#34495E')
        self.canvas.pack()
        
        # Bind eventos del mouse
        self.canvas.bind('<Button-1>', self.click_casilla)
        
        # Crear las casillas del tablero
        self.casillas = []
        for i in range(8):
            fila = []
            for j in range(8):
                x1, y1 = j * 60, i * 60
                x2, y2 = x1 + 60, y1 + 60
                
                color = self.colores['casilla_clara'] if (i + j) % 2 == 0 else self.colores['casilla_oscura']
                casilla = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=1)
                fila.append(casilla)
            self.casillas.append(fila)
        
        # Crear etiquetas de coordenadas
        self.crear_coordenadas()
    
    def crear_coordenadas(self):
        """Crea las etiquetas de coordenadas del tablero"""
        # Letras (columnas)
        for i in range(8):
            letra = chr(ord('a') + i)
            self.canvas.create_text(30 + i * 60, 465, text=letra, font=self.fuente_secundaria, fill='black')
        
        # Números (filas)
        for i in range(8):
            numero = str(8 - i)
            self.canvas.create_text(465, 30 + i * 60, text=numero, font=self.fuente_secundaria, fill='black')
    
    def crear_panel_informacion(self):
        """Crea el panel de información lateral"""
        self.frame_info = tk.Frame(self.frame_principal, bg='white', width=250)
        self.frame_info.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame_info.pack_propagate(False)
        
        # Información del juego
        self.label_turno = tk.Label(self.frame_info, text="Turno: Blanco", 
                                   font=self.fuente_principal, fg=self.colores['texto_principal'], bg='white')
        self.label_turno.pack(pady=(0, 10))
        
        # Estado del rey
        self.label_rey_blanco = tk.Label(self.frame_info, text="Rey Blanco: Seguro", 
                                        font=self.fuente_secundaria, fg='green', bg='white')
        self.label_rey_blanco.pack(pady=(0, 5))
        
        self.label_rey_negro = tk.Label(self.frame_info, text="Rey Negro: Seguro", 
                                       font=self.fuente_secundaria, fg='green', bg='white')
        self.label_rey_negro.pack(pady=(0, 10))
        
        # Movimientos restantes
        self.label_movimientos = tk.Label(self.frame_info, text="Movimientos restantes:", 
                                         font=self.fuente_secundaria, fg=self.colores['texto_secundario'], bg='white')
        self.label_movimientos.pack(pady=(0, 5))
        
        self.label_mov_blanco = tk.Label(self.frame_info, text="Blanco: 20", 
                                        font=self.fuente_secundaria, fg='black', bg='white')
        self.label_mov_blanco.pack(pady=(0, 2))
        
        self.label_mov_negro = tk.Label(self.frame_info, text="Negro: 20", 
                                       font=self.fuente_secundaria, fg='black', bg='white')
        self.label_mov_negro.pack(pady=(0, 15))
        
        # Separador
        separador = tk.Frame(self.frame_info, height=2, bg='#BDC3C7')
        separador.pack(fill=tk.X, pady=(0, 15))
        
        # Historial de movimientos
        tk.Label(self.frame_info, text="Historial de Movimientos:", 
                font=self.fuente_secundaria, fg=self.colores['texto_secundario'], bg='white').pack(pady=(0, 5))
        
        # Frame para el historial con scrollbar
        self.frame_historial = tk.Frame(self.frame_info, bg='white')
        self.frame_historial.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.frame_historial)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_historial = tk.Text(self.frame_historial, height=15, width=25, 
                                     font=self.fuente_secundaria, yscrollcommand=self.scrollbar.set,
                                     bg='#F8F9FA', fg='black', relief=tk.FLAT)
        self.text_historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar.config(command=self.text_historial.yview)
    
    def click_casilla(self, event):
        """Maneja el click en una casilla del tablero"""
        if self.juego.juego_terminado:
            return
        
        # Calcular coordenadas de la casilla clickeada
        col = event.x // 60
        fila = event.y // 60
        
        if not (0 <= fila <= 7 and 0 <= col <= 7):
            return
        
        # Verificar si es turno del humano
        turno_humano = (self.juego.turno == 'B' and self.color_humano == "Blanco") or \
                      (self.juego.turno == 'N' and self.color_humano == "Negro")
        
        if not turno_humano:
            return
        
        # Si no hay casilla seleccionada, seleccionar esta
        if self.casilla_seleccionada is None:
            pieza = self.juego.tablero[fila][col]
            if pieza != '.':
                # Verificar si la pieza pertenece al humano
                es_pieza_humana = (self.color_humano == "Blanco" and pieza.islower()) or \
                                 (self.color_humano == "Negro" and pieza.isupper())
                
                if es_pieza_humana:
                    self.casilla_seleccionada = (fila, col)
                    self.movimientos_posibles = self.juego.obtener_movimientos_validos(fila, col)
                    self.actualizar_display()
        else:
            # Intentar realizar movimiento
            fila_origen, col_origen = self.casilla_seleccionada
            
            if (fila, col) in self.movimientos_posibles:
                # Realizar movimiento
                if self.juego.realizar_movimiento(fila_origen, col_origen, fila, col):
                    self.actualizar_display()
                    self.actualizar_historial()
                    
                    # Verificar si el juego terminó
                    if self.juego.juego_terminado:
                        self.mostrar_resultado()
                    else:
                        # Turno de la máquina
                        self.root.after(1000, self.movimiento_maquina)
            
            # Limpiar selección
            self.casilla_seleccionada = None
            self.movimientos_posibles = []
            self.actualizar_display()
    
    def movimiento_maquina(self):
        """Realiza el movimiento de la máquina"""
        # Verificar si es turno de la máquina
        turno_maquina = (self.juego.turno == 'B' and self.color_humano == "Negro") or \
                       (self.juego.turno == 'N' and self.color_humano == "Blanco")
        
        if self.juego.juego_terminado or not turno_maquina:
            return
        
        # Obtener mejor movimiento según la dificultad
        movimiento = self.juego.obtener_mejor_movimiento_ia(self.nivel_dificultad)
        
        if movimiento:
            fila_origen, col_origen, fila_destino, col_destino = movimiento
            
            # Realizar movimiento
            if self.juego.realizar_movimiento(fila_origen, col_origen, fila_destino, col_destino):
                self.actualizar_display()
                self.actualizar_historial()
                
                # Verificar si el juego terminó
                if self.juego.juego_terminado:
                    self.mostrar_resultado()
    
    def actualizar_display(self):
        """Actualiza la visualización del tablero y la información"""
        # Actualizar piezas en el tablero
        for i in range(8):
            for j in range(8):
                pieza = self.juego.tablero[i][j]
                
                # Determinar color de la casilla
                color_base = self.colores['casilla_clara'] if (i + j) % 2 == 0 else self.colores['casilla_oscura']
                
                # Aplicar colores especiales
                if self.casilla_seleccionada == (i, j):
                    color = self.colores['casilla_seleccionada']
                elif (i, j) in self.movimientos_posibles:
                    color = self.colores['casilla_posible']
                else:
                    color = color_base
                
                # Actualizar color de la casilla
                self.canvas.itemconfig(self.casillas[i][j], fill=color)
                
                # Limpiar texto anterior
                self.canvas.delete(f"pieza_{i}_{j}")
                
                # Dibujar pieza si existe
                if pieza != '.':
                    x, y = j * 60 + 30, i * 60 + 30
                    color_texto = 'white' if pieza.isupper() else 'black'
                    
                    # Mapear símbolos a caracteres Unicode
                    simbolos = {
                        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
                        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
                    }
                    
                    simbolo = simbolos.get(pieza, pieza)
                    self.canvas.create_text(x, y, text=simbolo, font=self.fuente_piezas, 
                                          fill=color_texto, tags=f"pieza_{i}_{j}")
        
        # Actualizar información del juego
        self.actualizar_informacion()
    
    def actualizar_informacion(self):
        """Actualiza la información del juego"""
        # Turno actual
        if self.juego.turno == 'B':
            turno_texto = f"Turno: Blanco ({'Humano' if self.color_humano == 'Blanco' else 'Máquina'})"
        else:
            turno_texto = f"Turno: Negro ({'Humano' if self.color_humano == 'Negro' else 'Máquina'})"
        self.label_turno.config(text=turno_texto)
        
        # Estado de los reyes
        estado_blanco = "En Jaque" if self.juego.rey_blanco_jaque else "Seguro"
        color_blanco = 'red' if self.juego.rey_blanco_jaque else 'green'
        self.label_rey_blanco.config(text=f"Rey Blanco: {estado_blanco}", fg=color_blanco)
        
        estado_negro = "En Jaque" if self.juego.rey_negro_jaque else "Seguro"
        color_negro = 'red' if self.juego.rey_negro_jaque else 'green'
        self.label_rey_negro.config(text=f"Rey Negro: {estado_negro}", fg=color_negro)
        
        # Movimientos restantes
        self.label_mov_blanco.config(text=f"Blanco: {self.juego.movimientos_blanco}")
        self.label_mov_negro.config(text=f"Negro: {self.juego.movimientos_negro}")
    
    def actualizar_historial(self):
        """Actualiza el historial de movimientos"""
        if self.juego.historial_movimientos:
            ultimo_movimiento = self.juego.historial_movimientos[-1]
            pieza = ultimo_movimiento['pieza']
            desde = ultimo_movimiento['desde']
            hasta = ultimo_movimiento['hasta']
            turno = ultimo_movimiento['turno']
            
            # Convertir coordenadas a notación de ajedrez
            desde_str = f"{chr(ord('a') + desde[1])}{8 - desde[0]}"
            hasta_str = f"{chr(ord('a') + hasta[1])}{8 - hasta[0]}"
            
            # Determinar número de movimiento
            num_movimiento = len(self.juego.historial_movimientos)
            if turno == 'B':
                texto = f"{num_movimiento//2 + 1}. {pieza.upper()}: {desde_str}-{hasta_str}\n"
            else:
                texto = f"    {pieza.upper()}: {desde_str}-{hasta_str}\n"
            
            self.text_historial.insert(tk.END, texto)
            self.text_historial.see(tk.END)
    
    def cambiar_color(self, event):
        """Cambia el color que juega el humano"""
        self.color_humano = self.combo_color.get()
        # Reiniciar el juego cuando se cambia el color
        self.juego.resetear_juego()
        
        # Si el humano elige Negro, cambiar el turno para que empiece el humano
        if self.color_humano == "Negro":
            self.juego.turno = 'N'  # Cambiar a turno de Negro
        
        self.casilla_seleccionada = None
        self.movimientos_posibles = []
        self.text_historial.delete(1.0, tk.END)
        self.actualizar_display()
        messagebox.showinfo("Color Cambiado", 
                           f"Ahora juegas con las piezas {self.color_humano.lower()}s. ¡Nuevo juego iniciado!")
    
    def cambiar_dificultad(self, event):
        """Cambia el nivel de dificultad de la IA"""
        self.nivel_dificultad = self.combo_dificultad.get()
        messagebox.showinfo("Dificultad Cambiada", 
                           f"Dificultad cambiada a: {self.nivel_dificultad}")
    
    def nuevo_juego(self):
        """Inicia un nuevo juego"""
        self.juego.resetear_juego()
        
        # Si el humano elige Negro, cambiar el turno para que empiece el humano
        if self.color_humano == "Negro":
            self.juego.turno = 'N'  # Cambiar a turno de Negro
        
        self.casilla_seleccionada = None
        self.movimientos_posibles = []
        self.text_historial.delete(1.0, tk.END)
        self.actualizar_display()
        messagebox.showinfo("Nuevo Juego", f"¡Nuevo juego iniciado! Juegas con las piezas {self.color_humano.lower()}s")
    
    def rendirse(self):
        """El jugador se rinde"""
        if messagebox.askyesno("Rendirse", "¿Estás seguro de que quieres rendirte?"):
            self.juego.juego_terminado = True
            if self.color_humano == "Blanco":
                self.juego.resultado = "Victoria para el negro"
            else:
                self.juego.resultado = "Victoria para el blanco"
            self.mostrar_resultado()
    
    def mostrar_resultado(self):
        """Muestra el resultado del juego"""
        if self.juego.resultado:
            if "Victoria para el blanco" in self.juego.resultado:
                if self.color_humano == "Blanco":
                    mensaje = "¡Felicidades! Has ganado."
                else:
                    mensaje = "La máquina ha ganado. ¡Mejor suerte la próxima vez!"
            elif "Victoria para el negro" in self.juego.resultado:
                if self.color_humano == "Negro":
                    mensaje = "¡Felicidades! Has ganado."
                else:
                    mensaje = "La máquina ha ganado. ¡Mejor suerte la próxima vez!"
            else:
                mensaje = "El juego ha terminado en empate."
            
            messagebox.showinfo("Juego Terminado", mensaje)
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = InterfazAjedrez()
    app.ejecutar()
