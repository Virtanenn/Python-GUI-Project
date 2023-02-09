# Creator: Timo Virtanen


"""'
GUI-PROJECT - Hangman
A simple GUI project made during University course.
Goal of this project was to learn a little GUI programming with Tkinter
"""

import sys
from tkinter import*
import random
import os

"""
Class Hangman has all the functionality of the game.
__init__:ssä Initializes every picture, button and texts.
"""


class Hangman:
    def __init__(self, secret_word):

        self.__wrong_guesses = 0
        self.__list_of_wrong_letters = []

        self.__right_guesses = 0
        self.__secret_word = secret_word.lower()
        # Resolved: every letter found from the unknown word
        self.__resolved = "_  "*len(secret_word)
        self.__mainwindow = Tk()

        # placing the picture
        self.__canvas = Canvas(self.__mainwindow, width=500, height=350)
        self.__canvas.pack()
        self.__img = PhotoImage(file="hirsipuu_0.gif")
        self.__canvas.create_image(250, -10, anchor=N, image=self.__img)

        self.__wrong_letters = Label(
            self.__mainwindow, text="")
        self.__wrong_letters.config(font=('Lucida Calligraphy', 15), fg='red')
        self.__wrong_letters.pack(anchor=N)

        # letters found
        self.__resolved_label = Label(self.__mainwindow, text=self.__resolved)
        self.__resolved_label.config(font=('Helvatical bold', 30))
        self.__resolved_label.pack(side=TOP, anchor=CENTER)

        self.__winning_label = Label(self.__mainwindow, text="")
        self.__winning_label.pack(side=TOP, anchor=CENTER)
        self.__winning_label.config()

        # placing the buttons
        self.__list_of_letter_buttons = []
        for i in range(26):
            letter = chr(i + 65)
            self.__letter_button = Button(self.__mainwindow, text=f"{letter}")
            self.__letter_button.config(
                command=lambda letter=letter: self.insert_letter(letter),
                height=5, width=5)
            self.__letter_button.pack(side=LEFT, anchor=CENTER)
            self.__list_of_letter_buttons.append(self.__letter_button)


        self.__restart_button = Button(
            self.__mainwindow, text="Restart", command=self.restart_program)
        self.__restart_button.config(height=5, width=20, bg='RoyalBlue1')
        self.__restart_button.pack(side=LEFT)

        #Stops the program
        self.__stop_button = Button(self.__mainwindow, text="QUIT",
                                    command=self.exit_confirmation)
        self.__stop_button.config(height=5, width=20, bg='tomato')
        self.__stop_button.pack(side=LEFT)

    def insert_letter(self, letter):
        # if the letter is not found in the secret word
        if self.__secret_word.find(letter.lower()) < 0:
            self.wrong_guess(letter)

        else:
            # Deactivates button clicked
            self.__list_of_letter_buttons[ord(letter) - 65]["state"] = DISABLED
            ord_number = 0
            # lists resolved letters
            listed_resolved = list(self.__resolved)

            for i in self.__secret_word.upper():
                if i == letter:
                    listed_resolved[ord_number*3] = letter
                    self.__right_guesses += 1
                ord_number += 1

            self.__resolved = "".join(listed_resolved)
            self.__list_of_letter_buttons[ord(letter) - 65].config(bg="green2")
            self.__resolved_label["text"] = self.__resolved

            # checks if you won the game
            if self.__right_guesses == len(self.__secret_word):
                self.game_end()

    def wrong_guess(self, letter):
        # appends wrong letter to list.
        self.__list_of_wrong_letters.append(letter)
        self.__wrong_letters["text"] = "  ".join(self.__list_of_wrong_letters)

        # Deactivates button
        self.__list_of_letter_buttons[ord(letter) - 65].config(bg="brown3")
        self.__list_of_letter_buttons[ord(letter) - 65]["state"] = DISABLED

        self.__wrong_guesses += 1
        # Changes picture after wrong guess
        self.__img = PhotoImage(file="hirsipuu_" +
                                     str(self.__wrong_guesses) + ".gif")
        self.__canvas.create_image(250, -10, anchor=N, image=self.__img)

        # Game ends if there are 8 wrong guesses
        if self.__wrong_guesses == 8:
            self.losing()

    def losing(self):
        self.__resolved_label["text"] = "Y  O  U      L  O  S  T!"
        self.__resolved_label.config(font=('Lucida Calligraphy', 26), fg='red')

        # Revealing the word
        self.__wrong_letters["text"] = "Answer: " + self.__secret_word
        self.__restart_button["text"] = "Try again"

        # Deactivates every letterbutton
        for i in range(26):
            letter = chr(i + 65)
            self.__list_of_letter_buttons[ord(letter) - 65]["state"] = DISABLED

    def game_end(self):
        # winning the game
        self.__winning_label["text"] = "Y  O  U      W  O  N!"
        self.__winning_label.pack(side=TOP)
        self.__winning_label.config(font=('Aldo the Apache', 30), fg='green')

        # Changing color and text of restart button
        self.__restart_button["text"] = "Play again"
        self.__restart_button.config(bg="green2")

        # Deactivating letter buttons
        for i in range(26):
            letter = chr(i + 65)
            self.__list_of_letter_buttons[ord(letter) - 65]["state"] = DISABLED

    def exit_confirmation(self):
        # Confirming if you want to exit
        self.__stop_button["text"] = "Are you sure?"
        self.__stop_button.config(bg='red', command=self.exit)

    def exit(self):
        self.__mainwindow.destroy()

    def start(self):
        self.__mainwindow.mainloop()
        # Activates mainloop

    @staticmethod
    def restart_program():
        python = sys.executable
        os.execl(python, python, *sys.argv)


"""
Main calls for readfile and initializes game
"""


def main():
    words = read_file()
    # random.choicet valitsee sattumalta yhden sanan listasta
    secret_word = random.choice(words)
    ui = Hangman(secret_word)
    ui.start()


"""
read_file reads the file processes it
"""


def read_file():
    file = open("list_of_words.txt", mode="r")
    words = []
    for line in file:
        words.append(line.strip())
    return words


if __name__ == "__main__":
    main()
