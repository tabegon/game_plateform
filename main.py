# main.py
import tkinter as tk
from utils.launcher import lancer_jeu
from PIL import Image, ImageTk
import os

jeux_disponibles = {
    "Morpion": {"module": "jeux.Morpion.main", "image": "C:/Users/Théo/Documents/Workspace/plateform/game_plateform/assets/morpion.png"},
    "Ultimate Morpion": {"module": "jeux.UltimateMorpion.main", "image": "C:/Users/Théo/Documents/Workspace/plateform/game_plateform/assets/ultimate.png"},
    "2048": {"module": "jeux.2048.main", "image": "C:/Users/Théo/Documents/Workspace/plateform/game_plateform/assets/2048.png"},
    "Snake": {"module": "jeux.Snake.main", "image": "C:/Users/Théo/Documents/Workspace/plateform/game_plateform/assets/snake.png"},
}

images = {}

def creer_interface():
    root = tk.Tk()
    root.title("Plateforme de Jeux")
    root.geometry("1900x850")

    label = tk.Label(root, text="Choisis un jeu :", font=("Arial", 14))
    label.pack(pady=10)

    for nom_jeu, info in jeux_disponibles.items():
        chemin_image = info["image"]
        img = Image.open(chemin_image).resize((100, 100))
        img_tk = ImageTk.PhotoImage(img)
        images[nom_jeu] = img_tk
        bouton = tk.Button(
            root,
            text= f" {nom_jeu}",
            image=img_tk,
            compound="left",
            font=("Arial", 24),
            width=500,
            anchor="w",
            command=lambda path=info["module"]: lancer_jeu(path)
        )

        bouton.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    creer_interface()
