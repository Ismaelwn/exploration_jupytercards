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

function isList(obj) {
    return Array.isArray(obj);
}

async function convertMySTAstToHTML(jsonFile, outputFile) {
    try {
            // Lire le fichier JSON
            const jsonData = await fs.readFile(jsonFile, 'utf8')
            const ast = JSON.parse(jsonData) // Parser l'AST
    
            // Convertir l'AST MyST en HTML avec hiérarchie et styles
            const htmlContent = convertNodeToHtml(ast)
    
            // Ajouter une structure HTML de base
            const fullHtml = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyST AST to HTML</title>
    <style>
        /* === CSS pour les admonitions === */
        .admonition { border-left: 5px solid #4a90e2; padding: 10px 15px; margin: 15px 0; border-radius: 8px; background: #f3f6fa; position: relative; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); }
        .admonition-title { font-weight: bold; font-size: 1.1em; margin-bottom: 8px; display: flex; align-items: center; }
        .admonition-title::before { content: "ℹ️"; font-size: 1.2em; margin-right: 8px; }
        .admonition[data-type="warning"] { border-left-color: #e67e22; background: #fdf6e3; }
        .admonition[data-type="warning"] .admonition-title::before { content: "⚠️"; }
        .admonition[data-type="tip"] { border-left-color: #27ae60; background: #e8f5e9; }
        .admonition[data-type="tip"] .admonition-title::before { content: "💡"; }
        .admonition[data-type="error"] { border-left-color: #c0392b; background: #fdecea; }
        .admonition[data-type="error"] .admonition-title::before { content: "❌"; }
        /* === Grille et cartes === */
        .grid { display: flex; gap: 10px; }
        .card { border: 1px solid #ddd; padding: 10px; flex: 1; border-radius: 8px; background: #fff; }
        pre { background: #eee; padding: 10px; border-radius: 5px; }
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




// Chemin du dossier à lister
const dossierCible = join(process.cwd(), 'JSON');
const dossierSortie = join(process.cwd(), 'HTML');

try {
    // Lire les fichiers du dossier
    const fichiers = await readdir(dossierCible);
    
    console.log("Fichiers récupérés :", fichiers);

    
    
    for (let i = 0; i < fichiers.length; i++) {
        if (fichiers[i].endsWith('.json')) {
            console.log(`- ${fichiers[i]}`);
            const cheminJson = join(dossierCible, fichiers[i]);
            const cheminHtml = join(dossierSortie, `${fichiers[i]}.html`);

            // Lancer la conversion
            convertMySTAstToHTML(cheminJson, cheminHtml); 
        }
    }

} catch (err) {
    console.error("Erreur :", err);
}
