from Classes import ClassPieces

class Roi(ClassPieces.Pieces):
    def __init__(self, Piece : str, Couleur : str, Image : str, Position : tuple):
        super().__init__(Piece, Couleur, Image, Position)                   #Récupère la méthode __init__ de la Classe Parent, donc --> Pièces
        self.Roque = False                                                  #Pour savoir si le Roi a déjà été déplacé une fois ou non (dès que le Roi s'est déplacé, il ne peut plus roque avec une Tour)
    
    def AvailableMovements(self,NewPos : tuple):
        """Renvoie sous forme d'un Dictionnaire les différents Mouvements Possibles. Dict --> {'Empty' : [(Position --> Tuple, Situation --> (Team, Piece))], 'Allie' : list, 'Ennemy' : list, 'Special' : list, 'CanCaptureKing' : bool}"""
        from Classes import MainGame
        self.Disabled = True
        Deplacements = {'Empty' : [], 'Allie' : [], 'Ennemy' : [], 'Special' : [], 'CanCaptureKing' : False, 'MoveNbr' : 0}
        self.Movements = Deplacements

        #Code pour se déplacer
        Pos = NewPos
        for Y in range(-1, 2):    
            for X in range(-1, 2):
                if X == 0 and Y == 0:               #Position du Roi (ne peut pas se déplacer à sa propre position)
                    continue
                Pos = NewPos
                Pos = MainGame.GameInfos.FindCase(Pos, (X, -Y))

                if Pos != None:
                    Situation = self.InfosCase(Pos)
                    Special = self.DetectSpecialMove(Pos)
                    if Special == "PriseEnPassant":
                        self.AddMovement('Special', (Pos, Situation[1], Special), False)
                    else:
                        self.AddMovement(Situation[0], (Pos, Situation[1], None), True)
        
        if self.Roque == False:
            for X in range(-1, 2, 2):
                Pos = NewPos
                Stop = False
                for _ in range(4):
                    if Stop == True:
                        continue
                    Pos = MainGame.GameInfos.FindCase(Pos, (X, 0))

                    if Pos != None:
                        NextPos = MainGame.GameInfos.FindCase(Pos, (X, 0))
                        Situation = self.InfosCase(Pos)
                        if Situation[0] != "Empty":
                            Stop = True
                            continue
                        Special = self.DetectSpecialMove(NextPos)
                        if Special == "Roque":
                            self.AddMovement('Special', (Pos, Situation[1], Special), False)
                            print("ROQUEEEE")
                            Stop = True


        
        return Deplacements
    
    def NewPosition(self, Position: tuple, Situation: tuple, SpecialMove: str):
        self.Roque = True
        super().NewPosition(Position, Situation, SpecialMove)