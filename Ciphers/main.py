from tkinter import *
import binascii

### SIZES
CANVAS_HEIGHT = 80
CANVAS_WIDTH = 350
WINDOW_WIDTH = 350
WINDOW_HEIGHT = 140

###

### COLORS
WHITE = "#FFFFFF"
RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000C8"
BACKGROUND_COLOR = "#DCDCDC"
###

DICT_LANGUAGES = {1: "English", 2: "Hebrew"}
LIST_ENGLISH_LETTERS = [chr(i) for i in range(ord('a'), ord('z') + 1)]
LIST_HEBREW_LETTERS = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק',
                       'ר', 'ש', 'ת']
chosen_language = 1  ### add jump back to start of alphabet when letter goes pass the last letter


def check_hebrew_ending_letters(ch):
    if ord(ch) >= ord('ץ'):
        ch = chr(ord(ch) + 5)
    elif ord(ch) >= ord('ף'):
        ch = chr(ord(ch) + 4)
    elif ord(ch) >= ord('ן'):
        ch = chr(ord(ch) + 3)
    elif ord(ch) >= ord('ם'):
        ch = chr(ord(ch) + 2)
    elif ord(ch) >= ord('ך'):
        ch = chr(ord(ch) + 1)
    return ord(ch)


def cypher(*args):
    user_string = user_text.get().lower()
    cyphered_string = ""
    for ch in user_string:
        if ch.isspace():
            cyphered_string = cyphered_string + ' '
        else:
            if ch in LIST_HEBREW_LETTERS:
                cyphered_ch_int = LIST_HEBREW_LETTERS.index(ch) + cypher_level.get()
                if cyphered_ch_int >= len(LIST_HEBREW_LETTERS):
                    cyphered_ch_int = cyphered_ch_int - len(LIST_HEBREW_LETTERS)
                cyphered_string = cyphered_string + LIST_HEBREW_LETTERS[cyphered_ch_int]
            elif ch in LIST_ENGLISH_LETTERS:
                cyphered_ch_int = LIST_ENGLISH_LETTERS.index(ch) + cypher_level.get()
                if cyphered_ch_int >= len(LIST_ENGLISH_LETTERS):
                    cyphered_ch_int = cyphered_ch_int - len(LIST_ENGLISH_LETTERS)
                cyphered_string = cyphered_string + LIST_ENGLISH_LETTERS[cyphered_ch_int]
    canvas.itemconfig(cyphered_text, text=f"Cyphered text: {cyphered_string.upper()}")


def adjust(i):
    if (0 <= cypher_level.get() and i == 1) or (26 >= cypher_level.get() and i == -1):
        cypher_level.set(cypher_level.get() + i)

win = Tk()
win.title("Ceaser Cipher")

cypher_level = IntVar(win, value=0)

label = Label(win, text="Enter text to cypher and adjust the level of cypher")
canvas = Canvas(win, bg=BACKGROUND_COLOR, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
slider = Scale(win, from_=0, to=26, variable=cypher_level, orient=HORIZONTAL, command=cypher, length=200)

label.pack()
slider.pack()
canvas.pack()

win.bind("<Left>", lambda event: adjust(-1))
win.bind("<Right>", lambda event: adjust(1))


user_text = Entry(canvas, fg=BLUE, width=CANVAS_WIDTH // 10)
cyphered_text = canvas.create_text(CANVAS_WIDTH // 4, CANVAS_HEIGHT // 1.5,
                                   font=("consolas", 10),
                                   text="Cyphered text:",
                                   fill="red"
                                   )
user_text.place(x=CANVAS_WIDTH // 20, y=CANVAS_HEIGHT // 3)

win_width = win.winfo_width()
win_height = win.winfo_height()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

x = int((screen_width / 2) - (win_width / 2))
y = int((screen_height / 2) - (win_height / 2))

win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x - 200}+{y - 200}")

win.bind_all("<Key>", cypher)

win.update()

win.mainloop()
