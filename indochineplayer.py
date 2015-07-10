import random, memory, constants, sys, copy

class IndoChinePlayer:

    def __init__(self, color):

        print 'IndoChine GOO!' #print name of class to ensure that right class is used
        self.color = color #color is 'B' or 'W'
        if color == 'W':
            self.oppColor = 'B'
        elif color == 'B':
            self.oppColor = 'W'
        else:
            assert False, 'ERROR: Current player is not W or B!'
        self.maxDepth = 5
            
    def chooseMove(self, board, prevMove):
        '''
        board is a two-dimensional list representing the current board configuration.
        board is a copy of the original game board, so you can do to it as you wish.
        board[i][j] is 'W', 'B', 'G' when row i and column j contains a
        white piece, black piece, or no piece respectively.
        As usual i, j starts from 0, and board[0][0] is the top-left corner.
        prevMove gives the i, j coordinates of the last move made by your opponent.
        prevMove[0] and prevMove[1] are the i and j-coordinates respectively.
        prevMove may be None if your opponent has no move to make during his last turn.
        '''       
        memUsedMB = memory.getMemoryUsedMB()
        if memUsedMB > constants.MEMORY_LIMIT_MB - 100: #If I am close to memory limit
            #don't allocate memory, limit search depth, etc.
            #RandomPlayer uses very memory so it does nothing
            pass
        return self.pickBestMove(board)



    def gameEnd(self, board):
        '''
        This is called when the game has ended.
        Add clean-up code here, if necessary.
        board is a copy of the end-game board configuration.
        '''
        # no clean up necessary for random player
        pass

    def getColor(self):
        '''
        Returns the color of the player
        '''
        return self.color
    
    def getMemoryUsedMB(self):
        '''
        You do not need to add to this code. Simply have it return 0
        '''
        return 0.0

    ########################### SUPPORT CODE #############################

    def validMove(self, board, pos, ddir, color, oppColor):
        newPos = (pos[0]+ddir[0], pos[1]+ddir[1])
        validPos = newPos[0] >= 0 and newPos[0] < constants.BRD_SIZE and newPos[1] >= 0 and newPos[1] < constants.BRD_SIZE
        if not validPos: return False
        if board[newPos[0]][newPos[1]] != oppColor: return False

        while board[newPos[0]][newPos[1]] == oppColor:
            newPos = (newPos[0]+ddir[0], newPos[1]+ddir[1])
            validPos = newPos[0] >= 0 and newPos[0] < constants.BRD_SIZE and newPos[1] >= 0 and newPos[1] < constants.BRD_SIZE
            if not validPos: break

        validPos = newPos[0] >= 0 and newPos[0] < constants.BRD_SIZE and newPos[1] >= 0 and newPos[1] < constants.BRD_SIZE
        if validPos and board[newPos[0]][newPos[1]] == color:
            return True
        return False

    ############################## EXTRA FUNCTIONS ##############################

    # returns array of all possible valid move given a board configuration
    def allValidMoves(self,board):
                       
        dirs = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        color = self.color
        if   color == 'W': oppColor = 'B'
        elif color == 'B': oppColor = 'W'
        else: assert False, 'ERROR: Current player is not W or B!'

        moves = []
        for i in xrange(len(board)):
            for j in xrange(len(board[i])):
                if board[i][j] != 'G': continue #background is green, i.e., empty square
                for ddir in dirs:
                    if self.validMove(board, (i,j), ddir, color, oppColor):
                        moves.append((i,j))
                        break
        if len(moves) == 0: return None #no valid moves
        
        return moves

    #search function caller
    #TODO: to reduce memory used by function call
    def pickBestMove(self,board):
        bestAction = self.alphaBetaSearch(board)
        return bestAction


    #return best move in tuple
    def alphaBetaSearch(self,board):
        argmax = self.firstMaxValue(board,-sys.maxint-1, sys.maxint,0)
        return argmax

    #returns argmax, instead of value v, to determine the best move
    def firstMaxValue(self,board,alpha,beta,counter):
        if self.testTerminal(counter):
            return self.utilityFunction(board,self.color)
        counter = counter + 1        
        v = -sys.maxint - 1

        validMoves = self.allValidMoves(board)
        argmax = None
        #don't even bother evaluating minimax here, the first best action is really doing nothing is doing nothing
        if validMoves == None:
            return None
        else:
            for a in validMoves:
                minimPlayerDecision = self.minValue(self.getNextBoard(board,a,self.color),alpha,beta,counter)

                if v < minimPlayerDecision:
                    v = minimPlayerDecision
                    argmax = a 

                #else:
                #don't update v
                #don't need to update argmax also

                if v >= beta: return v
                alpha = max(alpha,v)

        return argmax

    #returns the best value to be brought forward for calculation
    def maxValue(self,board,alpha,beta,counter):
        if self.testTerminal(counter):
            return self.utilityFunction(board,self.color)
        counter = counter + 1        
        v = -sys.maxint - 1

        validMoves = self.allValidMoves(board)
        if validMoves == None:
            v = max(v,self.minValue(self.getNextBoard(board,None,self.color),alpha,beta,counter))
            if v >= beta: return v
            alpha = max(alpha,v)
        else:
            for a in validMoves:
                v = max(v,self.minValue(self.getNextBoard(board,a,self.color),alpha,beta,counter))
                if v >= beta: return v
                alpha = max(alpha,v)

        return v


    def minValue(self,board,alpha,beta,counter):
        if self.testTerminal(counter):
            return self.utilityFunction(board,self.color)
        counter = counter + 1
        v = sys.maxint


        validMoves = self.allValidMoves(board)

        if validMoves == None:
            v = min(v,self.maxValue(self.getNextBoard(board,None,self.oppColor),alpha,beta,counter))
            if v <= alpha: return v
            beta = min(beta,v)
        else:
            for a in validMoves:
                v = min(v,self.maxValue(self.getNextBoard(board,a,self.oppColor),alpha,beta,counter))
                if v <= alpha: return v
                beta = min(beta,v)
        return v


        #remember to change arguments in minValue and maxValue, last argument denotes the counter
    def testTerminal(self,counter):
        if counter > self.maxDepth:
            return True
        else:
            return False

    def utilityFunction(self,board,playerColor):
        sumBlack = 0
        sumWhite = 0
        for i in xrange(len(board)):
            for j in xrange(len(board[i])):
                
                if board[i][j] == 'W':
                    sumWhite += 1
                elif board[i][j] == 'B':
                    sumBlack += 1
                else:
                    continue
        if playerColor=='B':
            return sumBlack-sumWhite
        else:
            return sumWhite-sumBlack
        

    def getNextBoard(self,board,action,playerColor):
        if action==None:
            return board
        else:
            newBoard = copy.deepcopy(board)
            newBoard[action[0]][action[1]] = playerColor 
            return newBoard

        
