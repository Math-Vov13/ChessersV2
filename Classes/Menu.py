"""Import des Bibliothèques"""
import pygame
import webbrowser
from Classes.UI import ClassBouton, ClassInputBox, ClassEchiquier
from Classes import MainGame, ClassTimer, DataBase

"""Variables"""
#Menu
Clock = pygame.time.Clock()     #Initialise le Timer de Pygame
FPS = 60                        #FPS (=Images Par Seconde)
Running = True                  #Boucle du Jeu
ObjClicked = False              #Objet cliqué par la souris
AfficheBtn = []                 #Pour afficher les boutons du Menu
level = 1                       #Niveau de progression du menu

#Sounds
SoundGame = pygame.mixer.Sound("Sounds/chess_game.mp3")   #Charge le Son du Jeu
SoundMenu = pygame.mixer.Sound("Sounds/chess_menu.mp3")   #Charge le son du Menu
SoundPop = pygame.mixer.Sound("Sounds/pop.mp3")           #Charge le son des boutons
pygame.mixer.music.set_volume(30)                       #Définit le volume de la musique
Son = True                                              #Active la Musique

#Partie
GameInfos = MainGame.GameInfos  #Récupère les Infos de la Partie
GameMode = str                  #Le Mode de Jeu choisi
PlrMode = str                   #Le Mode Joueur choisi (Pvp / PvE)

#Joueurs
PseudoJ1 = "Jean"               #Pseudo du Joueur 1
PseudoJ2 = "Paul"               #Pseudo du Joueur 2
MDPJ1 = ""                      #Pour Sauvegarder
CouleurJ1 = "Blanc"             #Couleur Joueur1
CouleurJ2 = "Noir"              #Couleur Joueur2

#Timer
# PlrTimer = ClassTimer.Timer()
# GameTimer = 0
# TimerStarted = False
# StartTimer = 0
# LastTime = 0                    #Pour le Timer
# LastSec = 0                     #Pour le Timer
# TimerPaused = False             #Si le Timer est actif ou non


"""Création de la Fenêtre de Jeu"""
pygame.init()
pygame.display.init()

screen = pygame.display.set_mode((800, 800)) #Création de la fenêtre
screen.fill((33, 27, 33))     #Couleur du Fond d'ecran
pygame.display.set_caption("Chessers") #Définit le Nom de la fenêtre
icon = pygame.image.load('Images/Logo.png') #Défini le Logo de la fenêtre
pygame.display.set_icon(icon) #Affiche le Logo de la fenêtre
MainGame.ActualScreen = screen
MainGame.GameInfos.GameTimerObj = ClassTimer.Timer()
MainGame.GameInfos.Player1Timer = ClassTimer.Timer()
MainGame.GameInfos.Player2Timer = ClassTimer.Timer(True)
ClassEchiquier.Screen = screen

Background = pygame.image.load('Images/Background.png')
Background = pygame.transform.scale(Background, (800, 800))
Logo = pygame.image.load('Images/Logo Chessers Blanc.png')

def draw_text(text : str, font, text_col, Pos : tuple): #Fonction pour écrire du Texte
    img = font.render(text, True, text_col)
    screen.blit(img, Pos)


#Polices du Jeu
Titre_Menu = pygame.font.SysFont("courier new",90)
Police_Pause = pygame.font.SysFont("brushscriptitalique",30)
Titres = pygame.font.SysFont("arialroundedmtbold",60)
TitreTxt = pygame.font.SysFont("britannicbold",40, True)
Txt = pygame.font.SysFont("timesnewroman",20)

#define colors
BlackColor = (255, 255, 255)
RedColor = (255,0,0)

#Charge les Images
black_image = pygame.image.load("Images/Boutons/black.png").convert_alpha()
white_image = pygame.image.load("Images/Boutons/white.png").convert_alpha()
restart_image = pygame.image.load("Images/Boutons/restart.png").convert_alpha()
continue_image = pygame.image.load("Images/Boutons/continue.png").convert_alpha()
back_image = pygame.image.load("Images/Boutons/back_menu.png").convert_alpha()
micon_image = pygame.image.load('Images/Boutons/mic.png').convert_alpha()
micoff_image = pygame.image.load("Images/Boutons/mic_off.png").convert_alpha()
return_image = pygame.image.load("Images/Boutons/return.png").convert_alpha()

