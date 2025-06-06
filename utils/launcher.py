# utils/launcher.py
import importlib

def lancer_jeu(module_path):
    try:
        jeu_module = importlib.import_module(module_path)
    except ImportError as e:
        print(f"Erreur lors du chargement du jeu : {e}")
