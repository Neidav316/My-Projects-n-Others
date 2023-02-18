import random
import time
import tkinter

# SIZES
GAME_HEIGHT = 600
GAME_WIDTH = 600
SPEED = 200
SPACE_SIZE = 20  # Size of objects
BODY_PARTS = 3
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
###

# COLORS
WHITE = "#FFFFFF"
RED = "#FF0000"
GREEN = "#00FF00"
YELLOW = "#FFFF00"
BACKGROUND_COLOR = "#000000"
PINK = "#F2D2BD"
###

SINGLE_PLAYER_MODE = 1
DUO_PLAYER_MODE = 2
START_GAME = False
TIMER = 3


class Snake:

    def __init__(self, x, y, color, direction="none"):

        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.direction = direction
        self.color = color

        for i in range(0, BODY_PARTS):
            self.coordinates.append([x, y])  # Set coordinates for all body parts at the start
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color,
                                             tags="list of squares")
            self.squares.append(square)  # Set the canvas body parts at the start of coordinates


class Food:

    def __init__(self):
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=RED, tags="Food")


def next_move(snakes):
    for snake in snakes:
        x, y = snake.coordinates[0]
        if snake.direction == "up":
            y -= SPACE_SIZE
        elif snake.direction == "down":
            y += SPACE_SIZE
        elif snake.direction == "left":
            x -= SPACE_SIZE
        elif snake.direction == "right":
            x += SPACE_SIZE
        snake.coordinates.insert(0, (x, y))
    return snakes


def next_turn(snake, food):
    if snake.direction != "none":

        snake = next_move([snake])[0]
        x, y = snake.coordinates[0]

        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake.color)

        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:  # yes food, snake grows a body part

            global score

            score += 1

            label.config(text="Snake Game!\nScore: {}".format(score))

            canvas.delete("Food")

            food = Food()
        else:  # no food, snake dont grow
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]

        if check_collisions([snake], SINGLE_PLAYER_MODE) == -1:
            game_over(0)

        else:
            win.after(SPEED, next_turn, snake, food)
    else:
        win.after(SPEED, next_turn, snake, food)


def next_turn_two(snake_one, snake_two, food):
    global START_GAME, TIMER
    if START_GAME:

        snake_one, snake_two = next_move([snake_one, snake_two])
        for snake in [snake_one, snake_two]:
            x, y = snake.coordinates[0]

            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake.color)

            snake.squares.insert(0, square)
            if x == food.coordinates[0] and y == food.coordinates[1]:  # yes food, snake grows a body part
                canvas.delete("Food")
                food = Food()
            else:  # no food, snake dont grow
                del snake.coordinates[-1]
                canvas.delete(snake.squares[-1])
                del snake.squares[-1]
        who_lost = check_collisions([snake_one, snake_two], DUO_PLAYER_MODE)
        if who_lost != 0:
            game_over(who_lost)
        else:
            win.after(SPEED, next_turn_two, snake_one, snake_two, food)
    else:  # Timer Countdown
        TIMER -= 1
        if TIMER > 0:
            time.sleep(1)
            canvas.itemconfig("countdown", text="{}".format(TIMER))

        else:
            START_GAME = True
            time.sleep(1)
            if canvas.gettags("countdown"):
                canvas.delete("countdown")
        win.after(SPEED, next_turn_two, snake_one, snake_two, food)


def change_direction(new_direction, snake):
    if canvas.gettags(start_game_text):
        canvas.delete(start_game_text)
    if new_direction == "left":
        if snake.direction != "right":
            snake.direction = new_direction
    elif new_direction == "right":
        if snake.direction != "left":
            snake.direction = new_direction
    elif new_direction == "up":
        if snake.direction != "down":
            snake.direction = new_direction
    elif new_direction == "down":
        if snake.direction != "up":
            snake.direction = new_direction


def check_collisions(snakes, mode):
    if mode == SINGLE_PLAYER_MODE:  # 1 = player lost, 0 = continue game
        x, y = snakes[0].coordinates[0]
        if x < 0 or x >= GAME_WIDTH:
            return -1
        if y < 0 or y >= GAME_HEIGHT:
            return -1
        for body_part in snakes[0].coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return -1
        return 0
    elif mode == DUO_PLAYER_MODE:  # 1 = player one lost, 2 = player two lost, 3 = both lost, 0 = continue
        for i in range(len(snakes)):
            x, y = snakes[i].coordinates[0]
            if x < 0 or x >= GAME_WIDTH:
                return i + 1
            if y < 0 or y >= GAME_HEIGHT:
                return i + 1
            for body_part in snakes[i].coordinates[1:]:
                if x == body_part[0] and y == body_part[1]:
                    return i + 1
        if snakes[0].coordinates[0] in snakes[1].coordinates[1:]:
            return 1
        elif snakes[1].coordinates[0] in snakes[0].coordinates[1:]:
            return 2
        elif snakes[0].coordinates[0] == snakes[1].coordinates[0]:
            return 3

        return 0


