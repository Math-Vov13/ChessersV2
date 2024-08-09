ValeursP = {"Pion" : 1, "Cavalier" : 3, "Fou" : 3, "Tour" : 5, "Dame" : 9, "Roi" : float("inf")}

def Play_Move(Positions : dict, Pieces : list):
    Best_Piece = None
    for Piece in Pieces:
        Best_Piece = minimax(Positions)
    Best_Piece.NewPosition() #Bouge la Pièce

def minimax(Piece, position, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or position.is_game_over():
        return evaluate(position)
    
    if maximizingPlayer:
        maxEval = float('-inf')
        for move in position.legal_moves:
            position.push(move)
            eval = minimax(position, depth - 1, alpha, beta, False)
            position.pop()
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = math.inf
        for move in position.legal_moves:
            position.push(move)
            eval = minimax(position, depth - 1, alpha, beta, True)
            position.pop()
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def evaluate(position):
    return 0


class Node:
    def __init__(self, state, color, depth, parent=None):
        self.state = state
        self.color = color
        self.depth = depth
        self.parent = parent
        self.children = []
        self.value = None

    def add_child(self, child):
        self.children.append(child)

def minimax(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node.state.is_game_over():
        node.value = node.state.evaluate()
        return node.value

    if maximizing_player:
        max_value = -float('inf')
        for child in node.children:
            value = minimax(child, depth - 1, alpha, beta, False)
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        node.value = max_value
        return max_value

    else:
        min_value = float('inf')
        for child in node.children:
            value = minimax(child, depth - 1, alpha, beta, True)
            min_value = min(min_value, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        node.value = min_value
        return min_value

def generate_tree(node, depth, maximizing_player):
    if depth == 0 or node.state.is_game_over():
        return
    for move in node.state.generate_moves():
        new_state = node.state.move_piece(move)
        new_color = node.state.get_next_color()
        child_node = Node(new_state, new_color, node.depth + 1, node)
        node.add_child(child_node)
        generate_tree(child_node, depth - 1, not maximizing_player)

def get_best_move(state, depth : int):
    root = Node(state, state.get_next_color(), 0)
    generate_tree(root, depth, True)
    best_move = None
    best_value = -float('inf')
    for child in root.children:
        value = minimax(child, depth, -float('inf'), float('inf'), False)
        if value > best_value:
            best_move = child.state.last_move
            best_value = value
    return best_move

# def RechercheNombrePremier(Start : int, Max : int):
#     #assert Start > 0, "Error !"

#     FirstNbr = []
#     Results = []

#     if Start == 1:
#         Results.append(1)

#     Nbr = 2
#     while True:
#         IsFirst = True
#         for v in FirstNbr:
#             if Nbr % v == 0:
#                 IsFirst = False
#                 break

#         if IsFirst:
#             print("Nombre trouvé :", Nbr)
#             FirstNbr.append(Nbr)
#             if Nbr >= Start:
#                 Results.append(Nbr)
#             if len(Results) == Max:
#                 print("Fin !")
#                 break

#         Nbr+=1
#     return Results

# print(RechercheNombrePremier(1, 10000))

def MiniTree(Max =4):
    if Max == 0:
        return []
    
    L = []
    for i in range(64):
        L.append(i)
        L+= MiniTree(Max-1)
    

    return L

def CalculCoupsWithDepth(Coups: int, Depth: int):
    if Depth == 1:
        return Coups
    
    return CalculCoupsWithDepth(Coups, Depth-1) + (Coups ** Depth)

#New = MiniTree()
#print(New)
#print(len(New))
print(CalculCoupsWithDepth(1024, 4))