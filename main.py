# main.py
import tkinter as tk
from utils.launcher import lancer_jeu

# Dictionnaire des jeux
jeux_disponibles = {
    "Ultimate Morpion": "jeux.UltimateMorpion.main",
    "2048": "jeux.2048.main"
}

def creer_interface():
    root = tk.Tk()
    root.title("Plateforme de Jeux")
    root.geometry("300x200")

    label = tk.Label(root, text="Choisis un jeu :", font=("Arial", 14))
    label.pack(pady=10)

    for nom_jeu, module_path in jeux_disponibles.items():
        bouton = tk.Button(
            root, 
            text=nom_jeu, 
            font=("Arial", 12), 
            width=20, 
            command=lambda path=module_path: lancer_jeu(path)
        )
        bouton.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    creer_interface()
