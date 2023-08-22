import chess

##
def EndGame(board):
    return board.is_checkmate(
    ) or board.is_stalemate(
    ) or board.is_insufficient_material(
    ) or board.is_game_over()
  
#  
def score(points, board):    
  if EndGame(board):
    #Pontuação chequeMate
    if(board.is_checkmate()):
      if(board.turn):
        points += 10000 
      else:
        points -= 10000 
    else:
      #Pontuação Empate
      points -= 5000 
  else:
    #Pontuação peão
    points += len(board.pieces(chess.PAWN, chess.BLACK)) - len(board.pieces(chess.PAWN, chess.WHITE))
    #Pontuação cavalo
    points += 3 * (len(board.pieces(chess.KNIGHT, chess.BLACK)) - len(board.pieces(chess.KNIGHT, chess.WHITE)))
    #Pontuação bispo
    points += 3 * (len(board.pieces(chess.BISHOP, chess.BLACK)) - len(board.pieces(chess.BISHOP, chess.WHITE)))
    #Pontuação torre
    points += 5 * (len(board.pieces(chess.ROOK, chess.BLACK)) - len(board.pieces(chess.ROOK, chess.WHITE)))
    #Pontuação rainha
    points += 9 * (len(board.pieces(chess.QUEEN, chess.BLACK)) - len(board.pieces(chess.QUEEN, chess.WHITE)))
     
  return points
  
##
def TransformList(board):
  moves = str(board.legal_moves)
  moves = moves.replace(",","")
  startingMoves = int(moves.index("("))
  endingMoves = int(moves.index(")"))
  movementList = list(moves[startingMoves + 1:endingMoves].split(" "))
  return list(movementList)

#
def Minmax_alphabeta(nodes, ia, depth, alpha = float("-inf"), beta = float("inf")):
  #se o jogo acabou ou se a profundida 
  # maxima foi atingida
  if(depth == 0 or EndGame(nodes)):
    return score(0, nodes)
  #se é a vez da IA
  if ia: #turno da IA (max)
      for board in CopyBoard(nodes):
        value = Minmax_alphabeta(board, False, depth - 1, alpha, beta)
        alpha = max(value, alpha)
        if beta <= alpha:
          continue
        return alpha
  else: #turno do player (min)
     for board in CopyBoard(nodes):    
        value = Minmax_alphabeta(board, True, depth - 1, alpha, beta)
        beta = min(value, beta)
        if beta <= alpha:
          continue
        return beta
       
#
def BestMove_poda(board, depth = 1):
  max = float("-inf")
  bestMove = -1
  for nextBoard in CopyBoard(board):
    value = Minmax_alphabeta(nextBoard, False, depth)
    if value > max:
      max = value
      bestMove = nextBoard
  return bestMove

#
def CopyBoard(board):
    boardList = [] 
    movements = TransformList(board)
    for i in range(len(movements)):
        boardCopy = chess.Board(board.fen())
        boardCopy.push_san(movements[i])
        boardList.append(boardCopy)
    return boardList

##
def InicialMoves(move):
  if move == 1:
    board.push_san("e5")
  elif move == 2:
    board.push_san("Nc6")
  elif move == 3:
    board.push_san("Be7")
  else:
    bestBoard = BestMove_poda(board)
    for move in TransformList(board):
      boardCopy = chess.Board(board.fen())
      boardCopy.push_san(move)
      if boardCopy == bestBoard:
        bestMovement = move
    print("O computador decidiu que o movimento ganhador é: ", bestMovement)  
    board.push_san(bestMovement)

##
def Play(movimentos):    
    print(board)

    if not EndGame(board):
      if board.is_check():
        print("Check")   
      if not board.turn:
        print('O computador está pensando em como ganhar de você...')
        InicialMoves(movimentos)
        movimentos += 1
      else:
        try:
          print(TransformList(board))
          movement = input("\n Digite sua jogada: ")
          board.push_san(movement)
        except:
            print('\n Movimento invalido, tente novamente.')
          
      Play(movimentos) 
      
    else:
      if board.is_checkmate():
        print("Check Mate")
      else:
        print("Fim de jogo!")
        
points = 0
board = chess.Board()
movimentos = 1
Play(movimentos)
