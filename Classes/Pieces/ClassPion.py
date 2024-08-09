from Classes import ClassPieces

class Pion(ClassPieces.Pieces) :
    def __init__(self, Piece : str, Couleur : str, Image : str, Position : tuple, Sens : str):
        super().__init__(Piece, Couleur, Image, Position)                   #Récupère la méthode __init__ de la Classe Parent, donc --> Pièces

        self.FirstMouv = False                                                  #Si le Pion a déjà été déplacé ou non
        self.Jump2Cases = [False, None]                                         #Si le Pion a été déplacé de 2 Cases (utilisé pour la Prise en Passant) --> (False, Position)
        self.PosPEP = None                                                      #Position de la Prise en Passant possible
        self.Sens = Sens                                                        #Le Sens de déplacement du Pion

    def AvailableMovements(self, NewPos : tuple):
        """Renvoie sous forme d'un Dictionnaire les différents Mouvements Possibles. Dict --> {'Empty' : [(Position --> Tuple, Situation --> (Team, Piece))], 'Allie' : list, 'Ennemy' : list, 'Special' : list, 'CanCaptureKing' : bool}"""
        from Classes import MainGame
        self.Disabled = True
        Deplacements = {'Empty' : [], 'Allie' : [], 'Ennemy' : [], 'Special' : [], 'CanCaptureKing' : False, 'MoveNbr' : 0}
        self.Movements = Deplacements

        #Code pour se déplacer
        Pos = NewPos                                                 #Position du Pion
        Nbr = 1
        Stop = False
        for _ in range(2):                                                  #Calcule pour ses déplacements dans le sens du Pion (Haut ou Bas)
            if Stop == True:
                continue

            Pos = NewPos
            if self.Sens == "Haut":
                Pos = MainGame.GameInfos.FindCase(Pos, (0, Nbr))
            else:
                Pos = MainGame.GameInfos.FindCase(Pos, (0, -Nbr))

            if Pos != None:
                Situation = self.InfosCase(Pos)
                if Situation[0] == "Ennemy" or Situation[0] == "Allie":
                    Stop = True
                    if Situation[0] == "Allie":
                        self.AddMovement('Allie', (Pos, Situation[1], None), False)
                else:
                    Special = self.DetectSpecialMove(Pos)
                    if Special == "Promotion":
                        self.AddMovement('Special', (Pos, Situation, Special), False)
                    else:
                        self.AddMovement('Empty', (Pos, Situation[1], None), False)
                        if self.FirstMouv == False:
                            if Nbr == 1:
                                self.PosPEP = Pos
                                Nbr = 2
                            else:
                                self.Jump2Cases[1] = Pos
                        else:
                            Stop = True

        Nbr = -1
        for _ in range(2):                                                  #Calcule pour les déplacement pour capturé une Pièce ennemi (en diagonale)
            Pos = NewPos
            if self.Sens == "Haut":
                Pos = MainGame.GameInfos.FindCase(Pos, (Nbr, 1))
            else:
                Pos = MainGame.GameInfos.FindCase(Pos, (Nbr, -1))
            Nbr += 2

            if Pos != None:
                Situation = self.InfosCase(Pos)
                Special = self.DetectSpecialMove(Pos)
                if Situation[0] == "Ennemy":
                    if Special == "Promotion" or Special == "PriseEnPassant":
                        self.AddMovement('Special', (Pos, Situation, Special), True)
                    else:
                        self.AddMovement(Situation[0], (Pos, Situation[1], None), False)
                elif Situation[0] == "Allie":
                    self.AddMovement(Situation[0], (Pos, Situation[1], None), False)
    
        return Deplacements
    
    def NewPosition(self, Position : tuple, Situation : tuple, SpecialMove : str):  #Change de Position
        if self.FirstMouv == False:                                                 #Si c'est son premier mouvement
            self.FirstMouv = True
            from Classes import MainGame
            if MainGame.GameInfos.GameMode != "Tradition":
                print(self.Jump2Cases, self.Position)
                if self.Jump2Cases[0] == False and Position == self.Jump2Cases[1]:
                    print("Peut y avoir une Prise en Passant !! ;)")
                    from Classes.Pieces import ClassPionPEP
                    self.Jump2Cases[0] = True
                    print(self.PosPEP)
                    ClassPionPEP.PionPEP("PionPEP", self.Couleur, self.PosPEP, self)
        super().NewPosition(Position, Situation, SpecialMove)                       #Récupère la Méthode de la Fonction NewPosition