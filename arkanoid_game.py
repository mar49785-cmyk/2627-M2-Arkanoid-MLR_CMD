"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
import math

from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

@arkanoid_method
def cargar_nivel(self) -> list[str]:
    """Lee el fichero de nivel y devuelve la cuadrícula como lista de filas."""
    
    # - Comprueba que `self.level_path` existe y es fichero.
    ruta = self.level_path
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de nivel: {ruta}")
    
    # - Lee su contenido, filtra líneas vacías y valida que todas tienen el mismo ancho.
    contenido = ruta.read_text().splitlines()
    filas = [linea for linea in contenido if linea.strip()]
    ancho = len(filas[0])
    for fila in filas:
        if len(fila) != ancho:
            raise ValueError("Todas las dilas de nivel deben de tener el mismo ancho")
    
    # - Guarda el resultado en `self.layout` y devuélvelo.
    self.layout = filas
    return filas

@arkanoid_method
def preparar_entidades(self) -> None:
    """Posiciona paleta y bola, y reinicia puntuación y vidas."""
    
    # - Ajusta el tamaño de `self.paddle` y céntrala usando `midbottom`.
    self.paddle = self.crear_rect(0, 0, *self.PADDLE_SIZE)
    self.paddle.midbottom = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.PADDLE_OFFSET)

    # - Reinicia `self.score`, `self.lives` y `self.end_message`.
    self.score = 0
    self.lives = 3
    self.end_message = ""

    # - Llama a `self.reiniciar_bola()` para colocar la bola sobre la paleta.
    self.reiniciar_bola()

@arkanoid_method
def crear_bloques(self) -> None:
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    
    # - Limpia `self.blocks`, `self.block_colors` y `self.block_symbols`.
    self.blocks.clear()
    self.block_colors.clear()
    self.block_symbols.clear()

    # - Recorre `self.layout` para detectar símbolos de bloque.
    # - Usa `self.calcular_posicion_bloque` y rellena las listas paralelas.
    for fila, linea in enumerate(self.layout):
        for col, simbolo in enumerate(linea):
            if simbolo in self.BLOCK_COLORS:
                rect = self.calcular_posicion_bloque(fila, col)
                self.blocks.append(rect)   
                self.block_colors.append(self.BLOCK_COLORS[simbolo]) 
                self.block_symbols.append(simbolo)

@arkanoid_method
def procesar_input(self) -> None:
    """Gestiona la entrada de teclado para mover la paleta."""
    
    # - Obtén el estado de teclas con `self.obtener_estado_teclas()`.
    keys = self.obtener_estado_teclas()

    # - Desplaza la paleta con `self.PADDLE_SPEED` si se pulsan las teclas izquierda/derecha.
    if keys[self.KEY_LEFT] or keys[self.KEY_A]:
        self.paddle.x -= self.PADDLE_SPEED
    if keys[self.KEY_RIGHT] or keys[self.KEY_D]:
        self.paddle.x += self.PADDLE_SPEED

    # - Limita la posición para que no salga de la pantalla.
    if self.paddle.left < 0:
        self.paddle.left = 0
    if self.paddle.right > self.SCREEN_WIDTH:
        self.paddle.right = self.SCREEN_WIDTH

@arkanoid_method
def actualizar_bola(self) -> None:
    """Actualiza la posición de la bola y resuelve colisiones."""
    
    # - Suma `self.ball_velocity` a `self.ball_pos` y genera `ball_rect` con `self.obtener_rect_bola()`.
    self.ball_pos += self.ball_velocity
    ball_rect = self.obtener_rect_bola()

    # - Gestiona rebotes con paredes, paleta y bloques, modificando velocidad y puntuación.
    if ball_rect.left <= 0 or ball_rect.right >= self.SCREEN_WIDTH: # Rebote con laterales
        self.ball_velocity.x *= -1
    if ball_rect.top <= 0: # Rebote con el techo
        self.ball_velocity.y *= -1
    if ball_rect.colliderect(self.paddle): # Colisión con la paleta
        offset = (ball_rect.centerx - self.paddle.centerx) / (self.PADDLE_SIZE[0] / 2)
        angle = offset * (math.pi / 3) # Máximo 60 grados
        speed = self.ball_velocity.length()
        self.ball_velocity.x = speed * math.sin(angle)
        self.ball_velocity.y = -abs(speed * math.cos(angle))
        
    for i, rect in enumerate(self.blocks): # Colisión con bloques
         if ball_rect.colliderect(rect):
             simbolo = self.block_symbols[i]
             puntos = self.BLOCK_POINTS[simbolo]
             self.score += puntos

             # Eliminar bloque y sus datos paralelos
             del self.blocks[i]
             del self.block_colors[i]
             del self.block_symbols[i]

             # Rebote simple: invertir eje Y
             self.ball_velocity.y *= -1
             break # Salimos para evitar dobles colisiones

    # - Controla fin de nivel cuando no queden bloques y resta vidas si la bola cae.
    if ball_rect.top > self.SCREEN_HEIGHT:
        self.lives -= 1
        self.reiniciar_bola()
        return
    if not self.blocks:
        self.end_message = "¡Nivel completado!"

@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""
    
    # - Rellena el fondo y dibuja cada bloque con `self.dibujar_rectangulo`.
    self.screen.fill(self.BACKGROUND_COLOR)
    for rect, color in zip(self.blocks, self.block_colors):
        self.dibujar_rectangulo(rect, color)

    # - Pinta la paleta y la bola con las utilidades proporcionadas.
    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)
    self.dibujar_circulo(
        (int(self.ball_pos.x), int(self.ball_pos.y)),
        self.BALL_RADIUS,
        self.BALL_COLOR
    )

    # - Muestra puntuación, vidas y mensajes usando `self.dibujar_texto`.
    self.dibujar_texto(f"Puntuación: {self.score}", (20,20))
    self.dibujar_texto(f"Vidas: {self.lives}", (20,50))
    if self.end_message:
        self.dibujar_texto(self.end_message, (260, 280), grande=True)

@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""
    # - Inicializa recursos (`self.inicializar_pygame`, `self.cargar_nivel`, etc.).
    self.inicializar_pygame()
    print("Pygame inicializado")
    self.cargar_nivel()
    print(f"Nivel cargado: {self.layout}")
    self.preparar_entidades()
    print("Entidades preparadas")
    self.crear_bloques()
    print(f"Bloques creados: {len(self.blocks)}")
    self.running = True

    # - Procesa eventos de `self.iterar_eventos()` y llama a los métodos de actualización/dibujo.
    # - Refresca la pantalla con `self.actualizar_pantalla()` y cierra con `self.finalizar_pygame()`.
    while self.running:
        # Eventos
        for event in self.iterar_eventos():
            if event.type == self.EVENT_QUIT:
                self.running = False
            elif event.type == self.EVENT_KEYDOWN:
                if event.key == self.KEY_ESCAPE:
                    self.running = False
        # Lógica
        self.procesar_input()
        self.actualizar_bola()
        # Dibujado
        self.dibujar_escena()
        self.actualizar_pantalla()
        self.clock.tick(self.FPS)
        # Fin de partida
        if self.lives <= 0:
            self.end_message = "GAME OVER"
            self.dibujar_escena()
            self.actualizar_pantalla()
            self.esperar(1500)
            self.running = False
    self.finalizar_pygame()


def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()


if __name__ == "__main__":
    main()
