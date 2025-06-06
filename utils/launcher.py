# utils/launcher.py
import importlib
import threading

def lancer_jeu(module_path):
    def lancer():
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, 'main'):
                module.main()
            else:
                print(f"Erreur : {module_path} n'a pas de fonction main().")
        except Exception as e:
            print(f"Erreur lors du lancement de {module_path} : {e}")

    # Lancer le jeu dans un thread séparé pour ne pas bloquer l'interface
    thread = threading.Thread(target=lancer)
    thread.start()
