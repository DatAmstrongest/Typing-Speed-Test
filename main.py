from tkinter import *
import requests

TIME_LABEL = None
TEXT = None
TEXT_INPUT = None

WORDS = []
CURRENT_WORDS = []
CURRENT_GROUP_INDEX = 0
CURRENT_WORD_INDEX = 0
CURRENT_INDEX = 0
SHOWN_WORD_UPPER_LIMIT = 10

BACKGROUND_COLOR = "#252A34"
FOREGROUND_COLOR = "#EAEAEA"
CORRECT_COLOR =  "#08D9D6"
FALSE_COLOR = "#FF2E63"

CORRECT_WORDS_NUM = 0
WRONG_WORDS_NUM = 0
TOTAL_WRITTEN_WORDS = 0

TIME_UPPER_LIMIT = 5
CURRENT_TIME = TIME_UPPER_LIMIT

def callback(var_x):
    global TEXT_INPUT

    if len(var_x.get()) and (var_x.get()[-1] == " " or var_x.get()[-1] == ""):
        word = var_x.get()
        TEXT_INPUT.delete(0, END)
        color_word(word)
        if CURRENT_WORD_INDEX == SHOWN_WORD_UPPER_LIMIT:
            fetch_new_words()

def color_word(word):
    global CURRENT_WORD_INDEX
    global CURRENT_INDEX
    global TOTAL_WRITTEN_WORDS

    TOTAL_WRITTEN_WORDS += 1
    if word.strip() == CURRENT_WORDS[CURRENT_WORD_INDEX].strip():
        color_correct_word()
    else:
        color_wrong_word()
    CURRENT_INDEX += len(CURRENT_WORDS[CURRENT_WORD_INDEX])+1
    CURRENT_WORD_INDEX += 1

def color_correct_word():
    global CORRECT_WORDS_NUM
    global TEXT

    CORRECT_WORDS_NUM += 1
    TEXT.tag_add("first_word", f"1.{CURRENT_INDEX}", f"1.{CURRENT_INDEX+len(CURRENT_WORDS[CURRENT_WORD_INDEX])}")
    TEXT.tag_config("first_word", foreground=CORRECT_COLOR)

def color_wrong_word():
    global WRONG_WORDS_NUM
    global TEXT

    WRONG_WORDS_NUM += 1
    TEXT.tag_add("second_word", f"1.{CURRENT_INDEX}", f"1.{CURRENT_INDEX+len(CURRENT_WORDS[CURRENT_WORD_INDEX])}")
    TEXT.tag_config("second_word", foreground=FALSE_COLOR)


def fetch_new_words():
    global CURRENT_WORD_INDEX
    global CURRENT_GROUP_INDEX
    global CURRENT_INDEX
    global CURRENT_WORDS
    global TEXT

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
    TEXT.config(state=NORMAL)
    TEXT.delete("1.0", END)
    TEXT.insert(INSERT, " ".join(CURRENT_WORDS))
    TEXT.config(state=DISABLED)
    TEXT.tag_configure("center", justify='center')