ImgTEST = pygame.image.load("Images/Boutons/BOUTON.png").convert_alpha()
play_img = pygame.image.load("Images/Boutons/Jouer.png").convert_alpha()
stats_img = pygame.image.load("Images/Boutons/Stats.png").convert_alpha()
actus_img = pygame.image.load("Images/Boutons/Actus.png").convert_alpha()
Pvp_img = pygame.image.load("Images/Boutons/Pvp.png").convert_alpha()
Ia_img = pygame.image.load("Images/Boutons/Ia.png").convert_alpha()
PvpN_img = pygame.image.load("Images/Boutons/Mode_Normal_Pvp.png").convert_alpha()
PvpTr_img = pygame.image.load("Images/Boutons/Mode_Tradition.png").convert_alpha()
PvpU_img = pygame.image.load("Images/Boutons/Mode_UsVsUk.png").convert_alpha()
Timer_img = pygame.image.load("Images/Boutons/Mode_Timer.png").convert_alpha()
PveN_img = pygame.image.load("Images/Boutons/Mode_Normal_IA.png").convert_alpha()
PveA_img = pygame.image.load("Images/Boutons/Mode_Assist.png").convert_alpha()

TimerP1_img = pygame.image.load("Images/Boutons/TimerP1.png").convert_alpha()
TimerP2_img = pygame.image.load("Images/Boutons/TimerP2.png").convert_alpha()

#Créer les Boutons du Menu
Play_Btn = ClassBouton.BoutonMenu((130, 280), (250, 200), play_img, "", 1)           #Bouton Jouer
Stats_Btn = ClassBouton.BoutonMenu((420, 280), (250, 200), stats_img, "", 0)          #Classements
Actus_Btn = ClassBouton.BoutonMenu((100, 500), (600, 200), actus_img, "", 0)          #Actualités

PvP_Btn = ClassBouton.BoutonMenu((200, 300), (400, 175), Pvp_img, "", 1)            #Jouer Contre un Joueur
PvE_Btn = ClassBouton.BoutonMenu((200, 500), (400, 175), Ia_img, "", 2)            #Jouer Contre l'IA

PVP_Normal_Btn = ClassBouton.BoutonMenu((75, 300), (300, 175), PvpN_img, "", 1)
PVP_Tradition_Btn = ClassBouton.BoutonMenu((425, 300), (300, 175), PvpTr_img, "", 1)
PVP_USA_Btn = ClassBouton.BoutonMenu((75, 500), (300, 175), PvpU_img, "", 1)
PVP_Timer_Btn = ClassBouton.BoutonMenu((425, 500), (300, 175), Timer_img, "", 1)

PVE_Normal_Btn = ClassBouton.BoutonMenu((75, 300), (300, 175), PveN_img, "", 1)
PVE_Assist_Btn = ClassBouton.BoutonMenu((425, 300), (300, 175), PveA_img, "", 1)
PVE_Timer_Btn = ClassBouton.BoutonMenu((250, 500), (300, 175), Timer_img, "", 1)

WhiteP_Btn = ClassBouton.BoutonMenu((205, 170), (100, 100), white_image, "", 1)
BlackP_Btn = ClassBouton.BoutonMenu((205, 330), (100, 100), black_image, "", 1)
Return_Btn1 = ClassBouton.BoutonMenu((205, 535), (100, 100), return_image, "", -1)
Return_Btn2 = ClassBouton.BoutonMenu((250, 330), (150, 100), return_image, "", -1)
Continue_Btn = ClassBouton.BoutonMenu((275, 200), (250, 100), continue_image, "", 0)
Reset_Btn = ClassBouton.BoutonMenu((275, 330), (250, 100), restart_image, "", 0)
RMenu_Btn = ClassBouton.BoutonMenu((275, 460), (250, 100), back_image, "", 0)
RMenu_Btn2 = ClassBouton.BoutonMenu((275, 325), (250, 100), restart_image, "", 0)

