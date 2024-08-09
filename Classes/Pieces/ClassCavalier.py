from Classes import ClassPieces

class Cavalier(ClassPieces.Pieces):
    def __init__(self, Piece : str, Couleur : str, Image : str, Position : tuple):
        super().__init__(Piece, Couleur, Image, Position)                   #Récupère la méthode __init__ de la Classe Parent, donc --> Pièces
    
    def AvailableMovements(self, NewPos : tuple):
        """Renvoie sous forme d'un Dictionnaire les différents Mouvements Possibles. Dict --> {'Empty' : [(Position --> Tuple, Situation --> (Team, Piece))], 'Allie' : list, 'Ennemy' : list, 'Special' : list, 'CanCaptureKing' : bool}"""
        from Classes import MainGame
        self.Disabled = True
        Deplacements = {'Empty' : [], 'Allie' : [], 'Ennemy' : [], 'Special' : [], 'CanCaptureKing' : False, 'MoveNbr' : 0}
        self.Movements = Deplacements

        #Code pour se déplacer
        Pos = NewPos
        Y = -2
        for _ in range(2):
            X = -1
            for _ in range(2):
                Pos = NewPos
                Pos = MainGame.GameInfos.FindCase(Pos, (X, Y))
                X += 2

                if Pos != None:
                    Situation = self.InfosCase(Pos)
                    Special = self.DetectSpecialMove(Pos)
                    if Special == "PriseEnPassant":
                        self.AddMovement('Special', (Pos, Situation[1], Special), False)
                    else:
                        self.AddMovement(Situation[0], (Pos, Situation[1], None), True)
            Y += 4
        X = -2
        for _ in range(2):
            Y = -1
            for _ in range(2):
                Pos = NewPos
                Pos = MainGame.GameInfos.FindCase(Pos, (X, Y))
                Y += 2

                if Pos != None:
                    Situation = self.InfosCase(Pos)
                    Special = self.DetectSpecialMove(Pos)
                    if Special == "PriseEnPassant":
                        self.AddMovement('Special', (Pos, Situation[1], Special), False)
                    else:
                        self.AddMovement(Situation[0], (Pos, Situation[1], None), True)
            X += 4

        return Deplacements