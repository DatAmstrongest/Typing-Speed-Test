from tkinter import *

WORDS = []
CURRENT_WORDS = []
CURRENT_GROUP_INDEX = 0
CURRENT_WORD_INDEX = 0
CURRENT_INDEX = 0

def callback(var_x):
    if var_x.get()[-1] == " " or var_x.get()[-1] == "":
        global CURRENT_GROUP_INDEX
        global CURRENT_WORD_INDEX
        global CURRENT_WORDS
        global CURRENT_INDEX

        word = var_x.get()
        text_input.delete(0, END)

        if word.strip() == CURRENT_WORDS[CURRENT_WORD_INDEX].strip():
            text.tag_add("first_word", f"1.{CURRENT_INDEX}", f"1.{CURRENT_INDEX+len(word)}")
            text.tag_config("first_word", foreground="#08D9D6")
        else:
            text.tag_add("second_word", f"1.{CURRENT_INDEX}", f"1.{CURRENT_INDEX+len(CURRENT_WORDS[CURRENT_WORD_INDEX])}")
            text.tag_config("second_word", foreground="#FF2E63")
        CURRENT_INDEX += len(CURRENT_WORDS[CURRENT_WORD_INDEX])+1
        CURRENT_WORD_INDEX += 1
        if CURRENT_WORD_INDEX == 10:
            CURRENT_GROUP_INDEX += 1
            CURRENT_WORD_INDEX = 0  
            CURRENT_WORDS = WORDS[10*CURRENT_GROUP_INDEX: 10*CURRENT_GROUP_INDEX+10]
            CURRENT_INDEX = 0
            text.config(state=NORMAL)
            text.delete("1.0", END)
            text.insert(INSERT, " ".join(CURRENT_WORDS))
            text.config(state=DISABLED)
            text.tag_configure("center", justify='center')

    return True

def read_file():
    global WORDS
    global CURRENT_WORDS
    with open("./assets/sample_text.txt", "r") as file:
        text = file.read()
        WORDS = text.split(" ")
        CURRENT_WORDS = WORDS[0:10]
            

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