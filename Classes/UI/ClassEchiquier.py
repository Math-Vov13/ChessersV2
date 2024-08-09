import pygame
Screen = None
Lettres = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] #List utilisé pour la création de l'échiquier

def draw_text(text : str, font, text_col, Pos : tuple): #Fonction pour écrire du Texte
    img = font.render(text, True, text_col)
    Screen.blit(img, Pos)

#Définition de la classe Echiquier
class Echiquier:
    #Définition des variables
    nb_lignes = int #Nombre de lignes dans l'échiquier
    nb_colonnes = int #Nombre de colonnes dans l'échiquier
    taille_case = int #Taille d'une case en pixels
    taille_bordure = int #Taille de la bordure de l'échiquier en pixels
    taille_x = int #Taille en pixels de la largeur de l'échiquier
    taille_y = int #Taille en pixels de la hauteur de l'échiquier
    fenetre_echiquier = pygame.Surface

    #Définitions des fonctions

    #Initialisation de la classe
    def __init__(self, Lignes, Case, Bordure):
        #Initialisation des varaibles de l'échiquier
        self.nb_lignes = Lignes
        self.nb_colonnes = Lignes
        self.taille_case = Case
        self.taille_bordure = Bordure
        self.CasesPositions = {} #Dict qui contient les positions des Cases
        self.PiecesPositions = {}

        self.Background = None
        self.ListCases = []
        self.ListTexts = []

        #Initialisation de la taille de la fenêtre
        self.taille_x = Lignes * Case + 2 * Bordure
        self.taille_y = Lignes * Case + 2 * Bordure
        self.fenetre_echiquier = pygame.display.set_mode((self.taille_x, self.taille_y))

    #Dessine l'échiquier
    def Create(self,Couleur1, Couleur2, CouleurBordure):
        x = int
        y = int
        Ltr = str #Lettre
        Nombre = 0 #Nombre


        Background = pygame.Rect(50, 50, 700, 700)
        pygame.draw.rect(self.fenetre_echiquier, CouleurBordure, Background)
        self.Background = Background
        self.ListCases.append((self.fenetre_echiquier, CouleurBordure, Background))

        #self.fenetre_echiquier.fill(CouleurBordure)

        NbrTxt1 = 60
        for i in range(self.nb_lignes):                                                                     #Lettres
            Nombre = self.nb_lignes - i
            self.ListTexts.append((str(Nombre), pygame.font.SysFont("timesnewroman", 30), (0, 0, 0), (5 + Background.x, NbrTxt1 + Background.y)))   #Création de la Bordure Gauche
            NbrTxt1 += 80
            y = self.taille_bordure + i * self.taille_case
            NbrTxt2 = 60
            for j in range(self.nb_colonnes):                                                               #Nombres
                Ltr = Lettres[j]
                self.ListTexts.append((str(Ltr), pygame.font.SysFont("timesnewroman", 30), (0, 0, 0), (NbrTxt2 + Background.x, 670 + Background.y)))#Création de la Bordure du Bas
                NbrTxt2 += 80

                x = self.taille_bordure + j * self.taille_case
                Case_echiquier = pygame.Rect((x + Background.x, y + Background.y), (self.taille_case, self.taille_case))

                if (i + j) % 2 == 0:
                    #dessine une case de la couleur 1
                    #pygame.draw.rect(self.fenetre_echiquier, Couleur1, Case_echiquier)
                    self.ListCases.append((self.fenetre_echiquier, Couleur1, Case_echiquier))
                else:
                    #Dessine une case de la couleur 2
                    #pygame.draw.rect(self.fenetre_echiquier, Couleur2, Case_echiquier)
                    self.ListCases.append((self.fenetre_echiquier, Couleur2, Case_echiquier))


                Name = Ltr + str(Nombre)
                MilieuX = x + (self.taille_case + 10)
                MilieuY = y + (self.taille_case + 50)
                self.CasesPositions[(MilieuX, MilieuY)] = [Name, None] #{ (Position de la Case) : [Nom de la Case, Objet dessus] }
                self.PiecesPositions[(MilieuX, MilieuY)] = None
                #print(self.CasesPositions)
        
        print(self.CasesPositions)

    def Get_Positions(self): #Efface toutes les Positions de la Partie (est utilisé lors du reset de la partie)
        return self.CasesPositions
    
    def UpdateBoard(self):
        for Case in self.ListCases:
            pygame.draw.rect(Case[0], Case[1], Case[2])
            #pygame.draw.rect(self.fenetre_echiquier, (255,0,0), pygame.Rect((80, 80), (self.taille_case, self.taille_case))) #A8
    
        for Text in self.ListTexts:
            draw_text(Text[0], Text[1], Text[2], Text[3])