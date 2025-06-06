# utils/launcher.py
import importlib

def lancer_jeu(module_path):
    try:
        jeu_module = importlib.import_module(module_path)
        if hasattr(jeu_module, 'main'):
            jeu_module.main()
        else:
            print(f"Le jeu '{module_path}' n'a pas de fonction main().")
    except ImportError as e:
        print(f"Erreur lors du chargement du jeu : {e}")
