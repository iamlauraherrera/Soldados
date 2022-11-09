'''
    Integrantes: Laura Herrera y Jaime Andres
    FECHA:       09/11/22
    TEMA: Parcial 2 - Juego de soldados que disparan y con colisiones de objetos
'''
import pygame  #Importamos la libreria

#METODO PRINCIPAL DEL JUEGO
class Jugador(pygame.sprite.Sprite): 
    def __init__(self, coor_x, coor_y, imagen, vidas, arriba, abajo, izquierda, derecha, disparo):
        super().__init__()
        self.image = pygame.image.load(imagen).convert()
        self.image.set_colorkey(CHROMA)
        self.rect = self.image.get_rect()
        self.rect.center = (coor_x, coor_y)
        self.rect_inside = pygame.Rect(self.rect.left+10, self.rect.top+10, self.rect.w-20, self.rect.h-20)

        self.Tecla_Arriba = arriba
        self.Tecla_Abajo = abajo
        self.Tecla_Izquierda = izquierda
        self.Tecla_Derecha = derecha
        self.Tecla_Disparo = disparo

        self.Cadencia = 200
        self.Ultimo_Disparo = pygame.time.get_ticks()
        self.Sonido_Disparo = pygame.mixer.Sound("Audio/SonidoBala.mp3")

        self.Paso = 0
        self.Movimiento = False
        self.Invertir = False
        self.FT = True

        self.Velocidad = 10
        self.Velocidad_X = 0
        self.Velocidad_Y = 0

        self.Vidas = vidas

        if self.rect.left >= ANCHO // 2:
            self.image =pygame.transform.flip(self.image,True,False)
            self.Invertir = True

    def update(self):
        self.Velocidad_X = 0
        self.Velocidad_Y = 0
        self.Movimiento = False
        self.Tiempo = pygame.time.get_ticks()
        tecla = pygame.key.get_pressed()
        if tecla[self.Tecla_Arriba]:
            self.Velocidad_Y = -self.Velocidad
            self.Movimiento = True
        if tecla[self.Tecla_Abajo]:
            self.Velocidad_Y = self.Velocidad
            self.Movimiento = True  
        if tecla[self.Tecla_Izquierda]:
            self.Velocidad_X = -self.Velocidad
            self.Movimiento = True
            self.Invertir = True
        if tecla[self.Tecla_Derecha]:
            self.Velocidad_X = self.Velocidad
            self.Movimiento = True
            self.Invertir = False
        if tecla[self.Tecla_Disparo]:
            if self.FT:
                self.Sonido_Disparo.play()
                self.disparo()
                self.Ultimo_Disparo = self.Tiempo
                self.FT = False
            if self.Tiempo - self.Ultimo_Disparo > self.Cadencia:
                self.Sonido_Disparo.play()
                self.disparo()
                self.Ultimo_Disparo = self.Tiempo
    
        if self.Paso + 1 >=  3:
            self.Paso = 0
        if self.Movimiento and self.Invertir == False:
            self.image = Movimientos[self.Paso // 1].convert()
            self.image.set_colorkey(CHROMA)
            self.Paso += 1
        
        elif self.Movimiento and self.Invertir:
            self.image = Movimientos[self.Paso // 1].convert()
            self.image.set_colorkey(CHROMA)
            self.image =pygame.transform.flip(self.image,True,False)
            self.Paso += 1

        self.rect.x += self.Velocidad_X
        self.rect.y += self.Velocidad_Y

        # Limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        # Limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0
        # Limita el margen inferior
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
        # Limita el margen superior
        if self.rect.top < 0:
            self.rect.top = 0
    
    def disparo(self):
        
        bala = disparos(self.rect.centerx,self.rect.centery, self.Invertir)
        Grupo_Balas.add(bala)
        
#METODO DE DISPARAR
class disparos(pygame.sprite.Sprite):
    def __init__(self, x, y, invertir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface ((10,5))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.bottom = y - 25
        self.invertir = invertir
        self.Vel_Bala = 30
        
        if self.invertir:
            self.rect.centerx = x - 64
        else:
            self.rect.centerx = x + 64

    def update(self):
        if self.invertir:
            self.rect.x -= self.Vel_Bala
        else:
            self.rect.x += self.Vel_Bala

#METODO DE GANADOR
def Win(Jugador):
    Ejecutar = True
    if Jugador == 1:
        Pantalla.blit(Win_2, [0,0])
        Jugador = 0
    if Jugador == 2:
        Pantalla.blit(Win_1, [0,0])
        Jugador = 0
    pygame.display.flip()
    while Ejecutar:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Ejecutar = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if y >= 417 and y <=  487 and x >= 115 and x <= 375:
                    Ejecutar = False
                    Juego()
                if y >= 417 and y <=  487 and x >= 420 and x <= 680:
                    exit()

#METODO DE COMANDOS DE TECLAS Y CONTROLES QUE SE VAN A USAR
def Control():
    Ejecutar = True
    Pantalla.blit(Controles, [0,0])
    pygame.display.flip()
    while Ejecutar:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Ejecutar = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if y >= 478 and y <=  548 and x >= 278 and x <= 538:
                    Ejecutar = False
                    Pausar()
                    
#METODO PAUSAR JUEGO
def Pausar():
    Ejecutar = True
    Pantalla.blit(Pausa, [0,0])
    pygame.display.flip()
    while Ejecutar:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Ejecutar = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if y >= 417 and y <=  487 and x >= 115 and x <= 375:
                    Ejecutar = False
                if y >= 417 and y <=  487 and x >= 420 and x <= 680:
                    exit()
                if y >= 502 and y <=  572 and x >= 267 and x <= 527:
                    Control()

#METODO PARA EL OBJETO / BARRIL
class Barril(pygame.sprite.Sprite):
    def __init__(self, coor_x, coor_y, imagen):
        super().__init__()
        self.image = pygame.image.load(imagen).convert()
        self.image.set_colorkey(CHROMA)
        self.rect = self.image.get_rect()
        self.rect.x = coor_x
        self.rect.y = coor_y

pygame.init()

pygame.mixer.music.load("Audio/Musica.mp3")
pygame.mixer.music.play(1)
pygame.mixer.music.set_volume(0.2)

clock = pygame.time.Clock()

ANCHO = 800
ALTO = 600

Pantalla = pygame.display.set_mode((ANCHO,ALTO))
Icono = pygame.image.load("Imagen/Icono.png").convert()
pygame.display.set_caption("Soldier Shooter")
pygame.display.set_icon(Icono)

BLANCO = (255,255,255)
NEGRO = (0,0,0)
CHROMA = (0,0,255)

Grupo_Jugador = pygame.sprite.Group()
Grupo_Balas = pygame.sprite.Group()
Grupo_Barril = pygame.sprite.Group()

Movimientos = [pygame.image.load("Imagen/Soldado1.png"),
            pygame.image.load("Imagen/Soldado2.png"),
            pygame.image.load("Imagen/Soldado3.png")]
#Inicial = pygame.image.load("Inicial.png")

Win_1 = pygame.image.load("Imagen/Jugador1Win.png").convert()
Win_2 = pygame.image.load("Imagen/Jugador2Win.png").convert()
Pausa = pygame.image.load("Imagen/Pausa.png").convert()
Inicio = pygame.image.load("Imagen/Inicial.png").convert()
Controles = pygame.image.load("Imagen/Controles.png").convert()
Fondo = pygame.image.load("Imagen/Fondo.png").convert()

#FPS
FPS = 15

#Motor de Arranque principal del juego
def Juego():
    Jugador_1 = Jugador(ANCHO//4, ALTO //2, "Imagen/Soldado1.png", 10, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE)
    Grupo_Jugador.add(Jugador_1)
    Jugador_2 = Jugador((ANCHO//2 + ANCHO//4), ALTO//2, "Imagen/Soldado1.png", 10, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL)
    Grupo_Jugador.add(Jugador_2)
    Barril_1 = Barril(280,290,"Imagen/palmera.png")
    Grupo_Barril.add(Barril_1)
    Barril_2 = Barril(430,100,"Imagen/palmera.png")
    Grupo_Barril.add(Barril_2)

    Ejecutar = True

    Letra_HW = 36
    Fuente = pygame.font.Font("Font/Arial.ttf", Letra_HW)

    while Ejecutar:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Ejecutar = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Pausar()
        #Actualizacion 
        Pantalla.blit(Fondo,[0,0])
        Grupo_Jugador.update()
        Grupo_Balas.update()

        Contador_1 = Fuente.render(str(Jugador_1.Vidas), 0, BLANCO).convert()
        Contador_2 = Fuente.render(str(Jugador_2.Vidas), 0, BLANCO).convert()
        #Dibujo
        
        Linea_Central = pygame.draw.rect(Pantalla, BLANCO,(ANCHO / 2, 0, 5, ALTO),0)
        Grupo_Balas.draw(Pantalla)
        Grupo_Jugador.draw(Pantalla)
        Grupo_Barril.draw(Pantalla)
        Pantalla.blit(Contador_1,[ANCHO / 4 - Letra_HW, 0])
        Pantalla.blit(Contador_2,[(ANCHO / 4) * 3, 0])

        if Jugador_1.rect.colliderect(Linea_Central):
            Jugador_1.rect.right = Linea_Central.left
        if Jugador_2.rect.colliderect(Linea_Central):
            Jugador_2.rect.left = Linea_Central.right
        if pygame.sprite.spritecollide(Jugador_1,Grupo_Barril,False):
            if Jugador_1.rect.top < Barril_1.rect.bottom and Jugador_1.rect.centerx > Barril_1.rect.left and Jugador_1.rect.centerx < Barril_1.rect.right and Jugador_1.rect.top > Barril_1.rect.top:
                Jugador_1.rect.top = Barril_1.rect.bottom
            if Jugador_1.rect.bottom > Barril_1.rect.top and Jugador_1.rect.centerx > Barril_1.rect.left and Jugador_1.rect.centerx < Barril_1.rect.right and Jugador_1.rect.bottom < Barril_1.rect.bottom:
                Jugador_1.rect.bottom = Barril_1.rect.top
            if Jugador_1.rect.right > Barril_1.rect.left and Jugador_1.rect.centery > Barril_1.rect.top and Jugador_1.rect.centery < Barril_1.rect.bottom:
                Jugador_1.rect.right = Barril_1.rect.left
        if pygame.sprite.spritecollide(Jugador_2,Grupo_Barril,False):
            if Jugador_2.rect.top < Barril_2.rect.bottom and Jugador_2.rect.centerx > Barril_2.rect.left and Jugador_2.rect.centerx < Barril_2.rect.right and Jugador_2.rect.top > Barril_2.rect.top:
                Jugador_2.rect.top = Barril_2.rect.bottom
            if Jugador_2.rect.bottom > Barril_2.rect.top and Jugador_2.rect.centerx > Barril_2.rect.left and Jugador_2.rect.centerx < Barril_2.rect.right and Jugador_2.rect.bottom < Barril_2.rect.bottom:
                Jugador_2.rect.bottom = Barril_2.rect.top
            if Jugador_2.rect.left < Barril_2.rect.right and Jugador_2.rect.centery > Barril_2.rect.top and Jugador_2.rect.centery < Barril_2.rect.bottom:
                Jugador_2.rect.left = Barril_2.rect.right
                
        if Jugador_2.rect.colliderect(Linea_Central):
            Jugador_2.rect.left = Linea_Central.right
        for Bala in Grupo_Balas:
            if Jugador_1.rect.colliderect(Bala):
                Grupo_Balas.remove(Bala)
                Jugador_1.Vidas -= 1
            if Jugador_2.rect.colliderect(Bala):
                Grupo_Balas.remove(Bala)
                Jugador_2.Vidas -= 1
            if Barril_1.rect.colliderect(Bala):
                Grupo_Balas.remove(Bala)
            if Barril_2.rect.colliderect(Bala):
                Grupo_Balas.remove(Bala)

        if Jugador_1.Vidas < 1:
            Ejecutar = False
            ganador = 1
        if Jugador_2.Vidas < 1:
            Ejecutar = False
            ganador = 2
        
        pygame.display.flip()
    for player in Grupo_Jugador:
        Grupo_Jugador.remove(player)
    for Bala in Grupo_Balas:
        Grupo_Balas.remove(Bala)
    Win(ganador)

#Estructura del juego
def Main ():
    Pantalla.blit(Inicio, [0,0])
    pygame.display.flip()
    Ejecutar = True
    while Ejecutar:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Ejecutar = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if y >= 417 and y <=  487 and x >= 120 and x <= 380:
                        Ejecutar = False
                        Juego()
                if y >= 417 and y <=  487 and x >= 420 and x <= 680:
                    Ejecutar = False
Main()
