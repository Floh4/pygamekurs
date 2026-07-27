# Import statements
import pygame
import sys

# initialisieren von Pygame
pygame.init()

pygame.display.set_caption("Pong") # Titelname zu "Pong" machen

class Vector:
    """
    dadurch kann man position von den Spielern und dem Ball besser angeben
    Vergleich:
        ball.pos[1] mit ball.pos.y
    """

    def __init__(self, x = 0, y = 0):
        """Variabeln von den jeweils eingefügten klassen definieren"""
        self.x = x
        self.y = y

    def get_as_list(self):
        """Die position immer noch als liste ([0, 0]) bekommen"""
        return (self.x, self.y)

class Player:
    def __init__(self, pos = (10, 10), size = (10, 10)):
        """
        Anfangsattribute für die Klasse Player (Die Spieler in pong)
        Alle Paremeter:
            pos:Position vom Spieler wenn er am 
                Anfang geladen wird als tuple (liste in normalen klammer und unveränderlich) eingeben
            
            Size: Die größe vom Spieler als tuple (liste in normalen klammer und unveränderlich)
        """
        self.pos = Vector(pos[0], pos[1]) # Damit man player.pos.x und player.pos.y hat
        self.size = list(size) # Die größe als liste -> [breite vom Spieler, länge vom Spieler]
        self.rectangle = pygame.Rect(self.pos.get_as_list(), self.size) # spieler als rechteck initieren mithilfe von pygame
        self.middle_point = (self.pos.y + (self.size[1] / 2))          # Für abprall in verschiedene Richtungen
        self.left_top = self.pos.x # von wo die position vom Spieler ausgeht (von der oberen linken ecke)

    def draw(self, screen):
        """
        Zeichnet den Spieler auf den Bildschirm (bildschirm als parameter noch angeben)
        (nur den Spieler da es draw eine Klasse von Player ist)
        diese funktion wird aber selten alleine verwendet sondern ist eine
        Unterfunktion von update() da update() diese funktion enthält
        """

        # pygame.draw.rect(welcher bildschirm, (rot, grün, blau), welches rechteck)
        pygame.draw.rect(screen, (255, 255, 255), self.rectangle)
    
    def move(self, relative_y):
        self.pos.y -= relative_y  # bewegt den ball 
    
    def update(self, screen):
        """
        updated die Attribute vom Spieler UND zeichnet den spieler mithilfe von der draw funktion
        Paramenter: welcher Bildschirm eingeben
        """
        self.rectangle = pygame.Rect(self.pos.get_as_list(), self.size) # neues rechteck mit den richtigen positionen und größen
        self.middle_point = (self.pos.y + (self.size[1] / 2)) # mittelpunkt neu berechnen (wichtig für ball abprall)
        self.draw(screen) # Spieler zeichnen

