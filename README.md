# image-converter

Convertit les images d’un dossier en PNG, JPEG ou WebP, avec largeur maximale facultative. La transparence devient blanche en JPEG.

Python 3.10 ou plus récent.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Exemple

```bash
python main.py ~/Images ~/Images-converties --format webp --max-width 1200
python main.py ~/Images ~/Images-converties --format webp --max-width 1200 --apply
```

Sans `--apply`, la commande affiche seulement ce qu’elle ferait. Essaie-la sur un petit dossier de test avant de l’utiliser sur tes fichiers.

Le script ignore les liens symboliques. Il traite les fichiers à la racine du dossier, sauf le détecteur de doublons et la sauvegarde qui parcourent les sous-dossiers.
