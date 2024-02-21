"""
Main driver file. It handles user input displaying the current game state
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 1024
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 165
IMAGES = {}
SOUNDS = {}

"""
Initialize a global directory of images. This will be called exactly once in the main
"""

def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.image.load("Pieces/" + piece + ".png")
        IMAGES[piece] = p.transform.scale(IMAGES[piece], (SQ_SIZE, SQ_SIZE))

def loadSounds():
    sounds = ['capture', 'move-self']
    for sound in sounds:
        SOUNDS[sound] = p.mixer.Sound("Sounds/" + sound + ".mp3")

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages() # loading image files, only do this once
    loadSounds() # loading sounds files, only do once
    running = True
    sqSelected = () # keep track of the square selected by the last click of the user, tuple(row, col)
    playerClicks = [] # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    validMoves = gs.getValidMoves()
    moveMade = False
    activePiece = ()

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and e.button == 1:
                location = p.mouse.get_pos() # (x, y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                
                if playerClicks == [] and gs.selectWrongSquare(row, col):
                    continue

                if playerClicks == []:               
                    activePiece = (row, col)
                    playerClicks.append((row, col))
                    print(activePiece)

                elif len(playerClicks) == 1:
                    playerClicks.append((row, col))

                if len(playerClicks) == 2: # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        movePiece(gs, move)
                        moveMade = True
                    playerClicks = []

            # release piece    
            elif e.type == p.MOUSEBUTTONUP and e.button == 1:
                if activePiece == ():
                    continue

                location = p.mouse.get_pos() # (x, y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if activePiece[0] == row and activePiece[1] == col: # player clicked on piece, is not drag and dropping
                    activePiece = ()
                    continue
                
                else:
                    move = ChessEngine.Move(activePiece, (row, col), gs.board)
                    if move in validMoves:
                        movePiece(gs, move) # need to implement
                        moveMade = True
                        playerClicks = []
                        activePiece = ()


        if moveMade:
            gs.whiteToMove = not gs.whiteToMove
            validMoves = gs.getValidMoves()
            moveMade = False
        
        drawGameState(screen, gs, playerClicks, activePiece)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs, playerClicks, activePiece):
    drawBoard(screen) # draw squares on the board
    # add in piece highlighting, move suggestions
    if len(playerClicks) == 1:
        highlightSquare(screen, playerClicks[0][0], playerClicks[0][1])
        moveSuggestions(screen, gs, playerClicks[0][0], playerClicks[0][1])
    drawPieces(gs, screen, gs.board, activePiece)

def highlightSquare(screen, r, c):
    p.draw.rect(screen, p.Color("green"), p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def moveSuggestions(screen, gs, r, c):
    moves = gs.getValidMovesPiece(r, c)
    for move in moves:
        row, col = move.endRow, move.endCol
        print ("row:", row, "col:", col)
        center = ((col+1) * SQ_SIZE - SQ_SIZE//2, (row+1) * SQ_SIZE - SQ_SIZE//2 )
        p.draw.circle(screen, p.Color("black"), center, SQ_SIZE//8)
        #p.draw.rect(screen, p.Color("green"), p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawBoard(screen):
    colors = [p.Color(211, 182, 131), p.Color(43, 29, 20)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(gs, screen, board, activePiece):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece == "--" or activePiece == (r,c):
                continue
            screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if activePiece != () and gs.isFriendly(activePiece[0], activePiece[1]):
        pos = p.mouse.get_pos()
        pieceRect = p.Rect(pos[0], pos[1], SQ_SIZE, SQ_SIZE)
        pieceRect.center = pos
        screen.blit(IMAGES[board[activePiece[0]][activePiece[1]]], pieceRect)

def movePiece(gs, move):
    print("valid move")
    if gs.isEnemy(move.endRow, move.endCol):
        p.mixer.Sound.play(SOUNDS['capture'])
    p.mixer.Sound.play(SOUNDS['move-self'])
    gs.makeMove(move)
            

if __name__ == "__main__":
    main()