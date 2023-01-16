from tkinter import *


class Board:
    def __init__(self, n, m):
        self.__n = n
        self.__m = m
        self.__cellSize = 50
        self.__root = Tk()
        self.__root.resizable(False, False)
        self.__root.title("Chain Reaction")
        self.__root.config(bg="black")
        self.__canvas = Canvas(width=self.__n * self.__cellSize + 50, height=self.__m * self.__cellSize + 50, bg="black", bd=0, highlightthickness=0)
        self.__canvas.pack()
        self.__gridCells = []
        self._howManyPlayers = 2
        self.__colors = ["green", "red", "blue", "yellow", "orange", "purple", "pink", "brown"]
        self.__playerTurn = 0

        for i in range(m):
            for j in range(n):
                rect = self.__canvas.create_rectangle(self.__cellSize * j + 25, self.__cellSize * i + 25, 25 + self.__cellSize + j * self.__cellSize, 25 + self.__cellSize + i * self.__cellSize, fill="black", outline="white")
                self.__canvas.tag_bind(rect, "<Button-1>", lambda event, i=j, j=i: self.game(i, j))
                self.__gridCells.append(Cell(j, i, self.__root, self.__canvas, (i, j) in self.getCorners(),
                                             (j, i) in flatten(self.getEdges()), (j, i) in self.getCenterCells()))
        self.__root.mainloop()

    def getCorners(self):
        return (0, 0), (self.__m - 1, 0), (0, self.__n - 1), (self.__m - 1, self.__n - 1)

    def getEdges(self):
        return [(i, 0) for i in range(1, self.__n - 1)], [(i, self.__m - 1) for i in range(1, self.__n - 1)], [(0, i) for i in range(1, self.__m - 1)], [(self.__n - 1, i) for i in range(1, self.__m - 1)]

    def getCenterCells(self):
        return [(i, j) for i in range(1, self.__n - 1) for j in range(1, self.__m - 1)]

    def game(self, i, j):
        def removeSelf():
            self.getCellByCoordinates(i, j).removePawn()
        def setPlayerPawn(i2, j2):
            cell = self.getCellByCoordinates(i2, j2)
            if cell is None:
                return
            if cell.getColor() != None and cell.getColor() != self.__colors[self.__playerTurn]:
                return
            cell.addPawn(self.__colors[self.__playerTurn])
            self.__playerTurn = (self.__playerTurn + 1) % self._howManyPlayers

        if (j, i) in self.getCorners():
            if len(self.getCellByCoordinates(i, j).getPawns()) > 2:
                if i == 0 and j == 0:
                    setPlayerPawn(i, j + 1)
                    setPlayerPawn(i + 1, j)
                    removeSelf()
                elif i == 0 and j == self.__m - 1:
                    setPlayerPawn(i, j - 1)
                    setPlayerPawn(i + 1, j)
                    removeSelf()
                elif i == self.__n - 1 and j == 0:
                    setPlayerPawn(i, j + 1)
                    setPlayerPawn(i - 1, j)
                    removeSelf()
                elif i == self.__n - 1 and j == self.__m - 1:
                    setPlayerPawn(i, j - 1)
                    setPlayerPawn(i - 1, j)
                    removeSelf()
            else:
                setPlayerPawn(i, j)
        elif (i, j) in flatten(self.getEdges()):
            if len(self.getCellByCoordinates(i, j).getPawns()) > 3:
                if j == 0:
                    setPlayerPawn(i, j + 1)
                    setPlayerPawn(i - 1, j)
                    setPlayerPawn(i + 1, j)
                    removeSelf()
                elif j == self.__m - 1:
                    setPlayerPawn(i, j - 1)
                    setPlayerPawn(i - 1, j)
                    setPlayerPawn(i + 1, j)
                    removeSelf()
                elif i == 0:
                    setPlayerPawn(i, j - 1)
                    setPlayerPawn(i, j + 1)
                    setPlayerPawn(i + 1, j)
                    removeSelf()
                elif i == self.__n - 1:
                    setPlayerPawn(i, j - 1)
                    setPlayerPawn(i, j + 1)
                    setPlayerPawn(i - 1, j)
                    removeSelf()
            else:
                setPlayerPawn(i, j)
        elif (i, j) in self.getCenterCells():
            if len(self.getCellByCoordinates(i, j).getPawns()) > 4:
                setPlayerPawn(i, j - 1)
                setPlayerPawn(i, j + 1)
                setPlayerPawn(i - 1, j)
                setPlayerPawn(i + 1, j)
                removeSelf()
            else:
                setPlayerPawn(i, j)

    def getCellByCoordinates(self, x, y):
        for cell in self.__gridCells:
            if cell.getCoordinates() == (x, y):
                return cell


class Pawn:
    def __init__(self, x, y, color, tk, canvas):
        self.__x = x
        self.__y = y
        self.__color = color
        self.__tk = tk
        self.__canvas = canvas
        self.__oval = self.__canvas.create_oval(self.__x, self.__y,
                                                10 + self.__x, 10 + self.__y,
                                                fill=self.__color, outline="white")
        self.__canvas.update()

    def getOval(self):
        return self.__oval

    def deleteFromCanvas(self):
        self.__canvas.delete(self.__oval)


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

    def addPawn(self, color):
        if self.__isCorner:
            if len(self.__pawns) == 0:
                self.__pawns.append(Pawn(self.__x*50+45, self.__y*50+45, color, self.__tk, self.__canvas))
        if self.__isEdge:
            if len(self.__pawns) == 0:
                self.__pawns.append(Pawn(self.__x*50+58, self.__y*50+58, color, self.__tk, self.__canvas))
            elif len(self.__pawns) == 1:
                self.__pawns.append(Pawn(self.__x*50+30, self.__y*50+30, color, self.__tk, self.__canvas))
        if self.__isCenter:
            if len(self.__pawns) == 0:
                self.__pawns.append(Pawn(self.__x*50+30, self.__y*50+30, color, self.__tk, self.__canvas))
            elif len(self.__pawns) == 1:
                self.__pawns.append(Pawn(self.__x*50+45, self.__y*50+45, color, self.__tk, self.__canvas))
            elif len(self.__pawns) == 2:
                self.__pawns.append(Pawn(self.__x*50+58, self.__y*50+58, color, self.__tk, self.__canvas))
        self.__color = color
    def getPawns(self):
        return self.__pawns

    def removePawn(self):
        pawn = self.__pawns.pop()
        pawn.deleteFromCanvas()

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getCoordinates(self):
        return self.__x, self.__y

    def getColor(self):
        return self.__color


def flatten(l):
    return [item for sublist in l for item in sublist]

if __name__ == "__main__":
    board = Board(4, 7)