TimerP1 = ClassBouton.BoutonMenu((750, 200), (40, 400), TimerP1_img, "", 0)
TimerP2 = ClassBouton.BoutonMenu((750, 200), (40, 400), TimerP2_img, "", 0)

MicOn_Btn = ClassBouton.BoutonMenu((669, 2), (30, 30), micon_image, "Sound", 0)
MicOff_Btn = ClassBouton.BoutonMenu((669, 2), (30, 30), micoff_image, "Sound", 0)


#Etapes du Menu
ListBoutons = []
ListBoutons.append([])    #Rien (0)
ListBoutons.append([Play_Btn, Stats_Btn, Actus_Btn]) #Ecran Menu (1)
ListBoutons.append([PvP_Btn, PvE_Btn]) #Ecran Menu (2)
ListBoutons.append([PVP_Normal_Btn, PVP_Tradition_Btn, PVP_USA_Btn, PVP_Timer_Btn]) #Ecran Menu (3)
ListBoutons.append([PVE_Normal_Btn, PVE_Assist_Btn, PVE_Timer_Btn]) #Ecran Menu (4)
ListBoutons.append([]) #Partie (5)
ListBoutons.append([Continue_Btn, RMenu_Btn, Reset_Btn]) #Menu de Pause (6)
ListBoutons.append([RMenu_Btn2]) #Partie Terminée (7)

ListTexts = []


def VerifObjectHitBox(List, MousePos):
    for Object in List:
        if Object.HasHitBox == False:                               #Savoir si l'Objet a une HitBox ou Non
            continue                                                #Reprends depuis la boucle for
        if Object.HitBox.collidepoint(MousePos):                    #Si la Souris est entrée en colision avec la HitBox de l'Objet
            return Object                                           #Renvoie l'Objet Cliqué
    return False                                                    #Retourne false si il n'y a aucun Objet
        
"""Fonctions pour le Timer"""
def ResetTimer(): #Remet le Timer à 0
    global TimerStarted
    if MainGame.GameInfos.GameTimerObj.state != "stopped":
        MainGame.GameInfos.GameTimerObj.stop()
    MainGame.GameInfos.GameTimerObj.run(pygame.time.get_ticks()) # Start
    TimerStarted = True

def ContinueTimer(): #Continue le Timer
    pass
    #global TimerPaused, LastTime
    #if GameMode == "Timer":
    #    TimerPaused = False

