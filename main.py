from tkinter import *

WORDS = []
CURRENT_WORDS = []
CURRENT_GROUP_INDEX = 0
CURRENT_WORD_INDEX = 0
CURRENT_INDEX = 0
SHOWN_WORD_UPPER_LIMIT = 10

def callback(var_x):
    if var_x.get()[-1] == " " or var_x.get()[-1] == "":
        word = var_x.get()
        text_input.delete(0, END)
        if CURRENT_WORD_INDEX >= len(CURRENT_WORDS):
            show_game_result()
        else:
            color_word(word)

        if CURRENT_WORD_INDEX == SHOWN_WORD_UPPER_LIMIT:
            fetch_new_words()

def color_word(word):
    global CURRENT_WORD_INDEX
    global CURRENT_INDEX

    if word.strip() == CURRENT_WORDS[CURRENT_WORD_INDEX].strip():
        color_correct_word()
    else:
        color_wrong_word()
    CURRENT_INDEX += len(CURRENT_WORDS[CURRENT_WORD_INDEX])+1
    CURRENT_WORD_INDEX += 1

def color_correct_word():
    text.tag_add("first_word", f"1.{CURRENT_INDEX}", f"1.{CURRENT_INDEX+len(CURRENT_WORDS[CURRENT_WORD_INDEX])}")
    text.tag_config("first_word", foreground="#08D9D6")

def color_wrong_word():
    text.tag_add("second_word", f"1.{CURRENT_INDEX}", f"1.{CURRENT_INDEX+len(CURRENT_WORDS[CURRENT_WORD_INDEX])}")
    text.tag_config("second_word", foreground="#FF2E63")


def fetch_new_words():
    global CURRENT_WORD_INDEX
    global CURRENT_GROUP_INDEX
    global CURRENT_INDEX
    global CURRENT_WORDS

    CURRENT_GROUP_INDEX += 1
    CURRENT_WORD_INDEX = 0  
    if SHOWN_WORD_UPPER_LIMIT*CURRENT_GROUP_INDEX >= len(WORDS):
        show_game_result()
        return
    elif SHOWN_WORD_UPPER_LIMIT*CURRENT_GROUP_INDEX+SHOWN_WORD_UPPER_LIMIT >= len(WORDS):
         CURRENT_WORDS = WORDS[SHOWN_WORD_UPPER_LIMIT*CURRENT_GROUP_INDEX:]
    else:
        CURRENT_WORDS = WORDS[SHOWN_WORD_UPPER_LIMIT*CURRENT_GROUP_INDEX: SHOWN_WORD_UPPER_LIMIT*CURRENT_GROUP_INDEX+SHOWN_WORD_UPPER_LIMIT]
    CURRENT_INDEX = 0
    text.config(state=NORMAL)
    text.delete("1.0", END)
    text.insert(INSERT, " ".join(CURRENT_WORDS))
    text.config(state=DISABLED)
    text.tag_configure("center", justify='center')

def show_game_result():
    for child in root.winfo_children(): 
        child.destroy()

def read_file():
    global WORDS
    global CURRENT_WORDS
    with open("./assets/sample_text.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            WORDS = WORDS + [word.strip() for word in line.strip().split(" ") if word.strip()]
        CURRENT_WORDS =  WORDS[0: SHOWN_WORD_UPPER_LIMIT]


            

root = Tk()
root.config(bg="#252A34")
root.minsize(width=800, height=500)
var_x = StringVar()
var_x.trace("w", lambda name, index, mode, var_x=var_x: callback(var_x))
text_input = Entry(root, background="#EAEAEA", foreground="#252A34", textvariable=var_x)

read_file()
text = Text(root, highlightthickness = 0, borderwidth=0, width=75, height=5, fg="#EAEAEA", background="#252A34")
text.tag_configure("center", justify='center')
text.insert(INSERT, " ".join(CURRENT_WORDS))

# adding a tag to a part of text specifying the indices
text.tag_add("center", "1.0", "end") 
text.configure(state=DISABLED)
text.pack(pady=(20,0))
text_input.pack()

root.mainloop()