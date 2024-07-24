from tkinter import *

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

TIME_UPPER_LIMIT = 10
CURRENT_TIME = TIME_UPPER_LIMIT

def callback(var_x):
    if len(var_x.get()) and (var_x.get()[-1] == " " or var_x.get()[-1] == ""):
        word = var_x.get()
        text_input.delete(0, END)
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

    CORRECT_WORDS_NUM += 1
    text.tag_add("first_word", f"1.{CURRENT_INDEX}", f"1.{CURRENT_INDEX+len(CURRENT_WORDS[CURRENT_WORD_INDEX])}")
    text.tag_config("first_word", foreground=CORRECT_COLOR)

def color_wrong_word():
    global WRONG_WORDS_NUM

    WRONG_WORDS_NUM += 1
    text.tag_add("second_word", f"1.{CURRENT_INDEX}", f"1.{CURRENT_INDEX+len(CURRENT_WORDS[CURRENT_WORD_INDEX])}")
    text.tag_config("second_word", foreground=FALSE_COLOR)


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
    typing_speed = int((TOTAL_WRITTEN_WORDS/TIME_UPPER_LIMIT)*60)
    accuracy = CORRECT_WORDS_NUM/TOTAL_WRITTEN_WORDS
    net_speed = int(typing_speed*accuracy)
    print(f"Typing Speed: {typing_speed}\nAccuracy: {accuracy}\nNet Speed: {net_speed}")
    canvas = Canvas(bg=BACKGROUND_COLOR, width=600, highlightthickness=0)
    canvas.create_oval(25, 25, 175, 175, outline="black", fill=FOREGROUND_COLOR)
    canvas.create_oval(200, 25, 350, 175, outline="black", fill=FOREGROUND_COLOR)
    canvas.create_oval(375, 25, 525, 175, outline="black", fill=FOREGROUND_COLOR)
    canvas.pack(anchor="center", padx=(50,0))
      
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
    CURRENT_TIME -= 1
    if CURRENT_TIME < 0:
        show_game_result()
    else:
        time_label.configure(text=CURRENT_TIME)
        root.after(1000, update_timer)


root = Tk()
root.config(bg=BACKGROUND_COLOR)
root.geometry("800x300")

var_x = StringVar()
var_x.trace("w", lambda name, index, mode, var_x=var_x: callback(var_x))
text_input = Entry(root, background=FOREGROUND_COLOR, foreground=BACKGROUND_COLOR, textvariable=var_x, font=("Open Sans", 16))

read_file()
text = Text(root, highlightthickness = 0, borderwidth=0, width=75, height=5, fg=FOREGROUND_COLOR, background=BACKGROUND_COLOR, font=("Open Sans", 16))
text.tag_configure("center", justify='center')
text.insert(INSERT, " ".join(CURRENT_WORDS))

time_label = Label(root, text = CURRENT_TIME, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=("Open Sans", 16))
time_label.pack(side=TOP, anchor=NW, pady=(20,0), padx=(30,0))
timer = root.after(1000, update_timer)
# adding a tag to a part of text specifying the indices
text.tag_add("center", "1.0", "end") 
text.configure(state=DISABLED)
text.pack(pady=(20,0))
text_input.pack(expand=True, fill='both', padx=(60, 60), pady=(0,100))


root.mainloop()