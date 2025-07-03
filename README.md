# JupyterCards Definition Extractor

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/) 
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A lightweight Python library that **scans Markdown (.md) and JSON course files, automatically extracts definitions, and converts them into reusable flashcards compatible with [JupyterCards](https://github.com/Ismaelwn/jupytercards)**.

> **Context** – The project was developed during a research internship to streamline the creation of interactive teaching material. By automating the extraction of key concepts, instructors can focus on pedagogy while learners benefit from ready‑to‑use flashcards inside notebooks and Jupyter Book.

---

## Key Features

| Feature                         | Description                                                                                      |
| ------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Automatic definition mining** | Detects definition blocks in Markdown headers or specially‑tagged JSON structures.               |
| **One‑command conversion**      | CLI and Python API turn raw course content into the JSON schema expected by *JupyterCards*.      |
| **Randomised shuffling**        | Optional random order generation to maximise recall practice.                                    |
| **Topic filtering**             | Tag cards by topic to assemble custom decks on demand.                                           |
| **Jupyter‑native**              | Results can be displayed instantly in notebooks with `display_flashcards()` from *JupyterCards*. |
| **Fully open‑source**           | MIT‑licensed and extensible – fork it, adapt it, contribute!                                     |

---

## Quick Start

### 1 · Install

```bash
# Install extraction tools (this repo)
pip install git+https://github.com/Ismaelwn/exploration_jupytercards.git

# Install the flashcard renderer
pip install git+https://github.com/Ismaelwn/jupytercards.git
```

> **Prerequisites** • Python ≥ 3.11 • `pip` ≥ 24.0.1

### 2 · Prepare your courses

1. Put your `.md` and/or `.json` course files into a folder, e.g. `my_course/`.
2. Make sure definition blocks follow one of the supported patterns (see examples below).

### 3 · Generate flashcards (an example)

```bash
import subprocess
import sys
import os
from exploration_jupytercards import tools, preprocess   # ton package installé via pip
import exploration_jupytercards

current_dir = os.getcwd()
nextpart_dir = os.path.join(os.getcwd(),"_build", "content")

if len(sys.argv) > 1:
    content_dir = sys.argv[1]
else:
    raise FileNotFoundError(
        "Le répertoire de contenu n'est pas spécifié. "
        "Veuillez fournir un argument avec le chemin du dossier."
    )

# 0. Pré-traitement des .md et déplacement des fichiers temporaires
print("Pré-traitement des fichiers Markdown")
preprocess.pre_build(current_dir, content_dir)
preprocess.moove_files_JSON(content_dir, os.path.join(current_dir, "_build", "content"))
print("\n"+"Fin du Pré-traitement des fichiers Markdown")

print("\n"+"\n"+f"Début de l'Extraction des définitions dans : {content_dir}")
tools.extract_tools(current_dir)
print("\n"+f"Fin de l'Extraction des définitions dans : {content_dir}")
print("\n")
js_path = os.path.join(
    os.path.dirname(exploration_jupytercards.__file__),
    "AstToHTML.js"
)
print("\n"+"\n"+"Début de la Conversion HTML via JS…")
try:
    result2 = subprocess.run(
        ["node", js_path],
        capture_output=True, text=True, check=True, encoding='utf-8', errors='replace'
    )
    print(f"Sortie index.js :\n{result2.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Erreur dans index.js :\n{e.stderr}")
    sys.exit(2)
print("\n"+"Fin de la Conversion HTML via JS…")
print("\n")

print("\n"+"\n"+"Début de la Création du dictionnaire final ")
tools.toDict_tools(current_dir)
print("\n"+"Fin de la Création du dictionnaire final ")

```

### 4 · Visualise in a notebook

```python
from jupytercards import display_flashcards

display_flashcards("flashcards/my_course.json")
```

---

## Example Notebook

A fully‑worked, step‑by‑step demonstration is available in the companion repo **[Test\_creations\_cartes](https://github.com/Ismaelwn/Test_creations_cartes)**. Launch the `example.ipynb` notebook to see the extractor, the generated JSON, and the interactive cards side by side.

---

## How It Works

1. **Parsing** – The library walks through each input file, looking for:

   * Markdown headings starting with `# Definition` (configurable)
   * JSON objects containing `{ "term": …, "definition": … }`
2. **Cleaning** – HTML tags, LaTeX delimiters, and extra whitespace are stripped or escaped.
3. **Packing** – Cards are written to a single JSON array with the keys `front`, `back`, and optional `topic` (exactly what *JupyterCards* expects).
4. **Output** – Files are placed in `flashcards/` (or a directory of your choice).

---



## Contributing

Contributions are welcome! To submit a pull request:

1. Fork the repository and create your branch: `git checkout -b feature/my-feature`.
2. Run `pytest` and make sure all tests pass.
3. Commit your changes and open a PR – please describe the motivation and provide examples.

If you spot a bug or have a feature request, feel free to [open an issue](https://github.com/Ismaelwn/exploration_jupytercards/issues).

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

* **[JupyterCards](https://github.com/Ismaelwn/jupytercards)** for the flashcard rendering engine.
* The Jupyter community for inspiring interactive pedagogy.



