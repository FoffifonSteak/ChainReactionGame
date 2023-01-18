import winsound

from pawn import Pawn


class Cell:
    def __init__(self, x, y, tk, canvas, isCorner, isEdge, isCenter):
        self.__x = x
        self.__y = y
        self.__tk = tk
        self.__pawns = []
        self.__ovals = []
        self.__canvas = canvas
        self.__isCorner = isCorner
        self.__isEdge = isEdge
        self.__isCenter = isCenter
        self.__color = None

    def isCorner(self):
        return self.__isCorner

    def isEdge(self):
        return self.__isEdge

    def isCenter(self):
        return self.__isCenter

    def addPawn(self, color):
        winsound.PlaySound("pawn.wav", winsound.SND_FILENAME)
        self.__color = color
        if len(self.__pawns) == 0:
            self.__pawns.append(Pawn(self.__x * 50 + 45, self.__y * 50 + 45, color, self.__tk, self.__canvas))
            return

        if self.__isEdge:
            if len(self.__pawns) == 1:
                # Only in edge cells with 2 pawns, we need to remove the center pawn and add 2 new pawns in corners of the cells
                self.removePawn()
                self.__pawns.append(Pawn(self.__x * 50 + 58, self.__y * 50 + 58, color, self.__tk, self.__canvas))
                self.__pawns.append(Pawn(self.__x * 50 + 30, self.__y * 50 + 30, color, self.__tk, self.__canvas))
        if self.__isCenter:
            if len(self.__pawns) == 1:
                self.__pawns.append(Pawn(self.__x * 50 + 30, self.__y * 50 + 30, color, self.__tk, self.__canvas))
            elif len(self.__pawns) == 2:
                self.__pawns.append(Pawn(self.__x * 50 + 58, self.__y * 50 + 58, color, self.__tk, self.__canvas))

    def getPawns(self):
        return self.__pawns

    def resetPawns(self):
        for pawn in self.__pawns:
            pawn.deleteFromCanvas()
        self.__pawns = []
        self.__color = None

    def removePawn(self):
        pawn = self.__pawns.pop()
        pawn.deleteFromCanvas()
        if len(self.__pawns) == 0:
            self.__color = None

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getCoordinates(self):
        return self.__x, self.__y

    def getColor(self):
        return self.__color