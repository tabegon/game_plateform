# Créé par Louise, le 14/05/2025 en Python 3.7

import os

# Change le dossier de travail au dossier du script
os.chdir(os.path.dirname(__file__))


import pygame   # on importe pygame
import sys
import os
from random import randint

## on définit les carreaux
tiles_x = 33    # on définit le nombre de carreaux sur la grille sur la longueur
tiles_y = 21    # on définit le nombre de carreaux sur la grille sur la hauteur


## on définit la fenêtre
h = 777         # on choisit la hauteur de la fenêtre
l = 1221        # on choisit la largeur de la fenêtre



x = 180         # coordonnées pour la position de la fenêtre
y = 80
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
                # ici, on les applique


pygame.init()
# on ajoute cette fonction pour être sûre que cela marche sur toutes les machines
pygame.mixer.init()  # sert à démarrer le système du son de pygame

## Fenêtre
fenetre = pygame.display.set_mode((l, h))
    # on applique les mesures par pygame définits précedemment
couleur = pygame.Color(22,41,85)    # on définit la couleur du plateau, bleu ici


## Carreaux
tile_l = l // tiles_x # on définit le largeur des carreaux sur la grille sur la longueur
tile_h = h // tiles_y # on définit le largeur des carreaux sur la grille sur la hauteur


## Sons
manger_son = pygame.mixer.Sound("miamm.wav")  # charge un fichier son (à avoir dans le même dossier)
son_piment = pygame.mixer.Sound("mario.wav")
son_glacon = pygame.mixer.Sound("wii.wav")



## Nourriture

types_possible = ["hotdog", "piment", "glacon"] # les différentes nourritures


images_nourriture = {                # on va définir les images de la nourriture
    "hotdog": pygame.transform.scale(
              # on modifie le format de l'image pour qu'elle convienne à la case
        pygame.image.load("hotdog.jpg").convert_alpha(),
                                        # on charge l'image avant de modifier...
        (tile_l * 2, tile_h * 2)                        # sa taille, définie ici
    ),
    "piment": pygame.transform.scale(
        pygame.image.load("piment.png").convert_alpha(),
        (int(tile_l * 1.5), int(tile_h * 1.5))
    ),
    "glacon": pygame.transform.scale(
        pygame.image.load("glacons.png").convert_alpha(),
        (int(tile_l * 1.5), int(tile_h * 1.5))
    )
}



## on définit les variables du jeu

snake_x, snake_y = tiles_x // 2, tiles_y // 2  # on définit la position de départ
                                            # ici on le fait commencer au milieu

snake = [                           # on définit le snake complet
    [snake_x, snake_y],             # c'est-à-dire sur les coordonnées des cases
    [snake_x-1, snake_y],           # sur lesquelles il va débuter
    [snake_x-2, snake_y]
]


