#!/usr/bin/env python3
import os
import subprocess
import shutil
from shutil import copy2


def moove_files(SRC, DIR, out=False):
    """
    Copie tous les fichiers NON récursifs contenus dans SRC.
      - out == False → DIR/_build/content/<nom>
      - out == True  → DIR/<nom>
    """
    SRC = os.path.abspath(SRC)
    if not os.path.isdir(SRC):
        raise FileNotFoundError(f"Dossier source introuvable : {SRC}")

    # destination de base
    dest_base = (
        os.path.join(DIR, "_build", "content")
        if not out
        else DIR
    )
    os.makedirs(dest_base, exist_ok=True)

    for name in os.listdir(SRC):
        src_path = os.path.join(SRC, name)

        # ignorer les sous-dossiers
        if not os.path.isfile(src_path):
            continue

        dst_path = os.path.join(dest_base, name)
        copy2(src_path, dst_path)

def moove_files_JSON(SRC, DIR):
    """
    Déplace tous les fichiers *.json* (premier niveau uniquement) de SRC vers DIR.

    Parameters
    ----------
    SRC : str | os.PathLike
        Dossier où se trouvent les JSON à déplacer.
    DIR : str | os.PathLike
        Dossier de destination (créé si besoin).

    Raises
    ------
    FileNotFoundError
        Si le dossier source n'existe pas.
    """
    SRC = os.path.abspath(SRC)
    if not os.path.isdir(SRC):
        raise FileNotFoundError(f"Dossier source introuvable : {SRC}")

    DIR = os.path.abspath(DIR)
    os.makedirs(DIR, exist_ok=True)

    for name in os.listdir(SRC):
        if not name.lower().endswith(".json"):
            continue                      # on ne touche qu'aux .json

        src_path = os.path.join(SRC, name)
        if not os.path.isfile(src_path):
            continue                      # ignore les sous-dossiers

        dst_path = os.path.join(DIR, name)
        shutil.move(src_path, dst_path) 


def pre_build(current_dir, content_dir):
    """
    Copie myst.yml dans content_dir, lance 'myst build',
    déplace les fichiers générés et nettoie.
    """
    if not os.path.isdir(content_dir):
        os.makedirs(content_dir, exist_ok=True)

    copy2(
        os.path.join(current_dir, "myst.yml"),
        os.path.join(content_dir, "myst.yml"),
    )

    try:
        os.chdir(content_dir)
        result = subprocess.run(["myst", "build"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        

        # Dossier construit par myst :
        build_content = os.path.join(content_dir, "_build", "site", "content")
        if os.path.isdir(build_content):
            # on déplace vers <racine>/_build/content
            moove_files(build_content, os.path.join(current_dir, "_build", "content"), out=True)
        else:
            print(f"Avertissement : {build_content} introuvable ; aucun fichier déplacé.")

        # Nettoyage local (_build et copie myst.yml)
        shutil.rmtree("_build", ignore_errors=True)
        try:
            os.remove("myst.yml")
        except FileNotFoundError:
            pass

    finally:
        os.chdir(current_dir)
