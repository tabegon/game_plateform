from random import randint
import tkinter
from tkinter import ttk
import tkinter.ttk

class Tic_Tac_Boom:
    # ---------------------------- Initialisation du jeu et création des interfaces ----------------------------
    def __init__(self):
        """
        Initialisation de la classe avec leurs variable
        """
        # Les joueurs
        self.players = ['O', 'X']
        # Le joueur qui commence
        self.current_player = "X"
        # Créations des grilles
        self.boards = [[[" " for i in range(3)] for i in range(3)] for i in range(9)]
        # Création de la grille principale
        self.board_wins = [" " for i in range(9)]
        # Faire commencer dans le morpion du milieu
        self.active_board = 4

        # Initialisation des boutons et des frames
        self.buttons = []
        self.frames = []

        self.ia_random = False
        self.ia_moyenne = False        

        self.fenetre = tkinter.Tk()
        self.create_ui()

    def create_ui(self):
        """
        Crée l'interface utilisateur du jeu
        Cette fonction ne retourne rien car elle créer seulement l'interface à l'intérieur de la fonction
        """
        # Grille principale
        for big_row in range(3):
            for big_col in range(3):
                # Frames de l'interface graphique
                frame = tkinter.Frame(self.fenetre, highlightbackground="black", highlightthickness=2)
                # Sauvegarder dans la variable pour pouvoir changer sa highlightthickness
                self.frames.append(frame)
                # Placement de la frame
                frame.grid(row=big_row, column=big_col, padx=8, pady=4)
                board_buttons = []
                # Grilles secondaires
                for small_row in range(3):
                    for small_col in range(3):
                        # Placement de la grille
                        btn = tkinter.Button(frame, text=" ", font=("Arial", 20), width=5, height=2, bg='white',
                                        command=lambda br=big_row, bc=big_col, sr=small_row, sc=small_col: self.play(br, bc, sr, sc))
                        btn.grid(row=small_row, column=small_col)
                        # Sauvegarde du boutton dans la variable
                        board_buttons.append(btn)
                self.buttons.append(board_buttons)
        self.active_case()

        self.timerX = tkinter.Label(self.fenetre, text=" ", font=("Arial", 25))
        self.timerX.grid(row=0, column=3)

        self.button_game = tkinter.Button(self.fenetre, text=' New Game ', font=('Arial', 25), command=self.new_game)
        self.button_game.grid(row=1, column=3)


        self.timerO = tkinter.Label(self.fenetre, text=" ", font=("Arial", 25))
        self.timerO.grid(row=2, column=3)
    
    # ---------------------------- Fonctions d'un déroulement d'un coup ----------------------------

    def play(self, big_row, big_col, small_row, small_col):
    
        board_index = 3 * big_row + big_col # Nous donne l'index du plateau de morpion, 
                                            # 3*big row: nous donne l'indice de la ligne et +big_col nous donne l'indice colonne

        small_board_index = 3 * small_row + small_col # Nous donne l'index de l'endroit où nous avons jouer sur le petit plateau

        if self.active_board == board_index or self.active_board == None:
            # Ce qu'on joue
            self.boards[board_index][small_row][small_col] = self.current_player        # Remplace " " par 'X' ou 'O'
            self.buttons[board_index][small_board_index]["text"] = self.current_player  # Change le texte du bouton pour avoir le texte du joueur
            self.buttons[board_index][small_board_index]["state"] = "disabled"          # Empêche le fait de pouvoir rappuyer sur le bouton
        else:
            print('Vous vous êtes trompés de plateau')
            return

            
        if self.check_win(self.boards[board_index]):
            self.board_wins[board_index] = self.current_player
            self.case_color_win(board_index)

        else:
            if self.check_draw(board_index):
                self.reset_board(board_index)

        if self.check_global_win():
            if self.current_player == "X":
                print('X a gagner')
                
            else:
                print('O a gagner')
            
            self.fenetre.quit()
            print('Partie terminée')
                
            
        if self.board_wins[small_board_index] == ' ':
            self.active_board = 3 * small_row + small_col
        else:
            self.active_board = None
        self.active_case()

        self.next_turn()

        if self.ia_random == True:
            self.ia_random_play(self.active_board)
        elif self.ia_moyenne == True:
            self.ia_moyenne_play(self.active_board)
        
        


    def active_case(self):
        """
        Surligne la bordure de la case où l’on doit jouer
        """
        for i, frame in enumerate(self.frames):                            # On regarde toutes les frames une par une et on les énumères dans la variable i
            if self.active_board is None or self.board_wins[i] != " ":
                frame.configure(highlightbackground="black", highlightthickness=2)
            elif i == self.active_board:
                frame.configure(highlightbackground="darkblue", highlightthickness=4)
            else:
                frame.configure(highlightbackground="black", highlightthickness=2)

    def next_turn(self):
        """
        Permet de changer de tour, et donc ainsi de changer de joueur
        """
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def case_color_win(self, board_index):
        """
        Colorie le morpion gagné de la couleur du joueur
        @param board_index: integer, nous permet de retrouver le plateau dans le grand
        @param player: 'X' ou 'O', pour choisir la bonne couleur
        """
        for btn in self.buttons[board_index]:
            if self.current_player == 'X' :
                self.boards[board_index] = btn.configure(bg='blue')
            else :
                self.boards[board_index] = btn.configure(bg='red')

    def check_win(self, board):
        """ 
	    Vérifie la victoire sur un morpion
	    @param board: matrice du plateau de morpion
	    @return True sssi un plateau a win
	    """
        if board[0][0] == board[1][1] == board[2][2] != ' ' :
            return True
        if board[2][0] == board[1][1] == board[0][2] != ' ' :
            return True
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ' :
                return True
            if board[0][i] == board[1][i] == board[2][i] != ' ' :
                return True

    def check_draw(self, board_index): 
        """
        Vérifie si il y a égalité sur un petit plateau de morpion
        @param board_index: integer, pour trouver où se situe le morpion dans le grand
        @return True sssi égalité 
        """
        for i in range(3):
            for j in range(3) :
                if self.boards[board_index][i][j] == ' ' :
                    return False
        return True

    def check_global_win(self):
        """
	    Permet de créer une matrice pour le grand plateau de morpion avant
		d'appeller check_win pour vérifier si on a gagné l'ultimate morpion
        @return True sssi check_win == True
        """
        board = [[self.board_wins[3 * i + j] for j in range(3)] for i in range(3)] # Transformation de notre liste du plateau de morpion en matrice
        return self.check_win(board)

    def reset_board(self, board_index):
        """
        Remet le plateau choisi vide
        @param board_index: integer, pour trouver où se situe le 
        morpion dans le grand puis le vider
        """
        self.boards[board_index] = [[" " for i in range(3)] for i in range(3)]  # Remise à 0 du petit plateau
        self.board_wins[board_index] = " "                                      # Toujours pas de vainqueurs
        for i in range(9):
            btn = self.buttons[board_index][i]                                  # Récupération du bouton dans notre liste
            btn["text"] = " "                                                   # Sans texte
            btn["state"] = "normal"                                             # Et on peut cliquer sur le bouton

    def new_game(self) :
        """
        crée une nouvelle partie en suprimant le texte sur les boutons et en bloquant le premier coup au milieu
	    """ 
        for i in range(9):
            for btn in self.buttons[i]:
                self.boards[i] = btn.configure(bg='white')
            self.reset_board(i)
        self.active_board = 4
        self.active_case()

    # ---------------------------- Fonctions des timers ----------------------------

    def temps_1min(self):
        self.clockO = 60
        self.clockX = 60
        self.update_timers()  # Méthode qui gère le timer

    def temps_5min(self):
        self.clockO = 5 * 60
        self.clockX = 5 * 60
        self.update_timers()  # Méthode qui gère le timer

    def temps_10min(self):
        self.clockO = 10 * 60
        self.clockX = 10 * 60
        self.update_timers()  # Méthode qui gère le timer

    def update_timers(self):
        # Affiche le temps restants aux autres pendules
        self.timerX.configure(text=f'X: {self.clockX}')
        self.timerO.configure(text=f'O: {self.clockO}')

        if self.clockX != None and self.clockO != None:
            # Diminue le bon compteur
            if self.current_player == 'X' and self.clockX >= 0:
                self.clockX -= 1
            elif self.current_player == 'O' and self.clockO >= 0:
                self.clockO -= 1

            if self.clockX == 0:
                print('X a gagné au temps')
                self.fenetre.quit()
            elif self.clockO == 0:
                print('O a gagné au temps')
                self.fenetre.quit()

            # Répète toutes les 1 seconde
            self.fenetre.after(1000, self.update_timers)
        else:
            self.timerX.configure(text=' ')
            self.timerO.configure(text=' ')

    def without_timer(self):
        self.clockX = None
        self.clockO = None
        self.timerX.configure(text=' ')
        self.timerO.configure(text=' ')

    # ---------------------------- Fonctions des coups des ia ----------------------------

    def ia_random_play(self, board_index) : 
        i_ia = randint(0,2)
        j_ia = randint(0,2)
        if board_index == None:
            board_index = randint(0,8)
            while self.board_wins[board_index] != " ":
                board_index = randint(0,8)
        while self.boards[board_index][i_ia][j_ia] != " ":
            i_ia = randint(0,2)
            j_ia = randint(0,2)
        # Fait jouer l'ia
        
        self.boards[board_index][i_ia][j_ia] = self.current_player        # Remplace " " par 'X' ou 'O'
        self.buttons[board_index][3*i_ia+j_ia]["text"] = self.current_player  # Change le texte du bouton pour avoir le texte du joueur
        self.buttons[board_index][3*i_ia+j_ia]["state"] = "disabled"          # Empêche le fait de pouvoir rappuyer sur le bouton


        if self.check_win(self.boards[board_index]):
            self.board_wins[board_index] = self.current_player
            self.case_color_win(board_index)

        else:
            if self.check_draw(board_index):
                self.reset_board(board_index)

        if self.check_global_win():
            if self.current_player == "X":
                print('X a gagner')
                return
            else:
                print('O a gagner')
                return

        if self.board_wins[3*i_ia+j_ia] == ' ':
            self.active_board = 3 * i_ia + j_ia
        else:
            self.active_board = None
        self.active_case()

        self.next_turn()

    def active_ia_random(self):
        if self.ia_random == False:
            self.ia_random = True
        else:
            self.ia_random = False

    def ia_moyenne_play(self, board_index) :
        def play_ia():
                    # Fait jouer l'ia
            
                    self.boards[board_index][i][j] = self.current_player        # Remplace " " par 'X' ou 'O'
                    self.buttons[board_index][3*i+j]["text"] = self.current_player  # Change le texte du bouton pour avoir le texte du joueur
                    self.buttons[board_index][3*i+j]["state"] = "disabled"          # Empêche le fait de pouvoir rappuyer sur le bouton


                    if self.check_win(self.boards[board_index]):
                        self.board_wins[board_index] = self.current_player
                        self.case_color_win(board_index)

                    else:
                        if self.check_draw(board_index):
                            self.reset_board(board_index)

                    if self.check_global_win():
                        if self.current_player == "X":
                            print('X a gagner')
                            return
                        else:
                            print('O a gagner')
                            return

                    if self.board_wins[3*i+j] == ' ':
                        self.active_board = 3 * i + j
                    else:
                        self.active_board = None
                    self.active_case()

                    self.next_turn()
                    
        coins = [[0, 0], [0, 2], [2, 0], [2, 2]]
        milieu = [[1, 1]]
        arete = [[0, 1], [1, 0], [1, 2], [2, 1]]

        for objet in coins:
            i = objet[0]
            j = objet[1]
            if self.boards[board_index][i][j] == ' ':
                play_ia()
                return
        for objet in milieu:
            i = objet[0]
            j = objet[1]
            if self.boards[board_index][i][j] == ' ':
                play_ia()
                return
        for objet in arete:
            i = objet[0]
            j = objet[1]
            if self.boards[board_index][i][j] == ' ':
                play_ia()
                return
                
    def active_ia_moyenne(self):
        if self.ia_moyenne == False:
            self.ia_moyenne = True
        else:
            self.ia_moyenne = False


    # ---------------------------- Fonctions de la barre d'analyse ----------------------------
        # On a essayé de faire un système d'analyse et d'ia se basant la dessus en vain
