"""
This class is responsible for storing all of the information about the current state of a chess game. It will also be 
responsible for determining the valid moves and keeping a move log.
Can use numpy arrays to make this faster
"""

class GameState():
    def __init__(self):
        # 8x8 2D List 
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        
        """
        self.whitePieces = [Rook(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Rook(),
                            Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn()]
        self.blackPieces = [Rook(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Rook(),
                            Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn()]"""
        
        self.whiteToMove = True
        self.moveLog = []
    
    def makeMove(self, move):
        print("making move")
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # add move to move log to keep history and potentially undo moves

    def selectWrongSquare(self, r, c) -> bool:
        c = self.board[r][c][0]
        if self.whiteToMove:
            return c == 'b' or c == '-'
        return c == 'w' or c == '-'
    # returns True if the square is currently empty
    def squareEmpty(self, r, c) -> bool:
        return self.board[r][c] == "--"
    
    def getValidMoves(self):
        return self.getAllMoves()

    def getAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    
                    if piece == 'P':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        for move in moves:
            print("valid:", move.getChessNotation())
        return moves
    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r <= 0:
                return
            # check forward move
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1, c), self.board))
                # check double forward move
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2, c), self.board))

            # check left capture
            if c > 0 and self.board[r-1][c-1][0] == 'b':
                moves.append(Move((r,c), (r-1, c-1), self.board))
            # check right capture
            if c < 7 and self.board[r-1][c+1][0] == 'b':
                moves.append(Move((r,c), (r-1, c+1), self.board))

                             
        elif not self.whiteToMove:
            # check forward move
            if r >= 7:
                return
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board))
                # check double forward move
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2, c), self.board))
            
            # check right capture
            if c > 0 and self.board[r+1][c-1][0] == 'w':
                moves.append(Move((r,c), (r+1, c-1), self.board))
            # check left capture
            if c < 7 and self.board[r+1][c+1][0] == 'w':
                moves.append(Move((r,c), (r+1, c+1), self.board))


    def getRookMoves(self, r, c, moves):
        # check up
        self.checkDir((1, 0), r, c, moves)
        # check down
        self.checkDir((-1, 0), r, c, moves)
        # check left
        self.checkDir((0, 1), r, c, moves)
        # check right
        self.checkDir((0, -1), r, c, moves)

    def getBishopMoves(self, r, c, moves):
        # check up, right
        self.checkDir((1, 1), r, c, moves)
        # check up, left
        self.checkDir((1, -1), r, c, moves)
        # check down, right
        self.checkDir((-1, 1), r, c, moves)
        # check dowm, left
        print("moves before:")
        for move in moves:
            print(move.getChessNotation())
        self.checkDir((-1, -1), r, c, moves)
        print("moves after:")
        for move in moves:
            print(move.getChessNotation())


    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:
            friendly = 'b'
        else:
            friendly = 'w'

        moveList = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for m in moveList:
            if r + m[0] > 7 or r + m[0] < 0 or c + m[1] > 7 or c + m[1] < 0:
                continue
            if self.board[r + m[0]][c + m[1]][0] != friendly:
                moves.append(Move((r, c), (r + m[0], c + m[1]), self.board))

    def getQueenMoves(self, r, c, moves):
        # check up
        self.checkDir((1, 0), r, c, moves)
        # check down
        self.checkDir((-1, 0), r, c, moves)
        # check left
        self.checkDir((0, 1), r, c, moves)
        # check right
        self.checkDir((0, -1), r, c, moves)
        # check up, right
        self.checkDir((1, 1), r, c, moves)
        # check up, left
        self.checkDir((1, -1), r, c, moves)
        # check down, right
        self.checkDir((-1, 1), r, c, moves)
        # check dowm, left
        self.checkDir((-1, -1), r, c, moves)


    def getKingMoves(self, r, c, moves):
        pass

    # check dir gets passed a tuple to check until end of board in that direction(inversed), (1, 0) in increasing row direction, (1, 1) check diagonal
    def checkDir(self, dir, r, c, moves):
        print("Checking Dir:", dir, "Square:", r, c)
        row, col = r, c
        vert, horz = dir[0], dir[1]
        while(row + vert >= 0 and row + vert <= 7 and col + horz >= 0 and col + horz <= 7):
            print ("in while loop")
            print("row:", row, "col:", col, "vert:", vert, "horz", horz)
            char = self.board[row+vert][col+horz][0]
            # ran into empty square
            if char == '-':
                print("empty square")
                moves.append(Move((r,c), (row+vert, col+horz), self.board))
            # ran into enemy piece
            elif (self.whiteToMove and char == 'b') or (not self.whiteToMove and char == 'w'):
                print("enemy sqaure")
                moves.append(Move((r,c), (row+vert, col+horz), self.board))
                break
            # ran into friendly piece
            else:
                print("friendly square")
                break
            row += vert
            col += horz


            

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"h": 7, "g": 6, "f": 5, "e": 4,
                   "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r ,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.startRow == other.startRow and self.startCol == other.startCol and self.endRow == other.endRow
                and self.endCol == other.endCol and self.pieceMoved == other.pieceMoved and self. pieceCaptured == other.pieceCaptured)
    
    