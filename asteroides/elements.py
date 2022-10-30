import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from math import acos

class Animation:
    EST = Vector2(1,0)
    def __init__(self,image1,son,position:tuple, vitesse:tuple,image2=None):
        #image est de type Surface
        self.image1 = image1
        self.image2 = image2
        #son
        self.son = son
        #rayon du cercle circonscrit à l'image
        self.rayon = self.image1.get_width()/2
        #position du csg de l'image dans le repère de la fenêtre
        self.position = Vector2(position)
        #direction = vecteur vers l'EST à l'état initial
        self.direction = Vector2(1,0)
        #rectangle (de type Rect) entourant l'image
        self.rectangle = \
        pygame.Rect(self.position.x,self.position.y,self.rayon,self.rayon)
        #centre de l'image
        self.centre = self.position + Vector2(self.rayon)
        #vitesse de déplacement de l'Animation
        self.vitesse = Vector2(vitesse)

    def deplacer(self,largeur,hauteur):
        self.position += self.vitesse
        self.position.x = self.position.x % largeur
        self.position.y = self.position.y % hauteur
        self.centre = self.position + Vector2(self.rayon)
        self.rectangle = pygame.Rect(self.position.x,self.position.y,
        self.rayon,self.rayon)

    def dessiner(self,fenetre):
        fenetre.blit(self.image1, self.position)

    def entrer_en_collision_avec(self, other):
        distance = self.centre.distance_to(other.centre)
        return distance < self.rayon + other.rayon

class Vaisseau(Animation):
    def __init__(self,vaisseau_off,son_acc,position,vaisseau_on):
        super().__init__(vaisseau_off,son_acc,position,(0,0),vaisseau_on)
        #Nombre de vies
        self.nb_vies = 5
        self.direction = Vector2(1,0)
        self.accelere = False
        self.qte_acc = 2
        self.coeff_friction = 0.1
        self.delta_angle = 2.5
        self.taille_vaisseau = Vector2(90,90)
        self.score = 0
        self.missile = []   
      
    def accelerer(self):
        self.accelere = True
        self.vitesse += self.qte_acc*self.direction
        self.son.play()

    def decelerer(self):
        self.accelere = False
        self.vitesse -= self.coeff_friction*self.direction
        self.son.fadeout(1000)

    def tourner(self,sens):
        if sens == 1:
            self.direction.rotate_ip(self.delta_angle)
        else:
            self.direction.rotate_ip(-self.delta_angle)

    def dessiner(self,fenetre):
        if self.accelere:
            fenetre.blit(self.rot_image2,self.blit_position)
        else:
            angle = self.direction.angle_to(Animation.EST)
            self.rot_image1 = rotozoom(self.image1, angle, 1.0)
            self.rot_image2 = rotozoom(self.image2, angle, 1.0)
            taille_rot_vaisseau = Vector2(self.rot_image1.get_size())
            self.blit_position = self.position - \
            (taille_rot_vaisseau - self.taille_vaisseau)*0.5
            fenetre.blit(self.rot_image1, self.blit_position)
        
    #on ajoute un missile dans la liste missile du vaisseau
    def tirer(self,image_missile,son_tir):
        self.missile.append(Missile(image_missile,son_tir,self.position,self.vitesse,self.direction))
        son_tir.play()


class Asteroide(Animation):
    def __init__(self, image_asteroide,son_explosion,position,vitesse):
        super().__init__(image_asteroide,son_explosion,position,vitesse)

    def exploser(self,fenetre,image):
        for i in range(24):
            fenetre.blit(image,self.position,pygame.Rect(i*128,0,128,128))
        self.son.play()


class Missile(Animation):
    def __init__(self, image1, son, position: tuple, vitesse: tuple,direction, image2=None):
        super().__init__(image1, son, position, vitesse, image2)
        self.direction = direction
        self.taille_missile = Vector2(20,20)
        self.angle = self.direction.angle_to(Animation.EST)
        self.vitesse += Vector2(self.direction)*3
        self.image1 = image1
        self.qte_acc = 2
        self.image1_rot = rotozoom(self.image1,self.angle,0.3)
        self.blit_position = self.position - Vector2(90,90)*0.5
    
    def deplacer(self,hauteur,largeur):
        self.position += self.vitesse
        self.centre = self.position + Vector2(self.rayon)
        self.rectangle = pygame.Rect(self.position.x,self.position.y,
        self.rayon,self.rayon)

    def dessiner(self,fenetre):
        fenetre.blit(self.image1_rot,self.blit_position) 

    def sortir(self,hauteur,largeur):
        return (0 > self.position.x > largeur) or (0 > self.position.y > hauteur)
