import fs from 'node:fs/promises'
import { readdir } from 'fs/promises';
import { join } from 'path';

/**
 * Convertit un AST MyST en HTML en prenant en compte le style et la hiérarchie.
 * @param {Object} node - Un nœud de l'AST.
 * @param {number} depth - Niveau de profondeur pour structurer l'affichage.
 * @returns {string} - HTML généré.
 */
function convertNodeToHtml(node, depth = 0) {
    if (!node) return ""

    const indent = " ".repeat(depth * 4) // Indentation pour la hiérarchie
    const position = node.position ? ` data-line="${node.position.start.line}" data-column="${node.position.start.column}"` : ""

    switch (node.type) {
        case "admonition": {
            const type = node.kind || "note" // Type par défaut "note"
            return `${indent}<div class="admonition" data-type="${type}"${position}>\n${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("\n")}\n${indent}</div>`
        }

        case "admonitionTitle":
            return `${indent}<p class="admonition-title"${position}>${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("")}</p>`

        case "text":
            return `${indent}${node.value}`

        case "grid":
            return `${indent}<div class="grid"${position}>\n${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("\n")}\n${indent}</div>`

        case "card":
            return `${indent}<div class="card"${position}>\n${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("\n")}\n${indent}</div>`

        case "code":
            return `${indent}<pre><code${position}>${node.value}</code></pre>`

        case "image":
            return `${indent}<img src="${node.url}" alt="Image"${position} style="height:${node.height}; text-align:${node.align};">`

        default:
            return node.children ? node.children.map(child => convertNodeToHtml(child, depth)).join("\n") : ""
    }
}

async function convertMySTAstToHTML(jsonFile, outputFile) {
    try {
            // Lire le fichier JSON
            const jsonData = await fs.readFile(jsonFile, 'utf8')
            const ast = JSON.parse(jsonData) // Parser l'AST
    
            // Convertir l'AST MyST en HTML avec hiérarchie et styles
            const htmlContent = convertNodeToHtml(ast)
    
            // Ajouter une structure HTML de base et inclure le CSS MyST
            const fullHtml = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyST AST to HTML</title>
    <style>
    /* === CSS pour les admonitions === */
    .admonition {
        border-left: 4px solid #007ACC; /* Bordure bleue pour l'admonition */
        padding: 10px 16px;
        border-radius: 8px; /* Coins arrondis */
        background: #f0f8ff; /* Fond clair */
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1); /* Ombre légère */
        margin-bottom: 20px; /* Espacement en bas */
    }

    .admonition-title {
        font-weight: bold;
        font-size: 1.2em;
        color: #007ACC; /* Couleur du titre */
        margin-bottom: 12px;
    }

    /* === Bloc de code === */
    pre {
        background-color: #2d2d2d;  /* Fond sombre */
        color: #f5f5f5;             /* Texte clair */
        padding: 16px 20px;         /* Espacement autour du texte */
        border-radius: 8px;         /* Coins arrondis */
        font-size: 1em;             /* Taille de police confortable */
        font-family: "Courier New", monospace;  /* Police monospace */
        overflow-x: auto;           /* Barres de défilement horizontales */
        word-wrap: break-word;      /* Séparation des mots longs */
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);  /* Ombre légère */
    }

    /* Code en ligne */
    code {
        background-color: #2d2d2d;  /* Fond sombre pour le code en ligne */
        color: #f5f5f5;             /* Texte clair */
        padding: 4px 6px;           /* Espacement pour le code en ligne */
        border-radius: 4px;         /* Coins arrondis */
        font-size: 0.9em;           /* Taille de police plus petite */
        font-family: "Courier New", monospace;  /* Police monospace */
    }
    </style>
</head>
<body>
    ${htmlContent}
</body>
</html>`

        // Écrire le HTML dans le fichier de sortie
        await fs.writeFile(outputFile, fullHtml, 'utf8')
        console.log(`✅ Conversion terminée ! Fichier généré : ${outputFile}`)
    } catch (error) {
        console.error("❌ Erreur lors de la conversion :", error)
    }
}

// Exemple d'utilisation pour convertir un fichier AST en HTML
const dossierCible = join(process.cwd(), 'JSON');
const dossierSortie = join(process.cwd(), 'HTML');

try {
    const fichiers = await readdir(dossierCible);
    
    console.log("Fichiers récupérés :", fichiers);

    for (let i = 0; i < fichiers.length; i++) {
        if (fichiers[i].endsWith('.json')) {
            console.log(`- ${fichiers[i]}`);
            const cheminJson = join(dossierCible, fichiers[i]);
            const cheminHtml = join(dossierSortie, `${fichiers[i].replace(/\.json$/, '')}.html`);

            // Lancer la conversion
            convertMySTAstToHTML(cheminJson, cheminHtml); 
        }
    }

} catch (err) {
    console.error("Erreur :", err);
}
