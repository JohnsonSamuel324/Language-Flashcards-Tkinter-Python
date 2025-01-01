import random
from tkinter import *

BACK_FLASHCARD = "./images/card_back.png"
BACKGROUND_COLOR = "#B1DDC6"
FLIP_DELAY = 3000
FRONT_FLASHCARD = "./images/card_front.png"

word = ""
definition = ""
after_id = None
words_to_learn = []

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# ---------------------------- Grab Random Word ------------------------------- #
# Grab content from language data file and put into list[]
try:
    with open("./data/spanish_words.csv"):
        pass
except FileNotFoundError:
    with open("./data/spanish_words.csv", "w"):
        pass
finally:
    with open("./data/spanish_words.csv", encoding='utf-8') as file:
        data = file.readlines()
    file.close()
    # Remove \n and add to list in variable
    data = [word.replace("\n", "") for word in data]

# Grab content from words_to_learn.csv if created and has content
try:
    with open("./words_to_learn.csv"):
        pass
except FileNotFoundError:
    pass
else:
    with open("./words_to_learn.csv", encoding='utf-8') as file:
        words_to_learn = file.readlines()
    words_to_learn = words_to_learn[1:]
    words_to_learn = [word.replace("\n", "") for word in words_to_learn]
    # Remove the words from words_to_learn in data
    [data.remove(word_definition) for word_definition in words_to_learn]

def generate_flashcard():
    global definition
    global data
    global word
    # Randomly grab the spanish word and definition
    # Grab from data if words_to_learn is blank
    if words_to_learn == []:
        word_definition = random.choice(data).split(",")
    else:
        word_definition = random.choice(words_to_learn).split(",")
    word = word_definition[0]
    definition = word_definition[1]
    canvas.itemconfig(flashcard_side, image=flashcard_front)
    canvas.itemconfig(language_text, text="Spanish", fill="black")
    canvas.itemconfig(word_text, text=word, fill="black")
    flip_timer()

# ---------------------------- Flashcard Timer ------------------------------- #
def flip_timer():
    global after_id
    # If after_id is a window.after, cancel the timer
    if after_id is not None:
        window.after_cancel(after_id)
    # Flip flashcard after given delay
    after_id = window.after(FLIP_DELAY, flip_flashcard)

# ---------------------------- Flip flashcard ------------------------------- #
def flip_flashcard():
    canvas.itemconfig(flashcard_side, image=flashcard_back)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=definition, fill="white")

# ---------------------------- Right Button ------------------------------- #
def got_right():
    # Remove word from data
    if words_to_learn == []:
        data.remove(f"{word},{definition}")
    else:
        words_to_learn.remove(f"{word},{definition}")
        with open("./words_to_learn.csv", "r", encoding='utf-8') as file:
            old_content = file.readlines()
            old_content = [line.replace("\n", "") for line in old_content]
        with open("./words_to_learn.csv", "w", encoding='utf-8') as file:
            [file.write(f"{line}\n") for line in old_content if line != f"{word},{definition}"]
    # Go to next flashcard
    generate_flashcard()
    pass
# ---------------------------- Wrong Button ------------------------------- #
def got_wrong():
    # Add the word and definition to file
    try:
        with open("./words_to_learn.csv"):
            pass
    except FileNotFoundError:
        with open("./words_to_learn.csv", "w") as file:
            file.write("Spanish,English")
        file.close()
    finally:
        if f"{word},{definition}" not in words_to_learn:
            with open("./words_to_learn.csv", "a", encoding='utf-8') as file:
                file.write(f"\n{word},{definition}")
    # Go to next flashcard
    generate_flashcard()
    pass
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
wrong_button = Button(image=wrong_image, highlightthickness=0, bd=0, command=got_wrong)
wrong_button.grid(column=0, row=1)

# Right button
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, bd=0, command=got_right)
right_button.grid(column=1, row=1)

# When application starts, run generate_flashcard()
generate_flashcard()

window.mainloop()