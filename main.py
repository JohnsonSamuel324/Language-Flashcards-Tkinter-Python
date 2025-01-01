import random
from tkinter import *

BACK_FLASHCARD = "./images/card_back.png"
BACKGROUND_COLOR = "#B1DDC6"
FLIP_DELAY = 3000
FRONT_FLASHCARD = "./images/card_front.png"

word = ""
definition = ""

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# ---------------------------- Grab Random Word ------------------------------- #
def generate_flashcard():
    global word
    global definition

    with open("./data/spanish_words.csv") as file:
        data = file.readlines()
    file.close()
    # Randomly grab the spanish word and definition
    # Remove \n and add to list in variable
    word_definition = random.choice(data).replace("\n","").split(",")
    word = word_definition[0]
    definition = word_definition[1]
    canvas.itemconfig(flashcard_side, image=flashcard_front)
    canvas.itemconfig(language_text, text="Spanish", fill="black")
    canvas.itemconfig(word_text, text=word, fill="black")
    flip_timer()

# ---------------------------- Flashcard Timer ------------------------------- #
def flip_timer():
    window.after(FLIP_DELAY, flip_flashcard)

# ---------------------------- Flip flashcard ------------------------------- #
def flip_flashcard():
    canvas.itemconfig(flashcard_side, image=flashcard_back)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=definition, fill="white")

# ---------------------------- Right Button ------------------------------- #

# ---------------------------- Wrong Button ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #
# Flashcard
canvas = Canvas(width=800, height=526, highlightthickness=0)
canvas.config(bg=BACKGROUND_COLOR)
flashcard_front = PhotoImage(file=FRONT_FLASHCARD)
flashcard_back = PhotoImage(file=BACK_FLASHCARD)
flashcard_side = canvas.create_image(0, 0, anchor="nw", image=flashcard_front)
language_text = canvas.create_text(400, 150, text="Spanish", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 253, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Wrong button
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bd=0)
wrong_button.grid(column=0, row=1)

# Right button
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, bd=0, command=generate_flashcard)
right_button.grid(column=1, row=1)

# When application starts, run generate_flashcard()
generate_flashcard()

window.mainloop()