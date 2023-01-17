from tkinter import *
from tkinter import messagebox


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

    def getColor(self):
        return self.__color

    def setColor(self, color):
        self.__color = color
        self.__canvas.itemconfig(self.__oval, fill=self.__color)


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
        if self.__isCorner:
            if len(self.__pawns) == 0:
                self.__pawns.append(Pawn(self.__x * 50 + 45, self.__y * 50 + 45, color, self.__tk, self.__canvas))
        if self.__isEdge:
            if len(self.__pawns) == 0:
                self.__pawns.append(Pawn(self.__x * 50 + 58, self.__y * 50 + 58, color, self.__tk, self.__canvas))
            elif len(self.__pawns) == 1:
                self.__pawns.append(Pawn(self.__x * 50 + 30, self.__y * 50 + 30, color, self.__tk, self.__canvas))
        if self.__isCenter:
            if len(self.__pawns) == 0:
                self.__pawns.append(Pawn(self.__x * 50 + 30, self.__y * 50 + 30, color, self.__tk, self.__canvas))
            elif len(self.__pawns) == 1:
                self.__pawns.append(Pawn(self.__x * 50 + 45, self.__y * 50 + 45, color, self.__tk, self.__canvas))
            elif len(self.__pawns) == 2:
                self.__pawns.append(Pawn(self.__x * 50 + 58, self.__y * 50 + 58, color, self.__tk, self.__canvas))
        self.__color = color

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


def flatten(l):
    return [item for sublist in l for item in sublist]


class Board:
    def __init__(self, n, m):
        self.__n = n
        self.__m = m
        self.__cellSize = 50
        self.__root = Tk()
        self.__root.resizable(False, False)
        self.__root.title("Chain Reaction")
        self.__root.config(bg="black")
        self.__canvas = Canvas(width=self.__n * self.__cellSize + 50, height=self.__m * self.__cellSize + 50,
                               bg="black", bd=0, highlightthickness=0)
        self.__players = []
        self.__canvas.pack()
        self.__gridCells = []
        self._howManyPlayers = 2
        self.__colors = ["green", "red", "blue", "yellow", "orange", "purple", "pink", "brown"]
        self.__playerTurn = 0

        for i in range(self._howManyPlayers):
            self.__players.append(self.__colors[i])

        for i in range(m):
            for j in range(n):
                rect = self.__canvas.create_rectangle(self.__cellSize * j + 25, self.__cellSize * i + 25,
                                                      25 + self.__cellSize + j * self.__cellSize,
                                                      25 + self.__cellSize + i * self.__cellSize, fill="black",
                                                      outline="white")
                self.__canvas.tag_bind(rect, "<Button-1>", lambda event, x=j, y=i: self.play(x, y))
                self.__gridCells.append(Cell(j, i, self.__root, self.__canvas, (i, j) in self.getCorners(),
                                             (j, i) in flatten(self.getEdges()), (j, i) in self.getCenterCells()))
        self.__root.mainloop()

    def getCorners(self):
        return (0, 0), (self.__m - 1, 0), (0, self.__n - 1), (self.__m - 1, self.__n - 1)

    def getEdges(self):
        return [(i, 0) for i in range(1, self.__n - 1)], [(i, self.__m - 1) for i in range(1, self.__n - 1)], \
            [(0, i) for i in range(1, self.__m - 1)], [(self.__n - 1, i) for i in range(1, self.__m - 1)]

    def getCenterCells(self):
        return [(i, j) for i in range(1, self.__n - 1) for j in range(1, self.__m - 1)]

    def getCellsAround(self, x, y):
        cells = []
        for cell in self.__gridCells:
            if cell.getCoordinates() in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                cells.append(cell)
        return cells

    def isChaining(self, cell):
        if cell.isCorner() and len(cell.getPawns()) == 1:
            return True
        elif cell.isEdge() and len(cell.getPawns()) == 2:
            return True
        elif cell.isCenter() and len(cell.getPawns()) == 3:
            return True
        return False

    def play(self, x, y):
        colorsDeleted = set()

        def applyChainReaction(self, cell):
            if (cell.isCorner() and len(cell.getPawns()) == 1) or (cell.isEdge() and len(cell.getPawns()) == 2) or (
                    cell.isCenter() and len(cell.getPawns()) == 3):
                cell.resetPawns()
                for cellAround in self.getCellsAround(cell.getX(), cell.getY()):
                    for pawn in cellAround.getPawns():
                        if pawn.getColor() != cell.getColor():
                            colorsDeleted.add(pawn.getColor())
                        pawn.setColor(self.__colors[self.__playerTurn])
                    applyChainReaction(self, cellAround)
            else:
                cell.addPawn(self.__colors[self.__playerTurn])

        cell = self.getCellByCoordinates(x, y)
        if cell.getColor() is not None and cell.getColor() != self.__colors[self.__playerTurn]:
            return
        applyChainReaction(self, cell)

        # Update the player turn to the next color, if the color is a looser, skip it

        self.__playerTurn = (self.__playerTurn + 1) % len(self.__players)

        for color in colorsDeleted:
            if self.checkIfLooser(color):
                self.__players.remove(color)

        if self.checkVictory():
            messagebox.showinfo("Victory", "The winner is " + self.__players[0])
            self.__root.destroy()


    def checkIfLooser(self, color):
        for cell in self.__gridCells:
            if cell.getColor() == color:
                return False
        return True

    def checkVictory(self):
        return len(set(self.__players)) == 1

    def getCellByCoordinates(self, x, y):
        for cell in self.__gridCells:
            if cell.getCoordinates() == (x, y):
                return cell


if __name__ == "__main__":
    board = Board(4, 7)
