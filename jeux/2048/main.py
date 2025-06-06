
 #Programme réalisé par ROCHETTE Clément, ARTOLA Lucas et MESSINA Lucas

import tkinter as tk        #Ce module crée l'interface graphique
from tkinter import messagebox  #Affiche la fenêtre d'alerte si le joueur a perdu
import random
import os   #Ce module permet d'intéragir avec le système de fichiers. Ici le fichier 'highscore.txt'

TAILLE_GRILLE = 4
#On crée le dictionnaire associant chaqe valeur à une couleur
COULEURS = {0: "#ccc0b3", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
        128: "#edcf72", 256: "#fc8f0b", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}

class Jeu2048: #On crée une classe qui va gérer tout le jeu 2048
    def __init__(self, master):
        """
        Initialise une instance de l'interface graphique du jeu 2048
        @param master: La fenêtre principale Tkinter dans laquelle l'interface du jeu sera affichée
        @return: Aucun. Il s'agit d'un constructeur
        """
        #Initialise la fenêtre principale
        self.master = master
        self.master.title("2048")
        #Initialise la grille 4x4 vide
        self.grille = [[0]*TAILLE_GRILLE for x in range(TAILLE_GRILLE)] 
        self.score = 0

        self.highscore = self.charger_highscore() #On charge le meilleur score qui est stocké dans un fichier
        #Cette partie se charge d'afficher le score
        self.score_label = tk.Label(master, text="Score : 0", font=("Helvetica", 18))
        self.score_label.pack(pady=(10, 0))
        #Celle-ci se charge d'afficher le meilleur score
        self.highscore_label = tk.Label(master, text="Meilleur : " + str(self.highscore), font=("Helvetica", 14))
        self.highscore_label.pack(pady=(0, 10))
        #Cela affiche le cadre contenant la grille
        self.frame = tk.Frame(master, bg="#bbada0")
        self.frame.pack()
        #La grille d'étiquettes pour l'affichage
        self.labels = [[None]*TAILLE_GRILLE for x in range(TAILLE_GRILLE)]
        self.init_interface_grille()
        #Ici on ajoute les deux tuiles initiales 
        self.ajouter_tuile()
        self.ajouter_tuile()
        self.afficher()
        #On lie les touches fléclées aux déplacements 
        self.master.bind("<Key>", self.clavier)

    def charger_highscore(self):
        """
        Charge le meilleur score enregistré dans un fichier texte
        @param self: instance du jeu contenant les attributs, c'est à dire : grille, score et autre
        @return int: le score le plus élevé enregistré, ou 0 si le fichier n'existe pas ou si c'est la première partie
        """
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                texte = f.read()
                if texte.isdigit(): #On vérifie que le contenu soit bien un nombre
                    return int(texte)
        return 0

    def sauvegarder_highscore(self):
        """
        Sauvegarde le meilleur score actuel dans le fichier texte
        @param self: instance du jeu contenant le score à enregistrer
        @return: il n'y a rien à retouner
        """
        with open("highscore.txt", "w") as f:
            f.write(str(self.highscore))

    def init_interface_grille(self):
        """
        Initialise l'interface graphique de la grille du jeu
        @param self: instance du jeu
        @return: il n'y a rien à retourner
        """
        for i in range(TAILLE_GRILLE):
            for j in range(TAILLE_GRILLE):
                l = tk.Label(self.frame, text="", width=4, height=2, font=("Helvetica", 32, "bold"),
                             bg="#ccc0b3", fg="#776e65", relief="ridge", bd=4)
                l.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self.labels[i][j] = l   #On stocke le label pour y accéder plus tard

    def afficher(self):
        for i in range(TAILLE_GRILLE):
            for j in range(TAILLE_GRILLE):
                val = self.grille[i][j]
                l = self.labels[i][j]
                if val != 0:
                    l.config(text=str(val), bg=COULEURS.get(val, "#3c3a32"))
                else:
                    l.config(text="", bg=COULEURS.get(0))

    def ajouter_tuile(self):
        """
        Ajoute une tuile (2 ou 4) aléatoirement dans une case vide
        @param self: instance du jeu avec la grille à modifier
        @return: rien à retourner
        """
        vides = []
        for i in range(4):
            for j in range(4):
                if self.grille[i][j] == 0:
                    vides.append((i, j))
        if len(vides) > 0:
            i, j = random.choice(vides)
            proba = random.random()
            #Il y a 10% de chance chance d'obtenir un 4, sinon c'est un 2
            if proba < 0.1:
                self.grille[i][j] = 4
            else:
                self.grille[i][j] = 2

    def clavier(self, event):
        """
        Gère les déplacements de tuiles en fonction des touches clavier.
        @param event: événement clavier contenant la touche pressée
        @return: on ne retourne rien
        """
        touches = {"Up": "haut", "Down": "bas", "Left": "gauche", "Right": "droite"}
        if event.keysym in touches:
            direction = touches[event.keysym]
            nouvelle, bouge, gagne = self.deplacer(direction)
            if bouge:
                self.grille = nouvelle
                self.score = self.score + gagne
                self.score_label.config(text="Score : " + str(self.score))
                #On met à jour le meilleur score
                if self.score > self.highscore:
                    self.highscore = self.score
                    self.highscore_label.config(text="Meilleur : " + str(self.highscore))
                    self.sauvegarder_highscore()

                self.ajouter_tuile()
                self.afficher()
                #Ce bloc vérifie si le joueur a gagné. Donc qu'un 2048 a été atteint
                for ligne in self.grille:
                    for nombre in ligne:
                        if nombre == 2048:
                            messagebox.showinfo("Gagné !", "Vous avez atteint 2048 !")
                            return
                #Ici, on vérifie si la partie est perdu 
                if self.mouvements_possibles() == False:
                    messagebox.showinfo("Perdu", "Plus aucun mouvement possible.")

    def fusionner_ligne(self, ligne):
        """
        Fusionne les tuiles identiques d'une ligne vers la gauche, en respectant les règles du 2048
        @param ligne: list[int] c'est à dire une liste de 4 entiers représentant une ligne du plateau de jeu
        @return tuple : une nouvelle ligne (list[int]) après fusion et le score gagné (int)
        """
        nouvelle = []
        #On supprime les zéros
        for x in ligne:
            if x != 0:
                nouvelle.append(x)
        score = 0
        i = 0
        while i < len(nouvelle)-1:
            if nouvelle[i] == nouvelle[i+1]:
                nouvelle[i] = nouvelle[i] * 2
                score = score + nouvelle[i]
                nouvelle[i+1] = 0
                i = i + 2
            else:
                i = i + 1
        ligne2 = []
        #Ici, on supprime les zéros créés par fusion
        for x in nouvelle:
            if x != 0:
                ligne2.append(x)
        while len(ligne2) < 4:
            ligne2.append(0)
        return ligne2, score

    def deplacer(self, direction):
        """
        Déplace toutes les tuiles de la grille dans une direction donnée et effectue les fusions
        @param direction: a direction du mouvement ('gauche', 'droite', 'haut', 'bas')
        @return tuple: une nouvelle grille (list[list[int]]), un booléen indiquant s’il y a eu un mouvement,et le score total gagné avec ce déplacement
        """
        bouge = False
        score_total = 0
        nouvelle = [[0]*4 for x in range(4)]

        for i in range(4):
            if direction == "gauche":
                ligne = self.grille[i]
                ligne2, sc = self.fusionner_ligne(ligne)
                nouvelle[i] = ligne2
                if ligne2 != ligne:
                    bouge = True
                score_total = score_total + sc

            elif direction == "droite":
                #Ici on utlise [::-1] pour inverser la ligne sans modifier la grille originale
                #Cela crée une copie inversée, contrairement au .reverse() qui modifierai la liste en place
                #En fait ça pourrait causer des problèmes si aucun mouvement n'est validé par la suite
                ligne = self.grille[i][::-1]
                ligne2, sc = self.fusionner_ligne(ligne)
                ligne2 = ligne2[::-1]   #Là on réinverse pour remettre dans l'ordre exact
                nouvelle[i] = ligne2
                if ligne2 != self.grille[i]:
                    bouge = True
                score_total = score_total + sc

            elif direction == "haut":
                colonne = []
                for j in range(4):
                    colonne.append(self.grille[j][i])
                colonne2, sc = self.fusionner_ligne(colonne)
                for j in range(4):
                    nouvelle[j][i] = colonne2[j]
                    if colonne2[j] != self.grille[j][i]:
                        bouge = True
                score_total = score_total + sc

            elif direction == "bas":
                colonne = []
                for j in range(4):
                    colonne.append(self.grille[j][i])
                colonne = colonne[::-1]
                colonne2, sc = self.fusionner_ligne(colonne)
                colonne2 = colonne2[::-1]
                for j in range(4):
                    nouvelle[j][i] = colonne2[j]
                    if colonne2[j] != self.grille[j][i]:
                        bouge = True
                score_total = score_total + sc

        return nouvelle, bouge, score_total

    def mouvements_possibles(self):
        """
        Vérifie s'il reste au moins un déplacement possible sur la grille
        @return booléen : True s'il est possible de faire un mouvement, False sinon
        """
        directions = ['gauche', 'droite', 'haut', 'bas']
        for d in directions:
            nouvelle, bouge, _ = self.deplacer(d)
            if bouge == True:
                return True
        return False

#On crée de la fenêtre principale avec tkinter
root = tk.Tk()
#Cela crée le jeu dans la fenêtre principale et prépare toute l'interface du jeu
jeu = Jeu2048(root)
#Démarre la boucle principale de l'interface graphique, qui attend les événements utilisateur, c'est à dire toutes les actions possibles
root.mainloop()

