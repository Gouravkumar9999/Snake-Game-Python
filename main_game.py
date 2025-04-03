import csv
from tkinter import *
from tkinter import simpledialog
from snake import Snake
from food import Food

# Constants for the game
WIDTH = 1540
HEIGHT = 720
SPEED = 150
SPACE_SIZE = 20
BODY_SIZE = 2
BACKGROUND_COLOR = "#00FF00"

# Global variables for the game state
score = 0
direction = 'down'

def next_turn(snake, food):
    """Move the snake to the next position, check if food is eaten, and handle collisions."""
    global direction, score

    x, y = snake.coordinates[0]

    # Move the snake's head based on the current direction
    if direction == "up": 
        y -= SPACE_SIZE
    elif direction == "down": 
        y += SPACE_SIZE
    elif direction == "left": 
        x -= SPACE_SIZE
    elif direction == "right": 
        x += SPACE_SIZE

    # Insert new head at the front of the coordinates list
    snake.coordinates.insert(0, (x, y))

    # Create a new square for the snake's head
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="#00FFFF"
    )
    snake.squares.insert(0, square)

    # Check if the snake ate food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Points: {score}")

        # Remove the food and create new food
        canvas.delete("food")
        food = Food(canvas, WIDTH, HEIGHT, SPACE_SIZE)
    else:
        # If no food eaten, remove the tail of the snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions with walls or itself
    if check_collisions(snake):
        game_over()
    else:
        # Continue the game after a delay
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    """Change the snake's direction, ensuring it can't go in the opposite direction."""
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    """Check if the snake has collided with the walls or itself."""
    x, y = snake.coordinates[0]

    # Check wall collisions
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True

    # Check for self-collision
    if (x, y) in snake.coordinates[1:]:
        return True

    return False

def save_high_score(name, score):
    """Save the player's name and score to a CSV file."""
    with open('high_scores.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, score])

def display_high_scores():
    """Display a window with the high scores from the CSV file."""
    high_scores_window = Tk()
    high_scores_window.title("High Scores")
    high_scores_window.geometry('400x400')

    try:
        with open('high_scores.csv', mode='r') as file:
            reader = csv.reader(file)
            high_scores = list(reader)

        # Sort high scores in descending order
        high_scores.sort(key=lambda x: int(x[1]), reverse=True)

        high_scores_label = Label(high_scores_window, text="High Scores", font=('Consolas', 30, "bold"))
        high_scores_label.pack()

        # Display each high score
        for score in high_scores:
            label = Label(high_scores_window, text=f"{score[0]}: {score[1]}", font=('Consolas', 20))
            label.pack()

    except FileNotFoundError:
        label = Label(high_scores_window, text="No high scores yet.")
        label.pack()

    high_scores_window.mainloop()

def new_game():
    """Initialize a new game by setting up the canvas and starting the game loop."""
    global canvas
    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
    next_turn(snake, food)

def game_over():
    """Display the game over screen and prompt for the player's name, then display high scores."""
    canvas.delete("all")
    label.config(text=f"Game Over! Points: {score}")
    restart_button.pack()

    name = simpledialog.askstring("Input", "Enter your name:")

    # Save the high score
    if name:
        save_high_score(name, score)

    # Show high scores after saving
    display_high_scores()

def restart_game(event=None):
    """Restart the game, resetting score and positions of snake and food."""
    global score, direction, snake, food
    score = 0
    direction = 'down'
    label.config(text=f"Points: {score}")
    restart_button.pack_forget()
    canvas.delete("all")
    snake.restart(canvas, SPACE_SIZE, BODY_SIZE)
    food.restart(canvas, WIDTH, HEIGHT, SPACE_SIZE)
    next_turn(snake, food)

def start_game():
    """Start the game by hiding the start screen and initializing the game objects."""
    global front_screen, canvas, label, snake, food

    front_screen.destroy()

    # Create and pack the canvas for the game
    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
    canvas.pack(expand=True, fill='both')

    label = Label(window, text=f"Points: {score}", font=('Consolas', 20))
    label.pack()

    snake = Snake(canvas, SPACE_SIZE, BODY_SIZE)
    food = Food(canvas, WIDTH, HEIGHT, SPACE_SIZE)

    window.after(SPEED, next_turn, snake, food)

# Create the main window
window = Tk()
window.title("Snake Game")

# Set up the window size and position without fullscreen
window.geometry(f"{WIDTH}x{HEIGHT}")

# Set up the front screen with the start button and high score button
front_screen = Canvas(window, height=HEIGHT, width=WIDTH, bg='#000000')
front_screen.pack(expand=True, fill='both')

start_button = Button(front_screen, text="Start Game", command=start_game, font=('Consolas', 30), bg='#00FF00')
start_button.place(relx=0.41, rely=0.5)

high_scores_button = Button(front_screen, text="High Scores", command=display_high_scores, font=('Consolas', 25), bg='#555555')
high_scores_button.place(rely=0.8, relx=0.42)

# Set up the restart button
restart_button = Button(window, text="Restart", command=restart_game)
restart_button.pack_forget()

# Bind keyboard events for snake movement and other controls
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Return>', restart_game)
window.bind("<Escape>", lambda event: window.destroy())

window.mainloop()