def TimeFormat(Time : int) -> str:
    if Time%60 >= 10:
        return str(int(Time//60)) + " :" + str(int(Time%60))
    else:
        return str(int(Time//60)) + " :0" + str(int(Time%60))

"""Sounds"""
def PlaySound(Sound): #Joue un Son
    if Son == True:
        Sound.play()


def ResetGm(Visible : bool):
    GameInfos.Player1["Pseudo"] = PseudoJ1
    GameInfos.Player1["Couleur"] = CouleurJ1    #Défini la Couleur du J1
    GameInfos.Player2["Pseudo"] = PseudoJ2
    GameInfos.Player2["Couleur"] = CouleurJ2    #Défini la Couleur du J2
    GameInfos.GameMode = GameMode               #Met le Mode de Jeu choisi
    GameInfos.PlrMode = PlrMode                 #Met le Mode de Joueur choisi
    GameInfos.ResetGame(Visible)                #Initialise les autres paramètres de la Partie
    ResetTimer()                                #Remet le Timer à 0



def ChangeEtape(LvlAdded : int):
    global level
    print(ListBoutons[level])
    for Object in ListBoutons[level]:
        if Object in AfficheBtn:
            Index = AfficheBtn.index(Object)
            AfficheBtn.pop(Index)
    level += LvlAdded
    #print(level, len(ListBoutons), level >= len(ListBoutons))
    if level >= len(ListBoutons): #Arrêt du programme car Bug dans le Menu ! 
        global Running
        Running = False
        return
    
    for Object in ListBoutons[level]:
        AfficheBtn.append(Object)
    
    ListTexts.clear()

def UpdateMenuFrame(AddLvl : int):
    global level, GameMode, PlrMode

    print("Niveau Actuel :", level)

    """Level du Menu"""
    if level == 1: #Menu d'Entrée
        GameInfos.InMenu = True
        if MainGame.GameInfos.GameTimerObj.state != "stopped":
            MainGame.GameInfos.GameTimerObj.stop()
            if MainGame.GameInfos.GameMode == "Timer":
                try:
                    MainGame.GameInfos.Player1Timer.stop()
                except:
                    pass
                try:
                    MainGame.GameInfos.Player2Timer.stop()
                except:
                    pass
        GameInfos.GameStarted = False
        """if GameInfos.SoundPlaying == "" or GameInfos.SoundPlaying != "Menu": #Lance la musique
            SoundGame.stop()
            GameInfos.SoundPlaying = "Menu"
            SoundMenu.play(100,0,4000)
            if Son == False :
                pygame.mixer.pause()"""

        if Play_Btn.clicked == True:          #Bouton Jouer
            Play_Btn.ResetClick()
            ChangeEtape(AddLvl)
            #Aller à Connexion
        
        else:
            if Stats_Btn.clicked == True:
                Stats_Btn.ResetClick()
                webbrowser.open("http://localhost/Sites%20Perso/Chessers/Pages/classement.php")
            elif Actus_Btn.clicked == True:
                Actus_Btn.ResetClick()
                webbrowser.open("https://www.europe-echecs.com/actualites.html")
    
    if level == 2: #Choix de la Couleur

        if PvP_Btn.clicked == True: #Bouton Pièces Noires
            PvP_Btn.ResetClick()
            ChangeEtape(AddLvl)
 
        elif PvE_Btn.clicked == True: #Bouton Pièces Blanches
            PvE_Btn.ResetClick()
            ChangeEtape(2)

    if level == 3: #Choix du Mode de Jeu
        
        ListTexts.append(("Choix du Mode de Jeu", Titres, BlackColor, (115, 45)))
        PlrMode = "PvP"

        if PVP_Normal_Btn.clicked == True: #Bouton Mode de Jeu Classique
            
            GameMode = "Normal"
            PVP_Normal_Btn.ResetClick()
            ChangeEtape(2)
            AddLvl = 0
            ResetGm(True)
        
        elif PVP_Tradition_Btn.clicked == True: #Bouton Mode de Jeu USAVSUK
            
            GameMode = "Tradition"
            PVP_Tradition_Btn.ResetClick()
            ChangeEtape(2)
            AddLvl = 0
            ResetGm(True)
        
        elif PVP_USA_Btn.clicked == True: #Bouton Mode de Jeu Timer
            
            GameMode = "USA/UK"
            PVP_USA_Btn.ResetClick()
            ChangeEtape(2)
            AddLvl = 0
            ResetGm(True)
        
        elif PVP_Timer_Btn.clicked == True: #Bouton Mode de Jeu Timer
            
            GameMode = "Timer"
            PVP_Timer_Btn.ResetClick()
            ChangeEtape(2)
            AddLvl = 0
            ResetGm(True)
        
        """elif Return_Btn1.clicked == True: #Bouton Retour en Arrière
            
            Return_Btn1.ResetClick()
            ChangeEtape(AddLvl)
            UpdateMenuFrame(0)"""
   
    if level == 4: #Confirmation des Parmètres
        
        PlrMode = "PvE"

        if PVE_Normal_Btn.clicked == True: #Bouton Lancement de la Partie
            
            GameMode = "Normal"
            PVE_Normal_Btn.ResetClick()
            ChangeEtape(AddLvl)
            AddLvl = 0
            ResetGm(True)
        
        elif PVE_Assist_Btn.clicked == True: #Bouton Lancement de la Partie
            
            GameMode = "Assist"
            PVE_Assist_Btn.ResetClick()
            ChangeEtape(AddLvl)
            AddLvl = 0
            ResetGm(True)
        
        elif PVE_Timer_Btn.clicked == True: #Bouton Lancement de la Partie
            
            GameMode = "Timer"
            PVE_Timer_Btn.ResetClick()
            ChangeEtape(AddLvl)
            AddLvl = 0
            ResetGm(True)

    
    if level == 5: #Menu Pause
        if GameMode == "Timer":                           #Si le Mode de Jeu Timer est activé, alors changer la position du texte pour laisser place au Timer
            if GameInfos.GamePaused == True and GameInfos.Winner == "":
                ListTexts.append(("Pressez la Barre Espace pour Continuer la Partie", Police_Pause, BlackColor, (180, -5)))
            elif GameInfos.GamePaused == False and GameInfos.Winner == "":
                ListTexts.append(("Pressez la Barre Espace pour mettre Pause", Police_Pause, BlackColor, (210, -5)))
        else:                                       #Si le Mode de Jeu n'est pas le Timer, alors mettre à la place normal
            if GameInfos.GamePaused == True and GameInfos.Winner == "":
                ListTexts.append(("Pressez la Barre Espace pour Continuer la Partie", Police_Pause, BlackColor, (125, -5)))
            elif GameInfos.GamePaused == False and GameInfos.Winner == "":
                ListTexts.append(("Pressez la Barre Espace pour mettre Pause", Police_Pause, BlackColor, (135, -5)))

        ChangeEtape(AddLvl)

    if level == 6: #Menu Pause

        if GameInfos.GamePaused == False and GameInfos.InMenu == False:
            ChangeEtape(AddLvl)
            UpdateMenuFrame(0)
            return
        
        """if GameInfos.SoundPlaying == "Game":
            SoundGame.stop()
            GameInfos.SoundPlaying = "Menu"
            SoundMenu.play(100,0,4000)
            if Son == False :
                pygame.mixer.pause()"""
        
        if Continue_Btn.clicked == True:            #Bouton Continuer
            #SoundMenu.stop()
            Continue_Btn.ResetClick()
            """GameInfos.SoundPlaying = "Game"
            SoundGame.play(100,0,4000)
            if Son == False :
                pygame.mixer.pause()"""
            GameInfos.GamePaused = False
            UpdateMenuFrame(-1)

        elif Reset_Btn.clicked == True:                #Bouton Recommencer
            #SoundMenu.stop()
            Reset_Btn.ResetClick()
            """GameInfos.SoundPlaying = "Game"
            SoundGame.play(100,0,4000)
            if Son == False :
                pygame.mixer.pause()"""
            GameInfos.GamePaused = False
            GameInfos.ResetGame(True)
            ResetTimer()
            UpdateMenuFrame(-1)

        elif RMenu_Btn.clicked == True:              #Bouton Retour Menu
            global TimerStarted
            RMenu_Btn.ResetClick()
            GameInfos.ResetGame(False)
            TimerStarted = False
            ChangeEtape(-5)
            UpdateMenuFrame(0)
    
    print("Niveau Après :", level)

    if level == 7: #Si Partie Finie
        ListTexts.append((str(GameInfos.Winner).upper() + ' a gagné', Titres, RedColor, (250, 250)))

        if GameInfos.SoundPlaying == "Game":
            """SoundGame.stop()
            GameInfos.SoundPlaying = "Menu"
            SoundMenu.play(100,0,4000)
            if Son == False :
                pygame.mixer.pause()"""

        if RMenu_Btn2.clicked == True: #Bouton Recommencer
            RMenu_Btn2.ResetClick()
            GameInfos.ResetGame(False)
            ChangeEtape(-6)
            UpdateMenuFrame(0)

# """Récupération Données local"""
# with open('Data.txt', 'r') as fichier:	#Ouvre le fichier text
#     contenu = fichier.read()			#Lis le contenu du fichier
#     Data = json.loads(contenu)			#Permet de retranscrire un dict dans un str en dict

# PseudoJ1 = Data["Pseudo"]
# MDPJ1 = Data["MDP"]
# print(type(Data), Data)
# print(type(contenu), contenu)

PseudoJ1 = "Moi"
MDPJ1 = "Hello, World!"

"""Initialise l'écran de début"""
for Object in ListBoutons[level]:
    AfficheBtn.append(Object)
ListBoutons.append(MicOn_Btn)


"""Jeu"""
while Running == True: #Boucle Principal
    Clock.tick(FPS) #FPS
    #screen.fill((33, 27, 33))     #Couleur du Fond d'ecran

    """Affichage des différents éléments à l'écran"""
    if GameInfos.InMenu == True:
        screen.blit(Background, (0, 0)) #Affiche l'Arrière Plan
        screen.blit(Logo, (150, 15))   #Affiche le Logo
    
    else:
        screen.fill((33, 27, 33))
        GameInfos.Echiquier.UpdateBoard()
        draw_text(TimeFormat(MainGame.GameInfos.GameTimerObj.getTime()), Titres, BlackColor, (600, 5))		#Affiche le Temps de la Partie
        draw_text(PseudoJ1, Titres, BlackColor, (600, 750))	#Affiche le Nom du J1
        draw_text(PseudoJ2, Titres, BlackColor, (50, 5))		#Affiche le Nom du J2
        if GameInfos.GameMode == "Timer":
            draw_text(TimeFormat(MainGame.GameInfos.Player1Timer.getTime()), Titres, BlackColor, (400, 750))
            draw_text(TimeFormat(MainGame.GameInfos.Player2Timer.getTime()), Titres, BlackColor, (300, 5))

    for Object in MainGame.ListAfficheObj:    #Boucle qui affiche à l'écran chaque éléments dans la List
        screen.blit(Object.Image, Object.HitBox)
    
    for Button in AfficheBtn:
        screen.blit(Button.Image, Button.HitBox)
    
    for Text in ListTexts:
        draw_text(Text[0], Text[1], Text[2], Text[3])


    """Autre Evènements"""
    if GameInfos.GameEnded == True and GameInfos.Winner != "": #Echecs et Maths
        GameInfos.GameEnded = False
        TimerStarted = False
        print("Pris en compte")
        UpdateMenuFrame(2)
    
    """if GameInfos.PlrMode == "PvE" and GameInfos.Tour["Couleur"] == GameInfos.Player2["Couleur"] :
        from Classes import AI_Chess as IA
        #if GameInfos.GameMode == "Assist" and GameInfos.Tour["Couleur"] != GameInfos.Player2["Couleur"] or GameInfos.Tour["Couleur"] == GameInfos.Player2["Couleur"]:
        Piece, Pos, Situation, CP = IA.FindBestMove(GameInfos.Positions, MainGame.ObjetPieces, MainGame.CouleurPieces, GameInfos.Tour["Couleur"], GameInfos.NextColor(GameInfos.Tour["Couleur"]), 3)
        print("Le meilleur mouvement est :", Pos)
        print("La situation est :", Situation)
        print("La pièce qui effectue le meilleur mouvement est :", Piece)
        Piece.NewPosition(Pos, Situation, CP)"""

    if Son == True : #Si le Son est activé
        if MicOn_Btn.clicked == True : #Désactive le Son
            MicOn_Btn.ResetClick()
            pygame.mixer.pause()
            ListBoutons.pop(ListBoutons.index(MicOn_Btn))
            ListBoutons.append(MicOff_Btn)
            Son = False

    else: #Si le son est Désactivé
        if MicOff_Btn.clicked == True: #Réactive le Son
            MicOff_Btn.ResetClick()
            pygame.mixer.unpause()
            ListBoutons.pop(ListBoutons.index(MicOff_Btn))
            ListBoutons.append(MicOn_Btn)
            Son = True
    

    "Evènements du Jeu"
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quand la fenêtre est fermé
            Running = False #arrête la boucle
            break
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            MousePos = pygame.mouse.get_pos()
            #print("Début Clique")
            #print(pygame.mouse.get_pos())
            ObjClicked = VerifObjectHitBox(AfficheBtn, MousePos)
            if not ObjClicked:
                ObjClicked = VerifObjectHitBox(MainGame.ListAfficheObj, MousePos)
            #print(ObjClicked)
        
        elif event.type == pygame.MOUSEBUTTONUP: #Quand le clique de la Souris est remonté
            MousePos = pygame.mouse.get_pos()
            #print("Fin Clique")
            #print(pygame.mouse.get_pos())
            VerifMouse = VerifObjectHitBox(AfficheBtn, MousePos)
            if not VerifMouse:
                VerifMouse = VerifObjectHitBox(MainGame.ListAfficheObj, MousePos)
            #print(VerifMouse)

            if ObjClicked == VerifMouse and ObjClicked != False:        #Si le Joueur a cliqué sur un Objet
                Obj = ObjClicked
                #print("Un Objet vient d'être cliqué !!")
                #print(VerifMouse)
                #GameInfos.PSelected = Obj

                Obj.Clicked()
                if isinstance(Obj, ClassBouton.BoutonMenu):
                    PlaySound(SoundPop)
                    if Obj.Utility == "":
                        UpdateMenuFrame(Obj.AddLvl)
            else:                                                       #Si le Joueur a cliqué dans le vide
                #print("Cliqué à côté !")
                if GameInfos.GameStarted == True and GameInfos.GamePaused == False:
                    #print("Reset Cases")
                    GameInfos.ClearCases()



        elif event.type == pygame.KEYDOWN: #Quand une touche est cliqué
            if event.key == pygame.K_SPACE and GameInfos.GameStarted == True: #La Barre espace est appuyé et la partie a commencé
                if GameInfos.GamePaused == False and GameInfos.Winner == "": #Met le Jeu en Pause
                    print("Paused")
                    GameInfos.GamePaused = True
                    MainGame.GameInfos.GameTimerObj.pause()
                    if GameInfos.GameMode == "Timer":
                        try:
                            MainGame.GameInfos.Player1Timer.pause()
                        except:
                            pass
                        try:
                            MainGame.GameInfos.Player2Timer.pause()
                        except:
                            pass
                    UpdateMenuFrame(1)
                elif GameInfos.GamePaused == True and GameInfos.Winner == "": #Continue la Partie
                    print("UnPaused")
                    """SoundMenu.stop()
                    GameInfos.SoundPlaying = "Game"
                    SoundGame.play(100,0,4000)
                    if Son == False :
                        pygame.mixer.pause()"""
                    GameInfos.GamePaused = False
                    GameInfos.GameTimerObj.resume(pygame.time.get_ticks())
                    if GameInfos.GameMode == "Timer":
                        try:
                            MainGame.GameInfos.Player1Timer.resume(pygame.time.get_ticks())
                        except:
                            pass
                        try:
                            MainGame.GameInfos.Player2Timer.resume(pygame.time.get_ticks())
                        except:
                            pass
                    UpdateMenuFrame(-1)
    
    pygame.display.flip() #Mets à Jour l'écran
    #pygame.display.update([boite.rect, boite2.rect]) --> a utiliser plus tard avec seulement les rect des objets qui ont été bougés
    #pygame.time.wait() --> Wait de Pygame

    """Timer"""
    if GameInfos.GameStarted == True and GameInfos.GamePaused == False:
        Time = pygame.time.get_ticks()
        GameInfos.UpdateTimers(Time)
        
        # if PlrTimer.Active == True:
        #     if PlrTimer.UpdateTimer(Time, GameInfos.Tour["Couleur"]):
        #         GameInfos.EchecetMath(GameInfos.Tour["Couleur"]) #Perds au Temps

print("Stopped successfuly: Chessers V2")
pygame.display.quit #Quitte la fenêtre de Jeu
pygame.quit() #Quitte pygame