import math
import random

class AI:
    """A class implementing the AI for Tic Tac Toe."""

    def twoInARow(self, game, playerWithTwoInARow):
        """Search for a streak of two in a row and try to complete or block it."""
        for i in range(3):
            for j in range(3):
                if (playerWithTwoInARow.gridValue * 2) == game.getColumn(j).sum():
                    if game.grid[i][j] == game.empty.gridValue:
                        game.grid[i][j] = game.currentPlayer.gridValue
                        return True

                if (playerWithTwoInARow.gridValue * 2) == game.getRow(i).sum():
                    if game.grid[i][j] == game.empty.gridValue:
                        game.grid[i][j] = game.currentPlayer.gridValue
                        return True

            if (playerWithTwoInARow.gridValue * 2) == game.getDiagonal(0).sum():
                if game.grid[i][i] == game.empty.gridValue:
                    game.grid[i][i] = game.currentPlayer.gridValue
                    return True

            if (playerWithTwoInARow.gridValue * 2) == game.getDiagonal(1).sum():
                if game.grid[2 - i][i] == game.empty.gridValue:
                    game.grid[2 - i][i] = game.currentPlayer.gridValue
                    return True

        return False

    def tryToWin(self, game):
        """Search for a streak of two in a row and try to complete it."""
        return self.twoInARow(game, game.currentPlayer)

    def tryToBlock(self, game):
        """Search for a streak of two in a row and try to block it."""
        enemyPlayer = game.player1 if game.player2 == game.currentPlayer else game.player2
        return self.twoInARow(game, enemyPlayer)

    def evaluatePosition(self, game):
        """Score the current board position."""

        # This function takes the number of empty squares into account so the
        # AI will try to win sooner rather than later. It gets more points if
        # there are a lot of empty squares on the board. Otherwise it does
        # weird things like not playing in a square that would give it three
        # in a row. Also, it's important to add/subtract 1 to make sure the
        # evaluation isn't 0 when somebody wins.

        if game.checkWin(game.player1):
            return len(game.getEmptySquares()) + 1
        elif game.checkWin(game.player2):
            return -len(game.getEmptySquares()) - 1
        else:
            return 0

    def minimax(self, game, player, alpha=-math.inf, beta=math.inf):
        """
        Find the optimal move for the given player using minimax
        with alpha-beta pruning. Return a tuple where the first
        value is the evaluation of the optimal move and the second is
        a game object with the optimal move.
        """

        # Player 1 wants to maximize, and player 2 wants to minimize.

        if game.isGameOver():
            return (self.evaluatePosition(game), self)

        elif player == game.player1:
            bestMove = None
            maxEvaluation = -math.inf
            for move in game.getPossibleMoves(player):
                evaluation, _ = self.minimax(move, move.player2, alpha, beta)
                if (evaluation > maxEvaluation):
                    maxEvaluation = evaluation
                    bestMove = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return (maxEvaluation, bestMove)

        else:
            bestMove = None
            minEvaluation = math.inf
            for move in game.getPossibleMoves(player):
                evaluation, _ = self.minimax(move, move.player1, alpha, beta)
                if (evaluation < minEvaluation):
                    minEvaluation = evaluation
                    bestMove = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return (minEvaluation, bestMove)

    def randomMove(self, game):
        """Make a random move for the current player."""
        squareList = list(range(1, 10))
        random.shuffle(squareList)
        for square in squareList:
            if game.isEmpty(square):
                game.setGrid(square, game.currentPlayer)
                return

    def move(self, game):
        """
        Make a move for the current player.
        The hard AI uses minimax to make the optimal move.
        The medium AI wins if it already has two in a row and blocks
        the opponent if they have two in a row but otherwise plays randomly.
        The easy AI plays randomly.
        """

        if game.currentPlayer.difficulty == "hard":
            _, bestMove = self.minimax(game, game.currentPlayer)
            game.grid = bestMove.grid.copy()
        elif game.currentPlayer.difficulty == "medium":
            if self.tryToWin(game):
                return
            if self.tryToBlock(game):
                return
            self.randomMove(game)
        else:
            self.randomMove(game)
