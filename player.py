class Player:
    """A class representing a Tic Tac Toe player."""

    def __init__(self, name, gridValue, letter):
        self.name = name
        self.gridValue = gridValue
        self.identity = ""
        self.difficulty = ""
        self.letter = letter

    def isAI(self):
        """Returns whether the player is an AI."""
        return self.identity == "AI"

    def isHuman(self):
        """Returns whether the player is a human."""
        return self.identity == "human"