nourriture = {
    "position": [tiles_x // 3, tiles_y // 4],
                            # on définit la position de départ de la nourriture
    "type": "hotdog"        # qui sera un hotdog au départ
}


effet_en_cours = None         # effet glaçons, piment ou rien
effet_debut = 0               # temps de début de l'effet
effet_duree = 3000            # durée des effets en millisecondes, ici 3 secondes



vitesse = 10                  # on règle la vitesse initiale

pause = False                 # tant que p n'est pas pressé, le jeu tourne

niveau = 0                    # on définit le niveau de départ


couleurs_niveaux = [             # on définit la couleur des différents niveaux
    pygame.Color(148, 31, 198),  # violet
    pygame.Color(60, 215, 60),   # Vert
    pygame.Color(0, 200, 255),   # Bleu
    pygame.Color(255, 165, 0),   # Orange
    pygame.Color(255, 0, 255),   # Magenta
    pygame.Color(255, 100, 100), # Pêche
    pygame.Color(255, 255, 0),   # Jaune
    pygame.Color(255, 0, 0)      # Rouge
]


direction = [1, 0]
# on définit la direction de départ du snake, là il commence par aller vers la droite
clock = pygame.time.Clock()
# Clock permet de gérer la vitesse de la boucle principale dans un jeu Pygame


## Fonctions


def drawnourriture():
    pos_x = nourriture["position"][0] * tile_l + tile_l // 2
    pos_y = nourriture["position"][1] * tile_h + tile_h // 2
    # calcule la position du centre de la case où se trouve la nourriture pour
    # les coordonnées x et y
    type_n = nourriture["type"]
    # ici, on définit type_n aléatoirement le type de nourriture
    rect = images_nourriture[type_n].get_rect(center=(pos_x, pos_y))
    # on définit de manière aléatoire le carreau sur lequel la nourriture apparaîtra
    fenetre.blit(images_nourriture[type_n], rect)
    # affiche l'image de la nourriture à la position définie précédemment



def drawsnake():
    if effet_en_cours == "glacon":
    # si l'effet en cours est "glacon"
        snake_couleur = pygame.Color(255, 255, 255)
        # on met le serpent en blanc
    elif effet_en_cours == "piment":
    # si l'effet en cours est "piment"
        snake_couleur = pygame.Color(0, 0, 0)
        # on met le serpent en noir
    else:
        snake_couleur = couleurs_niveaux[niveau % len(couleurs_niveaux)]
        # sinon on met le serpent de la couleur associée au niveau actuel

    for cell in snake:              # ici, on parcourt chaque case du serpent
        cell_rect = pygame.Rect((cell[0]*tile_l, cell[1]*tile_h), (tile_l, tile_h))
        # on crée un rectangle qui est une case du serpent à sa position définie précedemment
        pygame.draw.rect(fenetre, snake_couleur, cell_rect)
        # on peint donc ces cases avec la couleur du serpent actuel


def toucher_bord(tete) :
# ici, on ne veut pas que le serpent touche le bord, sinon il perd
    x_tete, y_tete = tete[0], tete[1]
    # on prend les coordonnées de la tête du serpent
    if x_tete >= tiles_x or x_tete < 0:
    # si la tête dépasse de la limite droite ou gauche de la fenêtre
        return False
        # alors on renvoit faux -> on a perdu !
    if y_tete >= tiles_y or y_tete < 0:
        # si la tête dépasse de la limite du haut ou du bas de la fenêtre
        return False
        # alors on renvoit faux -> on a perdu !
    return True




def updateSnake(direction) :
    # on lui indique que l'on utilise la nourriture définie en dehors de la fonction
    # idem pour les 3 autres
    global nourriture
    global niveau
    global effet_en_cours, effet_debut


    dirX, dirY = direction  # on récupère la direction en abscisse et en ordonnée
    tete = snake[0].copy()  # on définit alors la tête du snake -> le 1er élément de la cellule
                            # et on la copie car on veut créer une nouvelle tête
    tete[0] = (tete[0] + dirX)  # on déplace notre tête et on prend son abscisse tête
                                        # puis on lui ajoute la direction en abscisse
    tete[1] = (tete[1] + dirY)


    if tete in snake[1:]:   # on teste si la tête est dans le snake (si elle se rentre dedans)
        return False        # dans ce cas, on a perdu
    if tete == nourriture["position"]:   # si la tête touche la nourriture
        type_n = nourriture["type"]
        # selon le type de nourriture, on applique l'effet voulu et la musique
        # correspondante
        if type_n == "hotdog":
            manger_son.play()
        elif type_n == "piment":      # s'il s'agit d'un piment
            son_piment.play()         # on lance la musique
            effet_en_cours = "piment" # ici, on applique l'effet piment définit auparavant
            effet_debut = pygame.time.get_ticks()  # et lui définit un temps
                                        #pour ne pas qu'elle tourne indéfinimment
        elif type_n == "glacon":
            son_glacon.play()
            effet_en_cours = "glacon"
            effet_debut = pygame.time.get_ticks()


        nourriture = None   # on supprime l'ancienne nourriture

        while nourriture is None:
            nouvelle_pos = [randint(0, tiles_x-1), randint(0, tiles_y-1)]
            # on génère, toujours de manière aléatoire, une nouvelle position
            # de la nourriture
            if nouvelle_pos not in snake: # dans qu'elle n'est pas dans le snake
                type_n = types_possible[randint(0, 2)]  #  nourriture aléatoire
                nourriture = {"position": nouvelle_pos, "type": type_n}


    else:
        snake.pop() # sinon, le serpent ne grandit pas

    snake.insert(0, tete) # on insert la tête au début

    if not toucher_bord(tete):
        return False  # Le snake a touché le bord → fin de partie

    score_actuel = len(snake) - 3  # mise à jour du score
    niveau = score_actuel // 3  # Un niveau tous les 3 points

    return True         # on renvoie vrai puisque le jeu continue




def accueil():              # on définit la page d'accueil
    font_titre = pygame.font.Font("snake.ttf", 96)
    # ici, on définit la police et la taille du titre
    texte_titre = font_titre.render("SNAKE GAME", True, (0, 255, 0))

    # on définit le titre et sa couleur
    texte_titre_rect = texte_titre.get_rect(center=(l // 2, h // 3))
    # ainsi que sa position

    font_instructions = pygame.font.Font("simpletix.otf", 36)
    # ici, on définit la police et la taille des instructions
    instructions = [
        "Utilise les fleches pour diriger le serpent",
        "Appuie sur P pour mettre en pause",
        "Appuie sur ECHAP pour quitter",
        "Appuie sur ESPACE pour commencer",
        "Le piment accelere le snake et les glacons le ralentit !"
    ]  # liste des instructions à afficher sur l'écran d'accueil




    fenetre.fill(couleur)   # on applique la couleur de fond définie à la fenêtre
    fenetre.blit(texte_titre, texte_titre_rect) # on affiche le titre dont les
                                            # coordonnées ont été définies précedemment

    for i, ligne in enumerate(instructions):
    # on affiche les instructions
        texte_ligne = font_instructions.render(ligne, True, (206, 229, 239))
        # on définit sa couleur
        texte_ligne_rect = texte_ligne.get_rect(center=(l // 2, h // 2 + i * 40))
        # on définit sa position
        fenetre.blit(texte_ligne, texte_ligne_rect)
        # et on les affiche

    pygame.display.update() # mise à jour de l'affichage


    attendre = True
    while attendre: # la boucle tourne en attendant que le joueur appuie sur espace
        for event in pygame.event.get():
        # ici, il parcourt tous les évènements pygame (clavier...)
            if event.type == pygame.QUIT: # si il clique sur la croix de la fenêtre
                pygame.quit() # on ferme pygame
                exit()         # et le programme
            if event.type == pygame.KEYDOWN: # si une touche est pressée
                if event.key == pygame.K_SPACE: # si c'est espace
                    attendre = False # on sort de la boucle d'attend et le jeu démarre
                elif event.key == pygame.K_ESCAPE: # et si c'est échap
                    pygame.quit() # alors on ferme pygame
                    sys.exit()  # et le programme



def game_over_screen(score):    # on définit l'écran de fin de jeu avec score et relance
    global pause                # on appelle pause qui est en dehors de la boucle
    ## Titre Game Over
    font = pygame.font.Font("double-feature-regular.ttf", 100)
    # on définit la police et sa taille
    texte = font.render("GAME OVER", True, (255,255,51))
    # on définit ce qu'elle dit et sa couleur
    texte_rect = texte.get_rect(center=(l // 2, h // 3))
    # et sa position


    ## Affichage score final
    font_score = pygame.font.Font("simpletix.otf", 48)
    texte_score = font_score.render(f"Score : {score}", True, (204, 153, 255))
    texte_score_rect = texte_score.get_rect(center=(l // 2, h // 2.5 + 60))

    ## Message de relance ou sortie
    font_continue = pygame.font.Font("simpletix.otf", 36)
    texte_continue = font_continue.render("Appuie sur ESPACE pour rejouer ou ECHAP pour quitter", True, (203, 206, 206))
    texte_continue_rect = texte_continue.get_rect(center=(l // 2, h // 2 + 120))

    ## Affiche sur la fenêtre de fin de jeu
    fenetre.fill(couleur)                           # on met la couleur de fond
    fenetre.blit(texte, texte_rect)                 # on affiche game over,
    fenetre.blit(texte_score, texte_score_rect)     # le score
    fenetre.blit(texte_continue, texte_continue_rect) # et les instructions
    pygame.display.update()                         # puis on met à jour la fenêtre
    

    # boucle d'attente pour savoir si le joueur relance ou quitte le jeu
    waiting = True
    while waiting:
        for event in pygame.event.get():  # on récupère les évènements pygame
            if event.type == pygame.QUIT: # si le joueur ferme la fenêtre
                return False              # on quitte le jeu
            if event.type == pygame.KEYDOWN:        # si une touche est pressée
                if event.key == pygame.K_ESCAPE:    # si c'est échap
                    return False                    # on quitte
                if event.key == pygame.K_p:         # si c'est p
                    pause = not pause               # on met en pause ou relance
                elif event.key == pygame.K_SPACE:   # si c'est espace
                    return True                     # on rejoue


def main():
    global effet_en_cours, pause, direction
    ## Programme principal

    accueil()       # on affiche les instructions sur la page d'accueil

    duree_effet = 3000  # Durée de l'effet en millisecondes (ici : 3 secondes)
    running = True             # on commence le programme en jouant

    while running:
        temps_actuel = pygame.time.get_ticks()   # temps depuis le lancement du programme

        if effet_en_cours is not None and temps_actuel - effet_debut <= duree_effet:
        # si un effet est en cours et qu'il reste encore du temps
            if effet_en_cours == "piment":
                vitesse = 13 # vitesse de l'accélération du serpent
            elif effet_en_cours == "glacon":
                vitesse = 6 #  # vitesse de ralentissement du serpent
        else: # si l’effet est terminé, on le désactive et remet la vitesse normale
            if effet_en_cours == "piment":
                son_piment.stop()               # on arrête le son du piment
            elif effet_en_cours == "glacon":
                son_glacon.stop()               # on arrête le son du glaçon
            effet_en_cours = None               # on supprime l'effet en cours
            vitesse = 10                         # Vitesse normale

        clock.tick(vitesse)

        ## on définit les touches de claviers & leurs fonctions
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # si l'utilisateur  ferme la fenêtre
                pygame.quit()             # on quitte
                sys.exit()                # le programme
            if event.type == pygame.KEYDOWN: # si une touche est pressée
                if event.key == pygame.K_ESCAPE: # si c'est échap
                    running = False              # on quitte le programme
                elif event.key == pygame.K_p: # si p est pressée
                    pause = not pause       # active ou désactive la pause
                elif not pause:             # sinon le serpent change de direction
                    if event.key == pygame.K_RIGHT and direction != [-1, 0]:
                        direction = [1, 0]
                    # ici, la flèche droite est pressée donc il va à droite à condition
                    # qu'il ne soit pas parti à gauche (sinon collision)
                    elif event.key == pygame.K_LEFT and direction != [1, 0]:
                        direction = [-1, 0] # gauche
                    elif event.key == pygame.K_UP and direction != [0, 1]:
                        direction = [0, -1] # haut
                    elif event.key == pygame.K_DOWN and direction != [0, -1]:
                        direction = [0, 1] # bas
        if not pause: # si le jeu n'est pas en pause
            if updateSnake(direction) == False: # si le serpent meurt (collison ou bord)
                son_piment.stop()    # on arrête les sons
                son_glacon.stop()
                effet_en_cours = None # on arrête les effets
                score = len(snake) - 3 # on calcule le score
                rejouer = game_over_screen(score) # on affiche l'écran de fin avec score et relance
                if rejouer: # si le joueur veut rejouer
                    # Réinitialiser le jeu
                    snake.clear() # on réinitialise le serpent actuel
                    snake_x, snake_y = tiles_x // 2, tiles_y // 2 # remet dans sa position centrale
                    snake.extend([ # on en crée un nouveau
                        [snake_x, snake_y],
                        [snake_x-1, snake_y],
                        [snake_x-2, snake_y]
                    ])
                    nourriture["position"] = [tiles_x // 3, tiles_y // 4]
                    # on remet la nourriture à la position de départ
                    vitesse = 6 # on remet la vitesse de base
                    direction = [1, 0] # ainsi que sa direction
                else:
                    running = False # si on ne rejoue pas, on quitte le programme

            ## Partie affichage (quand pas en pause)
            fenetre.fill(couleur)
            drawnourriture()             # dessine la nourriture à l'écran
            drawsnake()                  # dessine le serpent à l’écran
            score = len(snake) - 3       # met à jour le score
            pygame.display.set_caption(f'Snake - Score: {score}') # met à jour le titre de la fenêtre
            pygame.display.update()      # mise à jour de l'affichage

        else:   # si le jeu est en pause
            # Afficher le texte pause
            fenetre.fill(couleur)  # Remplir l'écran pour éviter les traînées
            font_pause = pygame.font.Font("simpletix.otf", 48) # on définit la taille pour le message de pause
            text_pause = font_pause.render("PAUSE - Appuie sur P pour reprendre", # on définit le texte
            True, pygame.Color(255, 255, 255)) # on définit sa couleur
            text_pause_rect = text_pause.get_rect(center=(l // 2, h // 2)) # et sa position
            fenetre.blit(text_pause, text_pause_rect) # on affiche le texte
            pygame.display.update() # et on met à jour l'affichage

    pygame.quit()       # on quitte l'affichage !!!!
