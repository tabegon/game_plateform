from tkinter import *
import random


def stvalentin():
    global players
    players = ['💗', '💐']
    new_game()


def genre():
    global players
    players = ['👧', '👦']
    new_game()


def halloween():
    global players
    players = ['🎃', '👻']
    new_game()


def noel():
    global players
    players = ['🎄', '🎅']
    new_game()


def simple():
    global players
    players = ['X', 'O']
    new_game()


def nourriture():
    global players
    players = ['🍿', '🍔']
    new_game()


def next_turn(row, column):
    global player
    if buttons[row][column]['text'] == "" and check_winner() is False:
        if player == players[0]:
            buttons[row][column]['text'] = player
            if check_winner() is False:
                player = players[1]
                label.config(text=("tour de " + players[1]))
            elif check_winner() is True:
                label.config(text=(players[0] + " à gagner... " + players[1] + " t'es nul(le)"))
            elif check_winner() == "ÉGALITÉ!":
                label.config(text=("ÉGALITÉ!"))
        else:
            buttons[row][column]['text'] = player
            if check_winner() is False:
                player = players[0]
                label.config(text=("tour de " + players[0]))
            elif check_winner() is True:
                label.config(text=(players[1] + " à gagner... " + players[0] + " t'es nul(le)"))
            elif check_winner() == "ÉGALITÉ!":
                label.config(text=("ÉGALITÉ!"))


def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        return True

    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != '':
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        return True

    elif empty_spaces() is False:
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="yellow")
        return "ÉGALITÉ!"

    else:
        return False


def empty_spaces():
    spaces = 9
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != "":
                spaces -= 1

    if spaces == 0:
        return False
    else:
        return True


def new_game():
    global player
    player = random.choice(players)
    label.config(text="tour de " + player)
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg="#F0F0F0")

def main():
    global label, buttons, player, players
    window = Tk()
    window.title('Morpion - JEU CLASSIQUE')
    players = ['#', '@']
    player = random.choice(players)
    buttons = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]
    label = Label(window, text="tour de " + player, font=('consolas', 40))
    label.pack(side="top")

    reset_button = Button(window, text="Recommencer", font=('consolas', 20), command=new_game)
    reset_button.pack(side='top')

    frame = Frame(window)
    frame.pack()

    for row in range(3):
        for column in range(3):
            buttons[row][column] = Button(frame, text="", font=('consolas', 40), width=5, height=2,
                                        command=lambda row=row, column=column: next_turn(row, column))
            buttons[row][column].grid(row=row, column=column)

    menu_u = Menu(window)

    menu_edition = Menu(menu_u)
    menu_u.add_cascade(label='Edition', menu=menu_edition)
    mode_jeu = Menu(menu_edition)
    option_jeu = Menu(menu_edition)
    menu_edition.add_cascade(label='Mode de Jeu', menu=mode_jeu)
    menu_edition.add_cascade(label='Option de marquage', menu=option_jeu)

    mode_jeu.add_command(label='2 joueurs')
    mode_jeu.add_command(label="Contre l'IA (SIMPLE)")
    mode_jeu.add_command(label="Contre l'IA (IMPOSSIBLE)")

    option_jeu.add_command(label='Original', command=lambda: simple())
    option_jeu.add_command(label='Nourriture', command=lambda: nourriture())
    option_jeu.add_command(label='Noël', command=lambda: noel())
    option_jeu.add_command(label='Halloween', command=lambda: halloween())
    option_jeu.add_command(label='Genre', command=lambda: genre())
    option_jeu.add_command(label='St Valentin', command=lambda: stvalentin())

    menu_edition.add_command(label='Recommencer', command=lambda: new_game())
    menu_u.add_command(label='Quitter', command=lambda: quit())

    window.config(menu=menu_u)

    window.mainloop()
