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
