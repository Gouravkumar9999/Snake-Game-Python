from tkinter import *
import random

class Food:
    def __init__(self, canvas, WIDTH, HEIGHT, SPACE_SIZE):
        x = random.randint(1, (WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(1, (HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y +
                           SPACE_SIZE, fill="#FFFFFF", tag="food")
    

    def restart(self, canvas, WIDTH, HEIGHT, SPACE_SIZE):
        # Clear existing food coz this also took 2 hrs coz im not smart
        canvas.delete("food")
        
        # Reset coordinates and create new food so long this took ohhh myy godddd
        self.canvas = canvas
        self.width = WIDTH
        self.height = HEIGHT
        self.space_size = SPACE_SIZE
        self.__init__(canvas, WIDTH, HEIGHT, SPACE_SIZE)
        pass