"""    def rating(self) :
        # coins + 1 
        
        self.rate = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.rating_var = 0    # variable differente de rate pour une meilleure précision de l'ia difficile  

    def rating_petit(self) :
        # si il y a une valeur + 1 
        for i in range(8) :
            for j in range(3):
                for h in range(3) : 
                    if self.boards[j][h]  == 'X' :
                        self.rate[i] += 0,5

        for i in range(9) : 
            for j in range(3):
                for h in range(3) : 
                    if self.boards[j][h]  == 'O' :
                        self.rate[i] -= 0,5

        #si dans les coins + 1
        for i in range(9) : 
            if self.boards[i][0][0] =='X':        
                self.rate[i] += 1 
            if self.boards[i][2][0] =='X': 
                self.rate[i] += 1
            if self.boards[i][0][2] =='X': 
                self.rate[i] += 1
            if self.boards[i][2][2] =='X': 
                self.rate[i] += 1
            
        for i in range(9) : 
            if self.boards[i][0][0] =='O':        
                self.rate[i] -= 1 
            if self.boards[i][2][0] =='O': 
                self.rate[i] -= 1
            if self.boards[i][0][2] =='O': 
                self.rate[i] -= 1
            if self.boards[i][2][2] =='O': 
                self.rate[i] -= 1
            
        # si 2 aligné + 2 
            for i in range(9) : 
                for j in range(2) : 
                    for h in range(2) :
                        if self.boards[i][j][h] == self.boards[i][j][h+1] == 'X' :
                            self.rate[i] += 2
                        if self.boards[i][j][h] == self.boards[i][j+1][h] == 'X' :
                            self.rate[i] += 2 
                
                if self.boards[i][0][0] == self.boards[i][1][1] =='X':
                    self.rate[i] += 2
                
                if self.boards[i][2][2] == self.boards[i][1][1] =='X':
                    self.rate[i] += 2

                if self.boards[i][2][2] == self.boards[i][0][0] =='X':
                    self.rate[i] += 2
                
                if self.boards[i][2][0] == self.boards[i][1][1] =='X':
                    self.rate[i] += 2
                
                if self.boards[i][0][2] == self.boards[i][1][1] =='X':
                    self.rate[i] += 2
                
                if self.boards[i][2][0] == self.boards[i][0][2] =='X':
                    self.rate[i] += 2

        for i in range(9) : 
                for j in range(2) : 
                    for h in range(2) :
                        if self.boards[i][j][h] == self.boards[i][j][h+1] == 'O' :
                            self.rate[i] -= 2
                        if self.boards[i][j][h] == self.boards[i][j+1][h] == 'O' :
                            self.rate[i] -= 2 
                
                if self.boards[i][0][0] == self.boards[i][1][1] =='O':
                    self.rate[i] -= 2
                
                if self.boards[i][2][2] == self.boards[i][1][1] =='O':
                    self.rate[i] -= 2

                if self.boards[i][2][2] == self.boards[i][0][0] =='O':
                    self.rate[i] -= 2
                
                if self.boards[i][2][0] == self.boards[i][1][1] =='O':
                    self.rate[i] -= 2
                
                if self.boards[i][0][2] == self.boards[i][1][1] =='O':
                    self.rate[i] -= 2
                
                if self.boards[i][2][0] == self.boards[i][0][2] =='O':
                    self.rate[i] -= 2
            
        return self.rate

    def rating_grand(self) :
        # si un morpion gagné +10 
        for j in range(3):
            for h in range(3) : 
                print(j, h)
                if self.board_wins[j][h] == 'X' :
                    self.rating_bar += 10

        for j in range(3):
            for h in range(3) : 
                if self.board_wins[j][h] == 'O' :
                    self.rating_bar -= 10

        #si au centre +30
        if self.board_wins[1][1] == 'X' :
            self.rating_bar += 30
        if self.board_wins[1][1] == '0' :
            self.rating_bar -= 30 


        #si 2 aligné +20
            for i in range(9) : 
                for j in range(2) : 
                    for h in range(2) :
                        if self.board_wins[j][h] == self.board_wins[j][h+1] == 'X' :
                            self.rating_bar += 20
                        if self.board_wins[i][j][h] == self.board_wins[j+1][h] == 'X' :
                            self.rating_bar += 20 
                
                if self.board_wins[0][0] == self.board_wins[1][1] =='X':
                    self.rating_bar += 20
                
                if self.board_wins[2][2] == self.board_wins[1][1] =='X':
                    self.rating_bar += 20

                if self.board_wins[2][2] == self.board_wins[0][0] =='X':
                    self.rating_bar += 20
                
                if self.board_wins[2][0] == self.board_wins[1][1] =='X':
                    self.rating_bar += 20
                
                if self.board_wins[0][2] == self.board_wins[1][1] =='X':
                    self.rating_bar += 20
                
                if self.board_wins[2][0] == self.board_wins[0][2] =='X':
                    self.rating_bar += 20

        for i in range(9) : 
                for j in range(2) : 
                    for h in range(2) :
                        if self.board_wins[j][h] == self.board_wins[j][h+1] == 'O' :
                            self.rating_bar -= 20
                        if self.board_wins[j][h] == self.board_wins[j+1][h] == 'O' :
                            self.rating_bar -= 20 
                
                if self.board_wins[0][0] == self.board_wins[1][1] =='O':
                    self.rating_bar -= 20
                
                if self.board_wins[2][2] == self.board_wins[1][1] =='O':
                    self.rating_bar -= 20

                if self.board_wins[2][2] == self.board_wins[0][0] =='O':
                    self.rating_bar -= 20
                
                if self.board_wins[2][0] == self.board_wins[1][1] =='O':
                    self.rating_bar -= 20
                
                if self.board_wins[0][2] == self.board_wins[1][1] =='O':
                    self.rating_bar -= 20
                
                if self.board_wins[2][0] == self.board_wins[0][2] =='O':
                    self.rating_bar -= 20

    def ia_difficile_play(self, board_index) : 
        rate = self.rate
        max_rate = -50
        for i in range(9) :
            if rate[i] > max_rate :
                max_rate = rate[i]
        max_rate_i = -50
        for j in range(3) :
            for h in range(3) : 
                new_rate = self.rating_petit()
                if new_rate > max_rate_i :
                    max_rate_i = self.rating_petit()
                    j_ia = j
                    i_ia = h

        # Fait jouer l'ia
        
        self.boards[board_index][i_ia][j_ia] = self.current_player        # Remplace " " par 'X' ou 'O'
        self.buttons[board_index][3*i_ia+j_ia]["text"] = self.current_player  # Change le texte du bouton pour avoir le texte du joueur
        self.buttons[board_index][3*i_ia+j_ia]["state"] = "disabled"          # Empêche le fait de pouvoir rappuyer sur le bouton


        if self.check_win(self.boards[board_index]):
            self.board_wins[board_index] = self.current_player
            self.case_color_win(board_index)

        else:
            if self.check_draw(board_index):
                self.reset_board(board_index)

        if self.check_global_win():
            if self.current_player == "X":
                print('X a gagner')
                return
            else:
                print('O a gagner')
                return

        if self.board_wins[3*i_ia+j_ia] == ' ':
            self.active_board = 3 * i_ia + j_ia
        else:
            self.active_board = None
        self.active_case()

        self.next_turn()
"""

    
# Création de la partie:

partie = Tic_Tac_Boom()



menubar = tkinter.Menu(partie.fenetre)
menu = tkinter.Menu(menubar)
menu.add_command(label="Activer/Désactiver IA Random", command=partie.active_ia_random)
menu.add_command(label="Activer/Désactiver IA Moyenne", command=partie.active_ia_moyenne)
menubar.add_cascade(label="IA", menu=menu)

menu_timer = tkinter.Menu(menubar)
menu_timer.add_command(label="no timer", command=partie.without_timer)
menu_timer.add_command(label="timer 1 minute", command=partie.temps_1min)
menu_timer.add_command(label="timer 5 minutes", command=partie.temps_5min)
menu_timer.add_command(label="timer 10 minute", command=partie.temps_10min)
menubar.add_cascade(label="Clock", menu=menu_timer)

partie.fenetre.config(menu=menubar)
partie.fenetre.mainloop()