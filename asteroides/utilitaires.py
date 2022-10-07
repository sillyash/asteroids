from pygame.image import load
from pygame.mixer import Sound
from pygame import Color
from pygame.math import Vector2

def charger_image(nom):
    chemin = "../ressources/images/{}.png".format(nom)
    #l'image chargée est de type Surface
    surface = load(chemin)
    return surface.convert_alpha()

def charger_son(nom):
    chemin = "../ressources/sons/{}".format(nom)
    return Sound(chemin)

def afficher(fenetre,texte,font,couleur=Color("red")):
    surf = font.render(texte, True, couleur)
    rect = surf.get_rect()
    rect.center = Vector2(220,30)
    fenetre.blit(surf, rect)