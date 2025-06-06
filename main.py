# main.py
import sys
from utils.launcher import lancer_jeu

jeux_disponibles = {
    "1": ("Ultimate Morpion", "jeux.UltimateMorpion.main")
}

def menu():
    print("=== Menu des jeux ===")
    for key, (nom, _) in jeux_disponibles.items():
        print(f"{key}. {nom}")
    
    choix = input("Choisis un jeu : ")
    if choix in jeux_disponibles:
        _, module_path = jeux_disponibles[choix]
        lancer_jeu(module_path)
    else:
        print("Choix invalide.")
        sys.exit()

if __name__ == "__main__":
    menu()
