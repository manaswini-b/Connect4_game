from copy import copy
import random
import sys

class maxConnect4Game:
  def __init__(self):
      self.gameBoard = [[0 for i in range(7)] for j in range(6)]
      self.currentTurn = 1
      self.player1Score = 0
      self.player2Score = 0
      self.pieceCount = 0
      self.gameFile = None
      random.seed()

  # Count the number of pieces already played
  def checkPieceCount(self):
      self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

  # Output current game status to console
  def printGameBoard(self):
      print ' -----------------'
      for i in range(6):
          print ' |',
          for j in range(7):
              print('%d' % self.gameBoard[i][j]),
          print '| '
      print ' -----------------'

  # Output current game status to file
  def printGameBoardToFile(self):
      for row in self.gameBoard:
          self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
      self.gameFile.write('%s\r\n' % str(self.currentTurn))

  # Place the current player's piece in the requested column
  def playPiece(self, column):
      if not self.gameBoard[0][column]:
          for i in range(5, -1, -1):
              if not self.gameBoard[i][column]:
                  self.gameBoard[i][column] = self.currentTurn
                  self.pieceCount += 1
                  return 1

  # The AI section. Currently plays randomly.
  def aiPlay(self,depth, state):
      curr_player=self.currentTurn
      if curr_player == 1:
        opp_player = 2
      else:
        opp_player = 1
      legal_moves={}
      for col in range(7):
        if self.isLegalMove(col,state):
          # print("state", state)
          temp=self.makeMove(state, col, curr_player)
          legal_moves[col]= -self.search(depth-1, temp, opp_player)
      # print("legal moves")
      # print(legal_moves)
      best_alpha = -99999999
      best_move = None
      moves = legal_moves.items()
      # random.shuffle(list(moves))
      count=0
      moves_list=[]
      values_list=[]
      for key, value in sorted(legal_moves.iteritems(), key=lambda (k,v): (v,k)):
        # print("key-values", key, value)
        moves_list.append(key)
        values_list.append(value)
        count+=1

      my_alpha = max(values_list)
      for move, alpha in moves:
          if alpha >= best_alpha and alpha == my_alpha:
              best_alpha = alpha
              best_move = move
      
      
      result = self.playPiece(best_move)
      if not result:
          self.aiPlay()
      else:
          if self.currentTurn == 1:
              self.currentTurn = 2
          elif self.currentTurn == 2:
              self.currentTurn = 1
  def makeMove(self, state, column, player):

        temp = [x[:] for x in state]
        for i in xrange(6-1, -1, -1):
            if temp[i][column] == 0:
                temp[i][column] = player
                return temp

  def search(self, depth, state, curr_player):

    # enumerate all legal moves from this state
    legal_moves = []
    for i in range(7):
        # if column i is a legal move...
        if self.isLegalMove(i, state):
            # make the move in column i for curr_player
            temp = self.makeMove(state, i, curr_player)
            legal_moves.append(temp)
    
    # if this node (state) is a terminal node or depth == 0...
    if depth == 0 or len(legal_moves) == 0 or self.pieceCount == 42:
        # return the heuristic value of node
      return self.value(depth, state, curr_player)
  
    # determine opponent's color
    if curr_player == 1:
        opp_player = 2
    else:
        opp_player = 1

    alpha = -99999999
    for child in legal_moves:
        if child == None:
            print("child == None (search)")
        alpha = max(alpha, -self.search(depth-1, child, opp_player))
    return alpha

  def isLegalMove(self, column, state):
      """ Boolean function to check if a move (column) is a legal move
      """
      
      for i in range(6):
          if state[i][column] == 0:
              # once we find the first empty, we know it's a legal move
              return True
      
      # if we get here, the column is full
      return False

  def value(self, depth, state, player):

      if player == 1:
          o_player = 2
      else:
          o_player = 1
      
      my_fours = self.checkForStreak(state, player, 4)
      my_threes = self.checkForStreak(state, player, 3)
      my_twos = self.checkForStreak(state, player, 2)
      opp_fours = self.checkForStreak(state, o_player, 4)
      opp_threes = self.checkForStreak(state, o_player, 3)
      opp_twos = self.checkForStreak(state, o_player, 2)
      # if opp_fours > 0:
      #     return -100000-depth
      # else:
      return (my_fours*100000 + my_threes*100 + my_twos*10)-(opp_fours*100000 + opp_threes*1000+ opp_twos*10)+depth

  def checkForStreak(self, state, player, streak):
      count = 0
      # for each piece in the board...
      for i in range(6):
          for j in range(7):
              # ...that is of the color we're looking for...
              if state[i][j] == player:
                  # check if a vertical streak starts at (i, j)
                  count += self.verticalStreak(i, j, state, streak)
                  
                  # check if a horizontal four-in-a-row starts at (i, j)
                  count += self.horizontalStreak(i, j, state, streak)
                  
                  # check if a diagonal (either way) four-in-a-row starts at (i, j)
                  count += self.diagonalCheck(i, j, state, streak)
      # return the sum of streaks of length 'streak'
      return count
          

  def verticalStreak(self, row, col, state, streak):
      consecutiveCount = 0
      if row+streak-1 < 6:
        for i in xrange(streak):
          if state[row][col] == state[row+i][col]:
              consecutiveCount += 1
          else:
              break
  
      if consecutiveCount == streak:
          return 1
      else:
          return 0

  def horizontalStreak(self, row, col, state, streak):
      consecutiveCount = 0
      if col+streak-1 < 7:
        for i in xrange(streak):
          if state[row][col] == state[row][col+i]:
              consecutiveCount += 1
          else:
              break

      if consecutiveCount >= streak:
          return 1
      else:
          return 0

  def diagonalCheck(self, row, col, state, streak):

      total = 0
      # check for diagonals with positive slope
      consecutiveCount = 0
      
      if row+streak -1 < 6 and col+streak-1 < 7 :
        for i in xrange(streak):
          if state[row][col] == state[row+i][col+i]:
            consecutiveCount+=1
          else:
            break

      if consecutiveCount == streak:
          total += 1

      # check for diagonals with negative slope
      consecutiveCount = 0
      if row-streak+1 >=0 and col+streak-1 < 7 :
        for i in xrange(streak):
          if state[row][col] == state[row-i][col+i]:
            consecutiveCount+=1
          else:
            break
      if consecutiveCount == streak:
          total += 1

      return total


  # Calculate the number of 4-in-a-row each player has
  def countScore(self):
      self.player1Score = 0;
      self.player2Score = 0;

      # Check horizontally
      for row in self.gameBoard:
          # Check player 1
          if row[0:4] == [1]*4:
              self.player1Score += 1
          if row[1:5] == [1]*4:
              self.player1Score += 1
          if row[2:6] == [1]*4:
              self.player1Score += 1
          if row[3:7] == [1]*4:
              self.player1Score += 1
          # Check player 2
          if row[0:4] == [2]*4:
              self.player2Score += 1
          if row[1:5] == [2]*4:
              self.player2Score += 1
          if row[2:6] == [2]*4:
              self.player2Score += 1
          if row[3:7] == [2]*4:
              self.player2Score += 1

      # Check vertically
      for j in range(7):
          # Check player 1
          if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                 self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
              self.player1Score += 1
          if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                 self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
              self.player1Score += 1
          if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                 self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
              self.player1Score += 1
          # Check player 2
          if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                 self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
              self.player2Score += 1
          if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                 self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
              self.player2Score += 1
          if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                 self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
              self.player2Score += 1

      # Check diagonally

      # Check player 1
      if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
             self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
          self.player1Score += 1
      if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
             self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
          self.player1Score += 1
      if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
             self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
          self.player1Score += 1
      if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
             self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
          self.player1Score += 1
      if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
             self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
          self.player1Score += 1
      if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
             self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
          self.player1Score += 1
      if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
             self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
          self.player1Score += 1
      if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
             self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
          self.player1Score += 1
      if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
             self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
          self.player1Score += 1
      if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
             self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
          self.player1Score += 1
      if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
             self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
          self.player1Score += 1
      if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
             self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
          self.player1Score += 1

      if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
             self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
          self.player1Score += 1
      if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
             self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
          self.player1Score += 1
      if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
             self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
          self.player1Score += 1
      if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
             self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
          self.player1Score += 1
      if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
             self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
          self.player1Score += 1
      if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
             self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
          self.player1Score += 1
      if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
             self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
          self.player1Score += 1
      if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
             self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
          self.player1Score += 1
      if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
             self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
          self.player1Score += 1
      if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
             self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
          self.player1Score += 1
      if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
             self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
          self.player1Score += 1
      if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
             self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
          self.player1Score += 1

      # Check player 2
      if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
             self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
          self.player2Score += 1
      if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
             self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
          self.player2Score += 1
      if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
             self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
          self.player2Score += 1
      if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
             self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
          self.player2Score += 1
      if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
             self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
          self.player2Score += 1
      if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
             self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
          self.player2Score += 1
      if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
             self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
          self.player2Score += 1
      if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
             self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
          self.player2Score += 1
      if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
             self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
          self.player2Score += 1
      if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
             self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
          self.player2Score += 1
      if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
             self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
          self.player2Score += 1
      if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
             self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
          self.player2Score += 1

      if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
             self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
          self.player2Score += 1
      if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
             self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
          self.player2Score += 1
      if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
             self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
          self.player2Score += 1
      if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
             self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
          self.player2Score += 1
      if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
             self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
          self.player2Score += 1
      if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
             self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
          self.player2Score += 1
      if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
             self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
          self.player2Score += 1
      if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
             self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
          self.player2Score += 1
      if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
             self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
          self.player2Score += 1
      if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
             self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
          self.player2Score += 1
      if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
             self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
          self.player2Score += 1
      if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
             self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
          self.player2Score += 1
