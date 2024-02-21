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

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                
                if playerClicks == [] and gs.selectWrongSquare(row, col):
                    continue

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else : 
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2: # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        print("valid move")
                        if gs.isEnemy(move.endRow, move.endCol):
                            p.mixer.Sound.play(SOUNDS['capture'])
                        p.mixer.Sound.play(SOUNDS['move-self'])
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []

        if moveMade:
            gs.whiteToMove = not gs.whiteToMove
            validMoves = gs.getValidMoves()
            moveMade = False
        
        drawGameState(screen, gs, playerClicks)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs, playerClicks):
    drawBoard(screen) # draw squares on the board
    # add in piece highlighting, move suggestions
    if len(playerClicks) == 1:
        highlightSquare(screen, playerClicks[0][0], playerClicks[0][1])
        moveSuggestions(screen, gs, playerClicks[0][0], playerClicks[0][1])
    drawPieces(screen, gs.board)

def highlightSquare(screen, r, c):
    p.draw.rect(screen, p.Color("green"), p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def moveSuggestions(screen, gs, r, c):
    moves = gs.getValidMovesPiece(r, c)
    for move in moves:
        r = move.endRow
        c = move.endCol
        p.draw.rect(screen, p.Color("green"), p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawBoard(screen):
    colors = [p.Color(211, 182, 131), p.Color(43, 29, 20)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece == "--":
                continue
            screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            

if __name__ == "__main__":
    main()