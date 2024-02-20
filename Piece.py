from abc import ABC, abstractmethod 
class Piece():
    def __init__(self, id, location, color):
        self.id = id
        self.location = location
        self.color = color # will be passed in as "w" or "b" to denote white or black
        self.possibleMoves = []
        checkingKing = False #boolean that says whether or not this piece is currently holding the other king in check
        
        @abstractmethod
        def calculatePossibleMoves(board):
            pass

        @abstractmethod
        def checkingKing(board):
            pass

class Pawn(Piece):
    def __init__(self):
        super.__init__()
        
        def calculatePossibleMoves(board) {
            if board[self.location[0] + 1][self.location[1]] == "--":
                self.possibleMoves.append((self.location[0] + 1, self.location[1]))
            # move forward two condition
            if self.color == "w" and self. location[0] == 1: 
                pass
            elif self.color == "b" and self.location[0] == 6:
        }

class Rook(Piece):
    def __init__(self):
        super.__init__()

class Bishop(Piece):
    def __init__(self):
        super.__init__()

class Knight(Piece):
    def __init__(self):
        super.__init__()

class King(Piece):
    def __init__(self):
        super.__init__()

class Queen(Piece):
    def __init__(self):
        super.__init__()