class Ball:
    def __init__(self, pos = (425, 250), velocity = (0, 0), radius = 7):
        """
        Anfangsattribute von der Klasse Ball (dieser ball in pong)
        Parameter:
            pos: Position vom Ball als tuple angeben
            velocity: Geschwindigkeit als tuple angeben, (x geschwindigkeit, y geschwindigkeit)
            radius: Radius vom Ball

        Speziell zur Ball velocity:
            Je nachdem ob die beiden velocity werte negativ oder positiv sind 
            bewegt sich der ball in eine andere richtung:
            Hier alle 4 Arten wie sich der Ball bewegen kann:
                - Velocity ist... :
                    - (positiv, positiv) -> ball fliegt oben links
                    - (negativ, positiv) -> ball fliegt unten links
                    - (positiv, negativ) -> ball fliegt rechts oben
                    - (negativ, negativ) -> ball fliegt rechts unten
        """
        self.pos = Vector(pos[0], pos[1]) # somit ball.pos.y, ball.pos.x
        self.velocity = Vector(velocity[0], velocity[1]) # damit hat man ball.velocity.x und ball.velocity.y
        self.radius = radius # somit hat ball.radius einen wert
        self.hitbox = pygame.Rect( # unsichtbare hitbox für den ball (einfach nur ein Rechteck)
            self.pos.x - self.radius,
            self.pos.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def draw(self, screen):
        """ball wird auf dem jeweiligen Bildschirm gezeichnet"""
        pygame.draw.circle(screen, (255, 255, 255), self.pos.get_as_list(), self.radius)
    
    def move(self, relative_x, relative_y):
        """Um wie viel der Ball sich von seiner jetzigen Position bewegen soll"""
        self.pos.x += relative_x 
        self.pos.y += relative_y

    def hitbox_follow(self):
        """
        die Mitte von der Hitbox vom Ball soll die position vom jetzigen ball betragen
        -> somit verfolgt die Hitbox den Ball
        """
        self.hitbox.center = (self.pos.x, self.pos.y)
    
    def draw_hitbox(self, screen):
        """hitbox rot zeichnen für debugging (Fehlerbehebung)"""
        pygame.draw.rect(screen, "red", self.hitbox, 1) # * Nur zum debuggen

def accelerate_ball(ball_pong, diff_player_ball, geschwindigkeitsgrenze): # * Beschleunigt Ball
    """
    ETWAS KOMPLEXERE FUNKTION:
    accelerate_ball ist eine normal funktion und gehört keiner klasse
    Es verwendet den Abstand zwischen der Mitte des balles und die mitte des spielers (deswegen auch player.middle_point)
    um den Ball anders abprallen zu lassen wenn er auf die Seite des Spielers kommt
    Parameter:
        ball_pong:
            - welcher ball
        diff_player_ball:
            - der abstand zwischen ball mitte und spieler mitte
        geschwindigkeitsgrenze:
            - ab wann soll den nicht weiter beschleunigt werden
    """

     # * Nur wenn der Ball an den äußeren Enden vom Spieler trift, prallt der Ball in einem Winkel ab (Optional)

     # die bedingung schaut ob beide geschwindigkeiten unter der Geschwindigkeits grenze sind 
     # und das der abstand von diff player ball größer ist als 20
     # desto größer der wert von diff_player_ball ist desto mehr wurde der ball an der Seite getroffen
    if ((abs(ball_pong.velocity.x) < geschwindigkeitsgrenze and abs(ball_pong.velocity.y) < geschwindigkeitsgrenze) and abs(diff_player_ball) > 20 ):
        if ball_pong.velocity.x > 0: # je nachdem ob die velocity negativ oder positiv war wird dann soviel hinzugefügt
            ball_pong.velocity.x += 2
        else:
            ball_pong.velocity.x -= 2
        ball_pong.velocity.y += 0.1 * ((diff_player_ball - 10) * -0.1)  # * Wirkungsgrad wie stark es wirken soll mit dem Winkel verändern
    # Falls das erste falsch war und nicht ging dann wird einfach eine generelle beschleunigung hinzugefügt und nichts mit dem je nach winkel wie es sich bewegen soll
    elif (ball_pong.velocity.x < geschwindigkeitsgrenze and ball_pong.velocity.y < geschwindigkeitsgrenze): # das ist für spieler
        if ball_pong.velocity.x > 0:
            ball_pong.velocity.x += 2
        else:
            ball_pong.velocity.x -= 2
        ball_pong.velocity.y += 0.1

def keybind(key_pygame_up, key_pygame_down, player, spielergeschwindigkeit, screen_height, player_height): 
    """
    Für die Kontrolle von den Spielern mithilfe von Tasten
    Parameter:
        key_pygame_up: welche taste gedrückt werden muss damit der spieler sich nach oben bewegt
        key_pygame_down: welche taste gedrückt werden muss damit der spieler sich nach unte bewegt
        player: welcher spieler überhaupt von den beiden
        spielergeschwindigkeit: selbsterklärend
        screen_height: höhe vom Bildschirm, die konstante die wird dazu definiert haben
        player_height: höhe vom spieler, auch die eine konstante
    """
    key = pygame.key.get_pressed()
    if key[key_pygame_up] and player.pos.y > 0: # * damit der ball an der decke nicht runter geht
        player.move(spielergeschwindigkeit)
    if key[key_pygame_down] and player.pos.y < screen_height - player_height: # * damit der ball an dem boden nicht runter geht
        player.move(-spielergeschwindigkeit)

def handle_exit():
    """wenn man auf fenster schließen klickt damit es auch wirklich schließt"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
