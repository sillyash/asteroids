import pygame
from utilitaires import charger_image,charger_son,afficher
from elements import Asteroide,Vaisseau
from randome import randint

class Jeu:
    #attributs de classe
    LARGEUR = 800
    HAUTEUR = 600
    def __init__(self):
        self._init_pygame()
        self.fenetre = pygame.display.set_mode((Jeu.LARGEUR, Jeu.HAUTEUR))

        #charger les images
        self.fonds_ecran = charger_image('bg2')
        self.vaisseau_off = charger_image('ship_off')
        self.vaisseau_on = charger_image('ship_on')
        self.asteroide = charger_image('asteroid')
        self.explosion = charger_image('explosion')
        #charger les sons
        self.son_explosion = charger_son("explosion.wav")
        self.son_acc = charger_son("acceleration.mp3")
        #horloge pour le rafraîchissement de l'image
        self.horloge = pygame.time.Clock()
        #font
        self.font = pygame.font.Font(None,64)
        #Liste d'astéroides
        self.asteroides = [Asteroide(self.asteroide,self.son_explosion,
        (randint(0,Jeu.LARGEUR//3),randint(0,Jeu.HAUTEUR//3)),(0.5,0.5)),
         Asteroide(self.asteroide,self.son_explosion,
        (randint(2*Jeu.LARGEUR//3,Jeu.LARGEUR),randint(2*Jeu.HAUTEUR//3,Jeu.HAUTEUR)),
        (-0.5,-0.5))]
        #le vaisseau
        self.vaisseau =  Vaisseau(self.vaisseau_off,self.son_acc,
        (Jeu.LARGEUR//2,Jeu.HAUTEUR//2),self.vaisseau_on)
        #message
        self.message = "Nb vies:{}  Score:{}".format(self.vaisseau.nb_vies,
        self.vaisseau.score)


    def boucle_inf(self):
        while True:
            self._capturer_evt()
            self._mettre_a_jour()
            self._dessiner()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroides")

    def _capturer_evt(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.vaisseau.accelerer()
            elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
                self.vaisseau.decelerer()

        dict_touches_pressees = pygame.key.get_pressed()
        if dict_touches_pressees[pygame.K_RIGHT]:
            self.vaisseau.tourner(1)
        elif dict_touches_pressees[pygame.K_LEFT]:
            self.vaisseau.tourner(-1)

    def _mettre_a_jour(self):
        #déplacements
        self.vaisseau.deplacer(Jeu.LARGEUR,Jeu.HAUTEUR)
        for asteroide in self.asteroides:
            asteroide.deplacer(Jeu.LARGEUR,Jeu.HAUTEUR)

        #collision vaisseau - asteroides
        if self.vaisseau.nb_vies > 0:
            for asteroide in self.asteroides:
                if asteroide.\
                entrer_en_collision_avec(self.vaisseau):
                    self.vaisseau.nb_vies -= 1
                    afficher(self.fenetre,self.message,self.font)
                    break
        #collission missile - asteroides


    def _dessiner(self):
        #effacer
        self.fenetre.blit(self.fonds_ecran, (0, 0))
        #redessiner
        self.message = "Nb vies:{}  Score:{}".\
        format(self.vaisseau.nb_vies,
        self.vaisseau.score)
        afficher(self.fenetre,self.message,self.font)
        if self.vaisseau.nb_vies > 0:
            self.vaisseau.dessiner(self.fenetre)
        for asteroide in self.asteroides:
            asteroide.dessiner(self.fenetre)
        #vitesse de rafraîchissement
        self.horloge.tick(60)
        pygame.display.update()

if __name__ == "__main__":
    partie  = Jeu()
    partie.boucle_inf()
