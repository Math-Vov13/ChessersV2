# MiniMax algorithm in Chess game
import asyncio
ValeursP = {"Pion" : 1, "PionPEP" : 1, "Cavalier" : 3, "Fou" : 3, "Tour" : 5, "Dame" : 9, "Roi" : float("inf")}

class IA:
    def __init__(self, Name : str, Color : str, EnnemyColor : str, Depth : int, Help : bool):
        self.Name = Name                #Nom de l'Ia
        self.Couleur = Color            #Couleur des Pièces de l'Ia
        self.PlrCouleur = EnnemyColor   #Couleur des Pièces Ennemies

        self.Profondeur = Depth         #Profondeur de l'Arbre des Possibles utilisé pour l'Ia
        self.Assiste = Help             #Utilisé pour le Mode Assist
    
    def PlayMove(self, Plateau : dict[tuple[int], list[str | None]], ObjetPieces : list, CouleurPieces : dict):
        print("Calculating Next Move...")
        Piece, Pos, Situation, CP = asyncio.run(self.FindBestMove(Plateau, ObjetPieces, CouleurPieces, self.Couleur, self.PlrCouleur, self.Profondeur))
        print("Le meilleur mouvement est :", Pos, " -->", Pos)
        print("La situation est :", Situation)
        print("La pièce qui effectue le meilleur mouvement est :", Piece)
        #sleep(3)
        Piece.NewPosition(Pos, Situation, CP) #Change la Position de la Pièce


    async def FindBestMove(self, Positions : dict[tuple[int], list[str | None]], ObjetPieces : list, CouleurPieces : dict[str, None], Couleur1 : str, Couleur2 : str, Depth : int):
        # ArbreDesPossibles = CreateTree(Positions, ObjetPieces, CouleurPieces, Couleur1, Couleur2, Depth)
        # print("Arbre des Possibles :", ArbreDesPossibles)
        # Noeud = minimax(ArbreDesPossibles)
        BatchList = []
        for Piece in CouleurPieces[self.Couleur]:
            BatchList.append(await self.__minimax(
                Piece=Piece,
                Plateau=Positions,
                CouleurPieces=CouleurPieces,
                Couleur=self.Couleur,
                maximazingPlayer=True,
                depth=self.Profondeur
                ))
            
        print("Resultats :", asyncio.gather(*BatchList))

        # Resultat = asyncio.run(self.__minimax(
        #     Plateau=Positions,
        #     CouleurPieces=CouleurPieces,
        #     Couleur=self.Couleur,
        #     maximazingPlayer=True,
        #     depth=self.Profondeur
        #     )
        # )
        #return Noeud.Piece, Noeud.Position, Noeud.Situation, Noeud.CoupSpecial
    
    async def __minimax(self, Piece: None, Plateau: dict[tuple[int], list[str | None]], CouleurPieces : dict[str, None], Couleur : str, maximazingPlayer: bool, depth: int):
        if depth == 0:
            return None
        
        if maximazingPlayer:
            maxEval = float("-inf")
            for Coup in Piece.Movements:
                Simulation = Piece.SimulateMove(Plateau, Coup)
                eval = await self.__minimax(Piece, Plateau=Simulation, CouleurPieces=CouleurPieces, Couleur=self.PlrCouleur, depth=depth-1, maximazingPlayer=False)
                maxEval = max(maxEval, eval)
            
            return maxEval
        else:
            minEval = float("+inf")
            for Coup in Piece.Movements:
                Simulation = Piece.SimulateMove(Plateau, Coup)
                eval = await self.__minimax(Piece, Plateau=Simulation, CouleurPieces=CouleurPieces, Couleur=self.Couleur, depth=depth-1, maximazingPlayer=True)
                minEval = min(minEval, eval)
            
            return minEval


    def __evalutation(self):
        return 0