def main_menu():
    win.geometry(f"400x300+{x - 200}+{y - 200}")
    menu_label = tkinter.Label(win, font=("consolas", 30), text="Snake Game")
    menu_label.pack()

    singleplayer_btn = tkinter.Button(win, width=20, text="Single Player Game",
                                      command=lambda: change_win(single_player))
    singleplayer_btn.pack(ipadx=5, ipady=10, pady=10, padx=10)

    two_player_btn = tkinter.Button(win, width=20, text="Duo Player Game", command=lambda: change_win(duo_players))
    two_player_btn.pack(ipadx=5, ipady=10, pady=10, padx=10)

    quit_btn = tkinter.Button(win, width=20, text="Exit", command= win.quit)
    quit_btn.pack(ipadx=5, ipady=10, pady=10, padx=10)


def change_win(mode):
    for widget in canvas.winfo_children():
        widget.destroy()
    for widget in win.winfo_children():
        widget.forget()
    mode()


def single_player():
    global start_game_text
    score = 0
    win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x - 250}+{y // 4}")
    canvas.delete(tkinter.ALL)
    label.config(text="Snake Game!\nScore: {}".format(score), font=("consolas", 20))
    label.pack()
    canvas.pack()

    snake = Snake(300, 300, GREEN)
    food = Food()

    start_game_text = canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 100,
                                         font=("consolas", 20),
                                         text="Press any arrow key to start",
                                         fill="cyan",
                                         tags="start game")

    ### binding keys
    win.bind("<Left>", lambda event: change_direction("left", snake))
    win.bind("<Right>", lambda event: change_direction("right", snake))
    win.bind("<Up>", lambda event: change_direction("up", snake))
    win.bind("<Down>", lambda event: change_direction("down", snake))

    next_turn(snake, food)


def duo_players():
    global START_GAME, TIMER
    TIMER = 3
    START_GAME = False
    win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x - 250}+{y // 4}")
    canvas.delete(tkinter.ALL)

    label.config(text="Snake Game!\nBlock each other to win!", font=("consolas", 20))
    label.pack()

    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 100,
                       font=("consolas", 40), text=f"{TIMER}",
                       fill="cyan",
                       tags="countdown")
    canvas.pack()

    snake_one = Snake(140, 140, GREEN, "right")
    snake_two = Snake(400, 400, PINK, "left")
    food = Food()
    win.bind("<Left>", lambda event: change_direction("left", snake_one))
    win.bind("<Right>", lambda event: change_direction("right", snake_one))
    win.bind("<Up>", lambda event: change_direction("up", snake_one))
    win.bind("<Down>", lambda event: change_direction("down", snake_one))

    win.bind("<a>", lambda event: change_direction("left", snake_two))
    win.bind("<d>", lambda event: change_direction("right", snake_two))
    win.bind("<w>", lambda event: change_direction("up", snake_two))
    win.bind("<s>", lambda event: change_direction("down", snake_two))

    win.update()

    next_turn_two(snake_one, snake_two, food)


def game_over(who_lost):
    canvas.delete(tkinter.ALL)
    game_over_text = 'GAME OVER' if who_lost not in [1,2,3] \
                     else ('Player '+ ('One' if who_lost == 2 else 'Two') + ' Wins') \
                     if who_lost in [1,2] else 'Its A Tie'
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                           font=("consolas", 50), text=game_over_text, fill="red")

    btn_return = tkinter.Button(canvas, width=15, bg=RED, fg=WHITE, text="Return to menu",
                                command=lambda: change_win(main_menu))
    btn_return.place(x=240, y=400)


# Set Window
win = tkinter.Tk()
win.title("Snake Game")
win.resizable(False, False)

score = 0

canvas = tkinter.Canvas(win, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
label = tkinter.Label(win)
start_game_text = -1  # default id for widget

win_width = win.winfo_width()
win_height = win.winfo_height()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

x = int((screen_width / 2) - (win_width / 2))
y = int((screen_height / 2) - (win_height / 2))

win.update()
###

main_menu()

win.mainloop()
