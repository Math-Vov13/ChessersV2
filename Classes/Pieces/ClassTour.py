from Classes import ClassPieces

class Tour(ClassPieces.Pieces):
    def __init__(self, Piece : str, Couleur : str, Image : str, Position : tuple):
        super().__init__(Piece, Couleur, Image, Position)                   #Récupère la méthode __init__ de la Classe Parent, donc --> Pièces
        self.Roque = False                                                  #Pour savoir si la Tour a déjà été déplacé une fois ou non (dès que la Tour s'est déplacé, elle ne peut plus roque avec le Roi)
    
    def AvailableMovements(self, NewPos : tuple):
        """Renvoie sous forme d'un Dictionnaire les différents Mouvements Possibles. Dict --> {'Empty' : [(Position --> Tuple, Situation --> (Team, Piece))], 'Allie' : list, 'Ennemy' : list, 'Special' : list, 'CanCaptureKing' : bool}"""
        from Classes import MainGame
        self.Disabled = True
        Deplacements = {'Empty' : [], 'Allie' : [], 'Ennemy' : [], 'Special' : [], 'CanCaptureKing' : False, 'MoveNbr' : 0}
        self.Movements = Deplacements

        #Code pour se déplacer
        Stop = False
        Pos = NewPos
        for i in range(2):
            for v in range(2):
                X, Y = 0, 0
                Stop = False
                for _ in range(7):
                    if Stop == True:
                        continue

                    Pos = NewPos
                    if i == 1:
                        Y += 1
                    else:
                        X += 1
                    if v == 0:
                        Pos = MainGame.GameInfos.FindCase(Pos, (X, Y))
                    else:
                        Pos = MainGame.GameInfos.FindCase(Pos, (-X, -Y))

                    if Pos != None:
                        Situation = self.InfosCase(Pos)
                        Special = self.DetectSpecialMove(Pos)
                        if Special == "PriseEnPassant":
                            self.AddMovement('Special', (Pos, Situation[1], Special), False)
                        else:
                            self.AddMovement(Situation[0], (Pos, Situation[1], None), True)
                            if Situation[0] != "Empty":
                                Stop = True
                    else:
                        Stop = True
        
        return Deplacements
    
    def NewPosition(self, Position: tuple, Situation: tuple, SpecialMove: str):
        self.Roque = True
        super().NewPosition(Position, Situation, SpecialMove)