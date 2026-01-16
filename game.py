import numpy as np
import random
import copy
from player import Player

class Game:
    """A class representing the game state of Tic Tac Toe."""

    def __init__(self):
        self.player1 = Player("player 1", -1, "X")
        self.player2 = Player("player 2", 1, "O")
        self.empty = Player("empty", 0, "")
        self.grid = np.zeros((3, 3), int)
        self.currentPlayer = None

    def getRow(self, row):
        """Return the specified row of the grid."""

        return self.grid[row, :]
    
    def getColumn(self, column):
        """Return the specified column of the grid."""

        return self.grid[:, column]

    def getDiagonal(self, diagonal):
        """
        Return the specified diagonal of the grid.
        0 is top left to bottom right.
        Any other input is top right to bottom left.
        """
        if diagonal == 0:
            return self.grid.diagonal()
        else:
            return np.fliplr(self.grid).diagonal()

    def isGameOver(self):
        """Check if the game has ended."""
        return (
            self.checkWin(self.player1)
            or self.checkWin(self.player2)
            or self.isTie()
        )
    
    def isTie(self):
        """Check if the game has ended in a tie."""
        return (
            not self.checkWin(self.player1)
            and not self.checkWin(self.player2)
            and np.all(self.grid)
        )

    def isEmpty(self, square):
        """Check if a given square is empty."""
        return self.getGrid(square) == self.empty.gridValue

    def getEmptySquares(self):
        """Return a list of squares (1-9) that are empty."""
        return [square for square in range(1, 10) if self.isEmpty(square)]

    def getPossibleMoves(self, player):
        """
        Return a list of game objects representing every possible move the
        player can make in the current position.
        """

        possibleMoves = []
        for square in self.getEmptySquares():
            gameCopy = copy.deepcopy(self)
            gameCopy.setGrid(square, player)
            possibleMoves.append(gameCopy)
        return possibleMoves

    def resetGrid(self):
        """Clear the grid."""
        self.grid = np.zeros((3, 3), int)

    def getGrid(self, square):
        """Given a number 1-9, return the corresponding grid entry."""
        return self.grid[int((square - 1) / 3)][(square - 1) % 3]

    def setGrid(self, square, player):
        """
        Given a number 1-9, fill the corresponding grid entry with the given
        player's marking.
        """

        self.grid[int((square - 1) / 3)][(square - 1) % 3] = player.gridValue

    def getLetter(self, square):
        """Given a number 1-9, return the letter of the player who controls that square."""

        if self.getGrid(square) == 1:
            return "O"
        elif self.getGrid(square) == -1:
            return "X"
        else:
            return " "

    def checkWin(self, player):
        """Return whether the given player has won the game."""
        return (
            (player.gridValue * 3) in self.grid.sum(axis=0)
            or (player.gridValue * 3) in self.grid.sum(axis=1)
            or (player.gridValue * 3) == self.getDiagonal(0).sum()
            or (player.gridValue * 3) == self.getDiagonal(1).sum()
        )

    def whoGoesFirst(self):
        """Randomly select which player goes first."""
        self.currentPlayer = random.choice((self.player1, self.player2))

    def swapPlayer(self):
        """Switch the current player to the other player."""
        self.currentPlayer = self.player1 if self.currentPlayer == self.player2 else self.player2
    