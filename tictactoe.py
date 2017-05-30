# Tic Tac Toe

import random
import copy


class Board:
    '''modified from Invent Your Own Games wiht Python by Al Sweigart'''
    def __init__(self):
        self.spaces = [' '] * 9

    def print(self):
        print('   |   |')
        print(' ' + self.spaces[6] + ' | ' + self.spaces[7] + ' | ' + self.spaces[8])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.spaces[3] + ' | ' + self.spaces[4] + ' | ' + self.spaces[5])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.spaces[0] + ' | ' + self.spaces[1] + ' | ' + self.spaces[2])
        print('   |   |')

    def isWinner(self, le):
        # Given a board and a player's letter, this function returns True if that player has won.
        return ((self.spaces[6] == le and self.spaces[7] == le and self.spaces[8] == le) or  # across the top
                (self.spaces[3] == le and self.spaces[4] == le and self.spaces[5] == le) or  # across the middle
                (self.spaces[0] == le and self.spaces[1] == le and self.spaces[2] == le) or  # across the self.spacesttom
                (self.spaces[6] == le and self.spaces[3] == le and self.spaces[0] == le) or  # down the left side
                (self.spaces[7] == le and self.spaces[4] == le and self.spaces[1] == le) or  # down the middle
                (self.spaces[8] == le and self.spaces[5] == le and self.spaces[2] == le) or  # down the right side
                (self.spaces[6] == le and self.spaces[4] == le and self.spaces[2] == le) or  # diagonal
                (self.spaces[8] == le and self.spaces[4] == le and self.spaces[0] == le))  # diagonal

    def isSpaceFree(self, spot):
        # Return true if the passed move is free on the passed board.
        return self.spaces[spot] == ' '

    def isfull(self):
        full = True
        for sp in self.spaces:
            full = full & (sp != ' ')
        return full

    def openspots(self):
        result = []
        for k in range(9):
            if self.isSpaceFree(k):
                result.append(k)
        return(result)


class Player:
    def __init__(self, nm, letter, human = True):
        self.letter = letter
        self.human = human
        self.name = nm

    def choose(self, board):
        print('%s it is your move. Choose a spot' % self.letter)
        print(board.openspots())
        return int(input())

class Bot(Player):
    def __init__(self, nm, letter, algo):
        self.algo = algo
        super().__init__(nm, letter, False)

    def choose(self, board):
        '''chose a spot on the board to play
            where to play is function of bot's letter and board state'''
        return(self.algo(self.letter, board))

class MoveAlgo:
    '''container for Bot choose algorithm
    algo should be a function which takes 'letter' and 'board' as arguments'''
    def __init__(self, id, algo):
        self.id = id
        self.algo = algo

class Game:
    '''p1, p2 are player or bot objects'''
    def __init__(self, p1, p2):
        self.board = Board()
        self.p1 = p1
        self.p2 = p2
        #decide who goes first
        first = random.choice([0, 1])
        if first == 0:
            self.currentplayer = self.p1
            self.otherplayer = self.p2
        else:
            self.currentplayer = self.p2
            self.otherplayer = self.p1

    def swap(self):
        tmp = self.currentplayer
        self.currentplayer = self.otherplayer
        self.otherplayer = tmp

    def move(self, spot):
        '''assume spot is open'''
        self.board.spaces[spot] = self.currentplayer.letter

    def gameover(self):
        return(self.board.isfull() | self.board.isWinner(self.p1.letter) | self.board.isWinner(self.p2.letter))

    def play(self):
        result = {self.p1.name: 0, self.p2.name: 0}
        keepgoing = True
        while(keepgoing):
            if (self.currentplayer.human):
                self.board.print()
            spot = self.currentplayer.choose(self.board)
            #automatic loss if illegal spot is selected
            if not (spot in self.board.openspots()):
                # if debugging: print('invalid move')
                result[self.currentplayer.name] = -10
                keepgoing = False
            self.move(spot)
            if self.board.isWinner(self.currentplayer.letter):
                # if debugging: print('%s wins' %s self.currentplayer.letter)
                result[self.currentplayer.name] = 1
                result[self.otherplayer.name] = -1
                keepgoing = False
            elif self.board.isfull():
                # if debugging: print('full board -- tie')
                keepgoing = False
            self.swap()
        # if debugging:
        #     game.board.print()
        #     print('xwin, ywin: %i %i' %(xwin, ywin))
        return(result)

def smartAlgo(letter, board):
    # AI copied from Invent Your Own Computer Games with Python by Al Sweigart
    # Given a board and the computer's letter, determine where to move and return that move.
    if letter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(9):
        bcopy = copy.deepcopy(board)
        if i in bcopy.openspots():
            bcopy.spaces[i] = letter
            if bcopy.isWinner(letter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(9):
        bcopy = copy.deepcopy(board)
        if i in bcopy.openspots():
            bcopy.spaces[i] = playerLetter
            if bcopy.isWinner(playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    cornerspots = [0,2,6,8]
    opencornerspots = [sp for sp in cornerspots if sp in board.openspots()]
    if len(opencornerspots) != 0:
        return(random.choice(opencornerspots))

    # Try to take the center, if it is free.
    if 4 in board.openspots():
        return 4

    # pick a random spot if nothing else worked
    return random.choice(board.openspots())

def dumbalgo(letter, board):
    return random.choice(board.openspots())

def dumberalgo(letter, board):
    return(random.randrange(9))


def main():
    debugging = True
#    pl1 = Player('me', 'X')
#    pl1 = Bot('comp2', 'X', smartAlgo)
    pl1 = Bot('comp2', 'X', dumbalgo)
    pl2 = Bot('comp1', 'Y', dumbalgo)
    game = Game(pl1, pl2)
    outcome = game.play()
#    print(outcome)
    return(outcome)

if __name__ == '__main__':
    for k in range(10):
        result = main()
        if result['comp1'] !=0 or result['comp2'] != 0:
            print(result)