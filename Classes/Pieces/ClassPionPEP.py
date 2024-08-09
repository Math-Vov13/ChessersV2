from Classes import ClassPieces

class PionPEP(ClassPieces.Pieces) :
    def __init__(self, Piece : str, Couleur : str, Position : tuple, Creator : object):
        super().__init__(Piece, Couleur, '', Position)                   #Récupère la méthode __init__ de la Classe Parent, donc --> Pièces
        from Classes import MainGame
        self.Creator = Creator
        print(self.Position)
        MainGame.GameInfos.Positions[self.Position][1] = self
        MainGame.PionPEPList[self.Couleur] = self
    
    def AvailableMovements(self, NewPos : tuple):
        pass
    
    def NewPosition(self, Position : tuple, Situation : tuple, SpecialMove : str):  #Change de Position
        pass