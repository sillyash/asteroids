import pygame
from utilitaires import charger_image,charger_son,afficher
from elements import Asteroide,Vaisseau,Soucoupe
from random import randint,random
from time import sleep
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
        self.missile = charger_image('missile')
        self.soucoupe = charger_image('soucoupe1')
        #charger les sons
        self.son_explosion = charger_son("explosion.wav")
        self.son_acc = charger_son("acceleration.mp3")
        self.son_missile = charger_son("son_missile.wav")
        #horloge pour le rafraîchissement de l'image
        self.horloge = pygame.time.Clock()
        #font
        self.font = pygame.font.Font(None,64)
        #Liste d'astéroides
        self.asteroides = [Asteroide(self.asteroide,self.son_explosion,(randint(0,Jeu.LARGEUR//3),randint(0,Jeu.HAUTEUR//3)),(0.5,0.5),3),\
        Asteroide(self.asteroide,self.son_explosion,(randint(2*Jeu.LARGEUR//3,Jeu.LARGEUR),randint(2*Jeu.HAUTEUR//3,Jeu.HAUTEUR)),(-0.5,-0.5),3)]
        #soucoupes
        self.soucoupes = [Soucoupe(self.soucoupe,self.son_explosion,(randint(0,Jeu.LARGEUR),randint(0,Jeu.HAUTEUR)),0)]
        #le vaisseau
        self.vaisseau =  Vaisseau(self.vaisseau_off,self.son_acc,(Jeu.LARGEUR//2,Jeu.HAUTEUR//2),self.vaisseau_on)
        #message
        self.message = "Nb vies:{}  Score:{}".format(self.vaisseau.nb_vies,self.vaisseau.score)
        SOUTIR  = pygame.event.custom_type()

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
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.vaisseau.accelerer()
            elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
                self.vaisseau.decelerer()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.vaisseau.tirer(self.missile,self.son_missile)
        dict_touches_pressees = pygame.key.get_pressed()
        if dict_touches_pressees[pygame.K_RIGHT]:
            self.vaisseau.tourner(1)
        elif dict_touches_pressees[pygame.K_LEFT]:
            self.vaisseau.tourner(-1)

    def _mettre_a_jour(self):
        #apparition d'astéroides
        if len(self.asteroides) < 3:
            self.asteroides.append(Asteroide(self.asteroide,self.son_explosion,(randint(0,Jeu.LARGEUR),0),(random(),random()),3))
        
        #invincibilité
        if self.vaisseau.invincible > 0:
            self.vaisseau.invincible -= 1
            self.vaisseau_off = charger_image('ship_off')
            self.vaisseau_on = charger_image('ship_on')
        else:
            self.vaisseau_off = charger_image('ship_off')
            self.vaisseau_on = charger_image('ship_on')  

        #déplacements
        self.vaisseau.deplacer(Jeu.LARGEUR,Jeu.HAUTEUR)
        for asteroide in self.asteroides:
            asteroide.deplacer(Jeu.LARGEUR,Jeu.HAUTEUR)
        for soucoupe in self.soucoupes:
            soucoupe.chasser(self.vaisseau)
            soucoupe.deplacer(Jeu.LARGEUR,Jeu.HAUTEUR)
            soucoupe.tirer_sur(self.missile,self.son_missile,self.vaisseau.direction)
            
        #collision vaisseau - asteroides/soucoupe
        if self.vaisseau.nb_vies > 0:
            for asteroide in self.asteroides:
                if asteroide.entrer_en_collision_avec(self.vaisseau):
                    if self.vaisseau.invincible == 0:
                        self.vaisseau.nb_vies -= 1
                        self.vaisseau.invincible = 60
                    if not(asteroide.scission()):
                        self.asteroides.remove(asteroide)
                    #asteroide.exploser(self.fenetre)
                    afficher(self.fenetre,self.message,self.font)
                    break
            for soucoupe in self.soucoupes:
                if soucoupe.entrer_en_collision_avec(self.vaisseau):
                    if self.vaisseau.invincible == 0:
                        self.vaisseau.nb_vies -= 1
                        self.vaisseau.invincible = 60
                    afficher(self.fenetre,self.message,self.font)
                    self.soucoupes.remove(soucoupe)
                    break

        #collision missile - bord
        for missile in self.vaisseau.missile:
            if missile.sortir(Jeu.HAUTEUR, Jeu.LARGEUR):
                self.vaisseau.missile.remove(missile)
                break
        for soucoupe in self.soucoupes:
            for missile in soucoupe.missile:
                if missile.sortir(Jeu.HAUTEUR, Jeu.LARGEUR):
                    soucoupe.missile.remove(missile)
                    break

        #collission missile - asteroides/soucoupes
        for missile in self.vaisseau.missile:
            for asteroide in self.asteroides:
                if asteroide.entrer_en_collision_avec(missile):
                    self.vaisseau.score += 1
                    self.vaisseau.missile.remove(missile)
                    if not(asteroide.scission()):
                        self.asteroides.remove(asteroide)
                    else:
                        self.asteroides.append(Asteroide(self.asteroide,self.son_explosion,asteroide.position,(random(),random()),3))
                        self.asteroides[len(self.asteroides)-1].scission()
                        if asteroide.taille == 1:
                            self.asteroides[len(self.asteroides)-1].scission()
                    #asteroide.exploser(self.fenetre,self.explosion)
                    afficher(self.fenetre,self.message,self.font)
                    break

            for soucoupe in self.soucoupes:
                if soucoupe.entrer_en_collision_avec(missile):
                    self.vaisseau.score += 1
                    self.vaisseau.missile.remove(missile)
                    self.soucoupes.remove(soucoupe)
                    afficher(self.fenetre,self.message,self.font)


    def _dessiner(self):
        #effacer
        self.fenetre.blit(self.fonds_ecran, (0, 0))
        #redessiner
        self.message = "Nb vies:{}  Score:{}".\
        format(self.vaisseau.nb_vies,self.vaisseau.score)
        afficher(self.fenetre,self.message,self.font)

        if self.vaisseau.nb_vies > 0:
            self.vaisseau.dessiner(self.fenetre)
            #on affiche les missiles
            for missile in self.vaisseau.missile:
                self.fenetre.blit(missile.image1_rot,missile.position)
                missile.deplacer(Jeu.LARGEUR,Jeu.HAUTEUR)

        for asteroide in self.asteroides:
            asteroide.dessiner(self.fenetre)

        #on affiche les soucoupes
        for soucoupe in self.soucoupes:
            soucoupe.dessiner(self.fenetre)
            for missile in soucoupe.missile:
                self.fenetre.blit(missile.image1_rot,missile.position)
                missile.deplacer(Jeu.LARGEUR,Jeu.HAUTEUR)
                #print(soucoupe.est_trop_proche(self.vaisseau))

        #vitesse de rafraîchissement
        self.horloge.tick(60)
        pygame.display.update()

if __name__ == "__main__":
    partie  = Jeu()
    partie.boucle_inf()
