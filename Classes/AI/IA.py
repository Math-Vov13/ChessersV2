from Classes import MainGame, ClassPieces
import math
ValeursP = {"Pion" : 1, "Cavalier" : 3, "Fou" : 3, "Tour" : 5, "Dame" : 9, "Roi" : float("inf")}

class Arbre:
    def __init__(self, state=None, parent=None, children=None):
        self.state = state
        self.parent = parent
        self.children = children or []

    def ajouter_enfant(self, state):
        enfant = Arbre(state=state, parent=self)
        self.children.append(enfant)
        return enfant

def construire_arbre(current_state, depth, max_depth, current_player, piece_values):
    if depth == 0:
        return Arbre(state=current_state)

    arbre = Arbre(state=current_state)
    for piece in MainGame.CouleurPieces[current_player]:
        for move in piece.AvailableMovements(piece.Position):
            new_state = piece.ImagineMove(current_state, move, piece)
            child = arbre.ajouter_enfant(new_state)
            child_score = minimax(child, max_depth, -math.inf, math.inf, False, current_player, evaluate_board, piece_values)
            child.score = child_score

    return arbre

def minimax(node, depth, alpha, beta, maximizing_player, current_player, evaluate_func, piece_values):
    if depth == 0 or node.is_terminal():
        return evaluate_func(node.state, current_player, piece_values), None

    best_move = None
    if maximizing_player:
        value = -math.inf
        for move, piece, child_node in node.get_children(current_player):
            child_value, _ = minimax(child_node, depth-1, alpha, beta, False, current_player, evaluate_func, piece_values)
            if child_value > value:
                value = child_value
                best_move = (move, piece)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
    else:
        value = math.inf
        for move, piece, child_node in node.get_children(current_player):
            child_value, _ = minimax(child_node, depth-1, alpha, beta, True, current_player, evaluate_func, piece_values)
            if child_value < value:
                value = child_value
                best_move = (move, piece)
            beta = min(beta, value)
            if alpha >= beta:
                break
    return value, best_move
    
def evaluate_board(Pieces : list, color : str):
    score = 0
    for Piece in Pieces:
        if Piece.Couleur == color:
            score += ValeursP[Piece.Name]
        else:
            score -= ValeursP[Piece.Name]
    return score

def findbestmove(board, Pieces, max_depth = 3):
    # Créer l'arbre de recherche
    tree = Arbre(board)
    # Obtenir le joueur qui doit jouer
    current_player = MainGame.GameInfos.Tour["Couleur"]
    # Appliquer l'algorithme Minimax avec élagage Alpha-Beta
    print(construire_arbre(board, 3, 0, "Blanc", ValeursP))
    best_move, _ = minimax(tree, max_depth, -math.inf, math.inf, True, current_player, evaluate_board, ValeursP)
    print(best_move)
    # Retourner le meilleur mouvement et la pièce qui le fait
    return best_move[0], best_move[1]


ActualBoard = {(120, 160): ['A8', None], (200, 160): ['B8', None], (280, 160): ['C8', None], (360, 160): ['D8', None], (440, 160): ['E8', None], (520, 160): ['F8', None], (600, 160): ['G8', None], (680, 160): ['H8', None], (120, 240): ['A7', None], (200, 240): ['B7', None], (280, 240): ['C7', None], (360, 240): ['D7', None], (440, 240): ['E7', None], (520, 240): ['F7', None], (600, 240): ['G7', None], (680, 240): ['H7', None], (120, 320): ['A6', None], (200, 320): ['B6', None], (280, 320): ['C6', None], (360, 320): ['D6', None], (440, 320): ['E6', None], (520, 320): ['F6', None], (600, 320): ['G6', None], (680, 320): ['H6', None], (120, 400): ['A5', None], (200, 400): ['B5', None], (280, 400): ['C5', None], (360, 400): ['D5', None], (440, 400): ['E5', None], (520, 400): ['F5', None], (600, 400): ['G5', None], (680, 400): ['H5', None], (120, 480): ['A4', None], (200, 480): ['B4', None], (280, 480): ['C4', None], (360, 480): ['D4', None], (440, 480): ['E4', None], (520, 480): ['F4', None], (600, 480): ['G4', None], (680, 480): ['H4', None], (120, 560): ['A3', None], (200, 560): ['B3', None], (280, 560): ['C3', None], (360, 560): ['D3', None], (440, 560): ['E3', None], (520, 560): ['F3', None], (600, 560): ['G3', None], (680, 560): ['H3', None], (120, 640): ['A2', None], (200, 640): ['B2', None], (280, 640): ['C2', None], (360, 640): ['D2', None], (440, 640): ['E2', None], (520, 640): ['F2', None], (600, 640): ['G2', None], (680, 640): ['H2', None], (120, 720): ['A1', None], (200, 720): ['B1', None], (280, 720): ['C1', None], (360, 720): ['D1', None], (440, 720): ['E1', None], (520, 720): ['F1', None], (600, 720): ['G1', None], (680, 720): ['H1', None]}