def show_game_result():
    for child in root.winfo_children(): 
        child.destroy()
    if TOTAL_WRITTEN_WORDS == 0:
        typing_speed,accuracy,net_speed = 0,0,0
    else:
        typing_speed = int((TOTAL_WRITTEN_WORDS/TIME_UPPER_LIMIT)*60)
        accuracy = CORRECT_WORDS_NUM/TOTAL_WRITTEN_WORDS
        net_speed = int(typing_speed*accuracy)

    print(f"Typing Speed: {typing_speed}\nAccuracy: {accuracy}\nNet Speed: {net_speed}")
    canvas = Canvas(bg=BACKGROUND_COLOR, width=600, highlightthickness=0)
    canvas.create_oval(25, 25, 175, 175, outline=CORRECT_COLOR, fill=FOREGROUND_COLOR)
    canvas.create_oval(200, 25, 350, 175, outline=CORRECT_COLOR, fill=FOREGROUND_COLOR)
    canvas.create_oval(375, 25, 525, 175, outline=CORRECT_COLOR, fill=FOREGROUND_COLOR)
    canvas.pack(anchor="center", padx=(50,0))

    typing_speed_value_label = Label(root, text = typing_speed, font=("Open Sans", 36), fg=BACKGROUND_COLOR, bg=FOREGROUND_COLOR)
    typing_speed_value_label.place(x=200, y=50)
    typing_speed_label = Label(root, text="WPM", font=("Open Sans", 16), fg=BACKGROUND_COLOR, bg=FOREGROUND_COLOR)
    typing_speed_label.place(x=200, y=110)

    accuracy_value_label = Label(root, text = f"{int(accuracy*100)}%", font=("Open Sans", 35), fg=BACKGROUND_COLOR, bg=FOREGROUND_COLOR)
    accuracy_value_label.place(x=363, y=50)
    accuracy_label = Label(root, text=f"{WRONG_WORDS_NUM} typos", font=("Open Sans", 16), fg=BACKGROUND_COLOR, bg=FOREGROUND_COLOR)
    accuracy_label.place(x=370, y=110)

    net_speed_value_label = Label(root, text = net_speed, font=("Open Sans", 35), fg=BACKGROUND_COLOR, bg=FOREGROUND_COLOR)
    net_speed_value_label.place(x=550, y=50)
    net_speed_label = Label(root, text="Net Speed", font=("Open Sans", 16), fg=BACKGROUND_COLOR, bg=FOREGROUND_COLOR)
    net_speed_label.place(x=540, y=110)
    
    restart_game_button = Button(root, text="Restart Game", command=restart_game)
    restart_game_button.pack()

def restart_game():
    for child in root.winfo_children(): 
        child.destroy()
    setup_game()

def setup_game():
    global CURRENT_WORDS
    global CURRENT_GROUP_INDEX
    global CURRENT_WORD_INDEX
    global CURRENT_INDEX

    global CORRECT_WORDS_NUM
    global WRONG_WORDS_NUM
    global TOTAL_WRITTEN_WORDS

    global CURRENT_TIME
    global TIME_LABEL

    global TEXT
    global TEXT_INPUT

    CURRENT_WORDS = []
    CURRENT_GROUP_INDEX = 0
    CURRENT_WORD_INDEX = 0
    CURRENT_INDEX = 0

    CORRECT_WORDS_NUM = 0
    WRONG_WORDS_NUM = 0
    TOTAL_WRITTEN_WORDS = 0
    CURRENT_TIME = TIME_UPPER_LIMIT

    var_x = StringVar()
    var_x.trace("w", lambda name, index, mode, var_x=var_x: callback(var_x))
    TEXT_INPUT = Entry(root, background=FOREGROUND_COLOR, foreground=BACKGROUND_COLOR, textvariable=var_x, font=("Open Sans", 16))

    read_file()
    TEXT = Text(root, highlightthickness = 0, borderwidth=0, width=75, height=5, fg=FOREGROUND_COLOR, background=BACKGROUND_COLOR, font=("Open Sans", 16))
    TEXT.tag_configure("center", justify='center')
    TEXT.insert(INSERT, " ".join(CURRENT_WORDS))


    TIME_LABEL = Label(root, text = CURRENT_TIME, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=("Open Sans", 16))
    TIME_LABEL.pack(side=TOP, anchor=NW, pady=(20,0), padx=(30,0))
    timer = root.after(1000, update_timer)
    # adding a tag to a part of text specifying the indices
    TEXT.tag_add("center", "1.0", "end") 
    TEXT.configure(state=DISABLED)
    TEXT.pack(pady=(20,0))
    TEXT_INPUT.pack(expand=True, fill='both', padx=(60, 60), pady=(0,100))


def read_file():
    global WORDS
    global CURRENT_WORDS
    with open("./assets/sample_text.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            WORDS = WORDS + [word.strip() for word in line.strip().split(" ") if word.strip()]
        CURRENT_WORDS =  WORDS[0: SHOWN_WORD_UPPER_LIMIT]

def update_timer():
    global CURRENT_TIME
    global TIME_LABEL

    CURRENT_TIME -= 1
    if CURRENT_TIME < 0:
        show_game_result()
    else:
        TIME_LABEL.configure(text=CURRENT_TIME)
        root.after(1000, update_timer)


root = Tk()
root.config(bg=BACKGROUND_COLOR)
root.geometry("800x300")

setup_game()


root.mainloop()