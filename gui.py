import tkinter as tk
from game import Game
from ai import AI

class Display(tk.Tk):
    """A class implementing the GUI for Tic Tac Toe."""

    def __init__(self):
        super().__init__()

        self.game = Game()
        self.ai = AI()

        self.title("Tic Tac Toe")

        self.menu = tk.Frame(self)
        self.board = tk.Frame(self)

        opponent = tk.Label(
            self.menu,
            font=("Calibri", 12),
            text="Who do you want to play against?"
        )
        difficulty = tk.Label(
            self.menu,
            font=("Calibri", 12),
            text="Difficulty level:"
        )

        opponent.grid(row=0, column=1, columnspan=3)
        difficulty.grid(row=2, column=1, columnspan=3)

        self.opponentButton1 = tk.Button(
            self.menu,
            text="Human\nvs.\nhuman",
            height=3,
            width=8,
            font=("Calibri", 12),
            command=self.humanVsHuman
        )
        self.opponentButton2 = tk.Button(
            self.menu,
            text="Human\nvs.\nAI",
            height=3,
            width=8,
            font=("Calibri", 12),
            command=self.humanVsAI
        )

        self.difficultyButton1 = tk.Button(
            self.menu,
            text="Easy",
            height=3,
            width=8,
            font=("Calibri", 12),
            command=self.easy,
            state=tk.DISABLED
        )
        self.difficultyButton2 = tk.Button(
            self.menu,
            text="Medium",
            height=3,
            width=8,
            font=("Calibri", 12),
            command=self.medium,
            state=tk.DISABLED
        )
        self.difficultyButton3 = tk.Button(
            self.menu,
            text="Hard",
            height=3,
            width=8,
            font=("Calibri", 12),
            command=self.hard,
            state=tk.DISABLED
        )

        self.opponentButton1.grid(row=1, column=1)
        self.opponentButton2.grid(row=1, column=2)

        self.difficultyButton1.grid(row=3, column=1)
        self.difficultyButton2.grid(row=3, column=2)
        self.difficultyButton3.grid(row=3, column=3)

        self.player1 = tk.Label(
            self.board,
            text=self.game.player1.name.capitalize() + "\n\n" + self.game.player1.letter,
            font=("Calibri", 16),
            fg="gray"
        )
        self.player2 = tk.Label(
            self.board,
            text=self.game.player2.name.capitalize() + "\n\n" + self.game.player2.letter,
            font=("Calibri", 16),
            fg="gray"
        )

        self.player1.grid(row=1, column=0)
        self.player2.grid(row=1, column=4)

        self.buttons = [
            tk.Button(
                self.board,
                text="",
                height=3,
                width=6,
                command=lambda square = square: self.click(square),
                state=tk.DISABLED,
                font=("Helvetica", 24)
            )
            for square in range(9)
        ]

        for i in range(9):
            self.buttons[i].grid(row=int(i / 3), column=i % 3 + 1)

        self.winMessage = tk.Label(
            self.board,
            text="",
            font=("Calibri", 12)
        )
        self.playAgain = tk.Button(
            self.board,
            text="Play\nagain",
            command=self.reset,
            height=3,
            width=8,
            font=("Calibri", 12)
        )

        self.menu.pack()

    def disableOpponentButtons(self):
        """Disable the buttons for selecting an opponent."""
        self.opponentButton1["state"] = tk.DISABLED
        self.opponentButton2["state"] = tk.DISABLED

    def humanVsHuman(self):
        """Configure the game for a human vs. human match."""
        self.game.player1.identity = "human"
        self.game.player2.identity = "human"
        self.disableOpponentButtons()
        self.startGame()

    def humanVsAI(self):
        """Configure the game for a human vs. AI match."""
        self.game.player1.identity = "human"
        self.game.player2.identity = "AI"
        self.disableOpponentButtons()
        self.activateDifficultyButtons()

    def activateDifficultyButtons(self):
        """Activate the buttons for selecting a difficulty."""
        self.difficultyButton1["state"] = tk.ACTIVE
        self.difficultyButton2["state"] = tk.ACTIVE
        self.difficultyButton3["state"] = tk.ACTIVE
    
    def disableDifficultyButtons(self):
        """Deactivate the buttons for selecting a difficulty."""
        self.difficultyButton1["state"] = tk.DISABLED
        self.difficultyButton2["state"] = tk.DISABLED
        self.difficultyButton3["state"] = tk.DISABLED

    def easy(self):
        """Set the AI difficulty to easy."""
        self.game.player2.difficulty = "easy"
        self.disableDifficultyButtons()
        self.startGame()

    def medium(self):
        """Set the AI difficulty to medium."""
        self.game.player2.difficulty = "medium"
        self.disableDifficultyButtons()
        self.startGame()

    def hard(self):
        """Set the AI difficulty to hard."""
        self.game.player2.difficulty = "hard"
        self.disableDifficultyButtons()
        self.startGame()

    def moveAIGUI(self):
        """Make a move for the AI."""
        self.ai.move(self.game)

        # Overwrite the board with the new game state after the AI's move.
        for square in range(9):
            self.buttons[square]["text"] = self.game.getLetter(square + 1)
            if not self.game.isEmpty(square + 1):
                self.buttons[square]["state"] = tk.DISABLED

    def click(self, square):
        """Move in the given square."""
        self.buttons[square]["text"] = self.game.currentPlayer.letter
        self.buttons[square]["state"] = tk.DISABLED
        self.game.setGrid(square + 1, self.game.currentPlayer)

        if self.game.currentPlayer == self.game.player1:
            self.player1["fg"] = "gray"
            self.player2["fg"] = "black"
        else:
            self.player1["fg"] = "black"
            self.player2["fg"] = "gray"

        if self.game.isGameOver():
            self.endGame()
        else:
            self.game.swapPlayer()

            if self.game.currentPlayer.isAI():
                self.player1["fg"] = "black"
                self.player2["fg"] = "gray"
                self.moveAIGUI()
                if self.game.isGameOver():
                    self.endGame()
                self.game.swapPlayer()


    def disableButtons(self):
        """Disable all the buttons on the board."""
        for button in self.buttons:
            button["state"] = tk.DISABLED
        
    def activateEmptyButtons(self):
        """Activate any empty buttons on the board."""
        for button in self.buttons:
            if button["text"] == "":
                button["state"] = tk.ACTIVE

    def endGame(self):
        """Stop the game and reveal the winner."""
        self.disableButtons()

        self.player1["fg"] = "gray"
        self.player2["fg"] = "gray"

        if self.game.isTie():
            self.winMessage["text"] = "It's a tie!"
        else:
            self.winMessage["text"] = self.game.currentPlayer.name.capitalize() + " wins!"

        self.winMessage.grid(row=8, column=1, columnspan=3)
        self.playAgain.grid(row=9, column=1, columnspan=3)

    def reset(self):
        """Hide the board and reveal the main menu."""
        self.opponentButton1["state"] = tk.ACTIVE
        self.opponentButton2["state"] = tk.ACTIVE

        for button in self.buttons:
            button["text"] = ""

        self.winMessage.grid_forget()
        self.playAgain.grid_forget()
        self.board.pack_forget()
        self.menu.pack()

        self.game.resetGrid()

    def startGame(self):
        """Hide the main menu and reveal the board."""
        self.menu.pack_forget()
        self.board.pack()
        for button in self.buttons:
            button["state"] = tk.ACTIVE
        
        self.game.whoGoesFirst()

        if self.game.currentPlayer == self.game.player1:
            self.player1["fg"] = "black"
            self.player2["fg"] = "gray"
        else:
            self.player1["fg"] = "gray"
            self.player2["fg"] = "black"

        if self.game.currentPlayer.isAI():
            self.moveAIGUI()
            self.game.swapPlayer()
