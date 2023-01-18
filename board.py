from tkinter import *
from tkinter.messagebox import showinfo, askyesno

import winsound

from cell import Cell

class Board:
    def __init__(self):
        self.__cellSize = 50
        self.__root = Tk()
        self.__root.resizable(False, False)
        self.__root.title("Chain Reaction")
        self.__root.config(bg="black")

        self.__init()
        self.__root.mainloop()

    def __init(self):
        self.__players = []
        self.__gridCells = []
        self.__colors = ["green", "red", "blue", "yellow", "purple", "orange red", "brown", "cyan"]
        self.__howManyPlayers = 2
        self.__playerTurn = 0
        self.__rects = []

        self.__rows = Label(self.__root, text="veuillez renseigner hauteur", bg="black", fg="white")
        self.__rows.pack(padx=10, pady=10)
        self.__rowsEntry = Entry(self.__root, justify="center")
        self.__rowsEntry.pack()
        self.__columns = Label(self.__root, text="veuillez renseigner largeur", bg="black", fg="white")
        self.__columns.pack(padx=10, pady=10)
        self.__columnsEntry = Entry(self.__root, justify="center")
        self.__columnsEntry.pack()

        self.__howManyPlayers = Label(self.__root, text="veuillez renseigner le nombre de joueurs", bg="black",
                                      fg="white")
        self.__howManyPlayers.pack(padx=10, pady=10)
        self.__howManyPlayersEntry = Entry(self.__root, justify="center")
        self.__howManyPlayersEntry.pack()
        self.__button = Button(self.__root, text="Valider", command=self.createBoard)
        self.__button.pack(padx=10, pady=10)

    def createBoard(self):
        self.__n = int(self.__rowsEntry.get())
        self.__m = int(self.__columnsEntry.get())
        self.__numberOfPlayers = int(self.__howManyPlayersEntry.get())

        if self.__n < 3 or self.__n > 10:
            showinfo("Erreur", "Le nombre de lignes doit être compris entre 3 et 10.")
            return

        if self.__m < 3 or self.__m > 12:
            showinfo("Erreur", "Le nombre de colonnes doit être compris entre 3 et 12.")
            return

        if self.__numberOfPlayers < 2 or self.__numberOfPlayers > 8:
            showinfo("Erreur", "Le nombre de joueurs doit être compris entre 2 et 8.")
            return

        winsound.PlaySound("sonGong.wav", winsound.SND_ASYNC)

        for i in range(self.__numberOfPlayers):
            self.__players.append(self.__colors[i])

        self.__canvas = Canvas(width=self.__n * self.__cellSize + 50, height=self.__m * self.__cellSize + 50,
                               bg="black", bd=0, highlightthickness=0)
        self.__canvas.pack()

        self.__rows.destroy()
        self.__rowsEntry.destroy()
        self.__columns.destroy()
        self.__columnsEntry.destroy()
        self.__howManyPlayers.destroy()
        self.__howManyPlayersEntry.destroy()
        self.__button.destroy()

        self.__canvas.config(width=self.__n * self.__cellSize + 50, height=self.__m * self.__cellSize + 50)

        # In case of a new started game, if it's the first, the iteration on a empty list will not be executed
        for cell in self.__gridCells:
            cell.resetPawns()

        for i in range(self.__m):
            for j in range(self.__n):
                self.__rects.append(self.__canvas.create_rectangle(self.__cellSize * j + 25, self.__cellSize * i + 25,
                                                                   25 + self.__cellSize + j * self.__cellSize,
                                                                   25 + self.__cellSize + i * self.__cellSize,
                                                                   fill="black",
                                                                   outline=self.__colors[0]))
                self.__canvas.tag_bind(self.__rects[-1], "<Button-1>", lambda event, x=j, y=i: self.play(x, y))
                self.__gridCells.append(Cell(j, i, self.__root, self.__canvas, (i, j) in self.getCorners(),
                                             (j, i) in flatten(self.getEdges()), (j, i) in self.getCenterCells()))

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

    def play(self, x, y):
        colorsDeleted = set()

        def applyChainReaction(self, cell):
            if (cell.isCorner() and len(cell.getPawns()) == 1) or \
                    (cell.isEdge() and len(cell.getPawns()) == 2) or \
                    (cell.isCenter() and len(cell.getPawns()) == 3):
                cell.resetPawns()
                for cellAround in self.getCellsAround(cell.getX(), cell.getY()):
                    for pawn in cellAround.getPawns():
                        if pawn.getColor() != cell.getColor():
                            colorsDeleted.add(pawn.getColor())
                        pawn.setColor(self.__players[self.__playerTurn])
                    applyChainReaction(self, cellAround)
            else:
                cell.addPawn(self.__players[self.__playerTurn])

        cell = self.getCellByCoordinates(x, y)
        if cell.getColor() is not None and cell.getColor() != self.__players[self.__playerTurn]:
            return
        applyChainReaction(self, cell)

        for color in colorsDeleted:
            if self.isLooser(color):
                self.__players.remove(color)

        if self.checkVictory():
            newGame = askyesno("Victory",
                                          "The winner is " + self.__players[0] + ". Do you want to play again?")
            if not newGame:
                self.__root.destroy()
                return
            self.__canvas.destroy()
            self.__init()
            return

        self.__playerTurn = (self.__playerTurn + 1) % len(self.__players)
        for rect in self.__rects:
            self.__canvas.itemconfig(rect, outline=self.__players[self.__playerTurn])

    def isLooser(self, color):
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


def flatten(l):
    return [item for sublist in l for item in sublist]
