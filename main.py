# main.py
import tkinter as tk
from utils.launcher import lancer_jeu
from PIL import Image, ImageTk
import os

# Dictionnaire des jeux avec leurs modules et images
jeux_disponibles = {
    "Ultimate Morpion": {"module": "jeux.UltimateMorpion.main", "image": "C:/Users/Théo/Documents/Workspace/plateform/game_plateform/assets/ultimate.png"},
    "2048": {"module": "jeux.2048.main", "image": "C:/Users/Théo/Documents/Workspace/plateform/game_plateform/assets/2048.png"},
}

# Liste pour garder les références d'image
images = {}

def creer_interface():
    root = tk.Tk()
    root.title("Plateforme de Jeux")
    root.geometry("400x300")

    label = tk.Label(root, text="Choisis un jeu :", font=("Arial", 14))
    label.pack(pady=10)

    for nom_jeu, info in jeux_disponibles.items():
        chemin_image = info["image"]
        img = Image.open(chemin_image).resize((100, 100))
        img_tk = ImageTk.PhotoImage(img)
        images[nom_jeu] = img_tk  # Garder une référence pour éviter que l'image soit supprimée
        bouton = tk.Button(
            root,
            text=nom_jeu,
            image=img_tk,
            compound="left",  # image à gauche du texte
            font=("Arial", 24),
            width=500,
            anchor="w",  # aligner à gauche
            command=lambda path=info["module"]: lancer_jeu(path)
        )

        bouton.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    creer_interface()
