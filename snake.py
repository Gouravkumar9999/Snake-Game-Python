from tkinter import *

class Snake:
    def __init__(self, canvas, SPACE_SIZE, BODY_SIZE):
        self.body_size = BODY_SIZE
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill="#FF0000", tag="snake")
            self.squares.append(square)

    def restart(self, canvas, SPACE_SIZE, BODY_SIZE):
        # Clear existing snake squares (this is easy)
        for square in self.squares:
            canvas.delete(square)

        # Reset coordinates and squares (this is very annoying too)
        self.coordinates = []
        self.squares = []
        self.canvas = canvas
        self.space_size = SPACE_SIZE

        # Initialize the snake's body (again coz it doesnt and i spent way too much time on this)
        for i in range(0, BODY_SIZE):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill="#FF0000", tag="snake")
            self.squares.append(square)
            pass