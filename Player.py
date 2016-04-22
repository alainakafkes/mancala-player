## Alaina Kafkes
## 21 April 2016

## Creates several types of players that can play Mancala, including
## a custom player class that has an intelligent Mancala heuristic.

from random import *
from decimal import *
from copy import *
from MancalaBoard import *

INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1 #impossible move
        alpha = -INFINITY
        beta = INFINITY
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
        	if ply == 0: # if we're at ply 0, we need to call our eval function & return
        		return (self.score(board), m)
        	if board.gameOver():
        		return (-1, -1) # end game
        	nb = deepcopy(board) # make a new board
        	nb.makeMove(self, m) # try that move
        	opp = Player(self.opp, self.type, self.ply)
        	s = opp.minAB(nb, ply-1, turn, alpha, beta) #check what the opponent would do next
        	if s > score: # if the result is better than our best score so far, save that move,score
        		move = m
        		score = s
        	alpha = max(score, alpha)
        return score, move #return the best score and move so far 

    def maxAB(self,board, ply, turn, alpha, beta):
        """ Find the AB-pruning value for the next move for this player
            at a given board configuation. Returns score. """
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            score = max(score, opponent.minAB(nextBoard, ply-1, turn, alpha, beta))
            if (score >= beta): # prune if new score exceeds beta
                return score
            alpha = max(alpha, score)
        return score 


    def minAB(self, board, ply, turn, alpha, beta):
        """ Find the AB-pruning value for the next move for this player
            at a given board configuation. Returns score. """
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            score = min(score, opponent.maxAB(nextBoard, ply-1, turn, alpha, beta))
            if (score <= alpha): # prune if new score is less than alpha
                return score
            beta = min(beta, score)
        return score


                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
           #Implement custom player
           #calls ABMove function
           #each move in 10 seconds or less
           val, move = self.alphaBetaMove(board, 8)
           print "choose move", move, "with value", val
           return move 
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class alaina(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently (score is the heuristic) """

    def score(self, board):
        """ Evaluate the Mancala board for this player """ 
        print "Calling score in MancalaPlayer"
        myMancala = board.scoreCups[(self.num-1)]
        oppMancala = board.scoreCups[(self.opp-1)]
        if self.num == 1:
            myStones = sum(board.P1Cups)
            oppStones = sum(board.P2Cups)
        else:
            myStones = sum(board.P2Cups)
            oppStones = sum(board.P1Cups)
        eval = (myMancala - oppMancala) + (myStones - oppStones)
        return eval 
         
 