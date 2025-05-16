import fs from 'node:fs/promises';
import { readdir, readFile } from 'fs/promises';
import path, { join } from 'node:path';
import { existsSync, readFileSync } from 'fs';
import { createHash } from 'crypto';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Déterminer le dossier réel où se trouve ce script
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 🔧 Répertoires correctement relatifs au script
const dossierCible = join(__dirname, '../JSON');
const dossierSortie = join(__dirname, '../HTML');
const dossierCache = join(__dirname, '../JSON_old');

// 🔧 Création explicite des dossiers nécessaires
await fs.mkdir(dossierSortie, { recursive: true });
await fs.mkdir(dossierCache, { recursive: true });

function hash(content) {
    return createHash('sha256').update(content).digest('hex');
}

function fichierModifie(jsonPath, cachePath) {
    if (!existsSync(cachePath)) return true;
    const actuel = readFileSync(jsonPath, 'utf8');
    const ancien = readFileSync(cachePath, 'utf8');
    return hash(actuel) !== hash(ancien);
}

function convertNodeToHtml(node, depth = 0) {
    if (!node) return "";

    const indent = " ".repeat(depth * 4);
    const position = node.position
        ? ` data-line="${node.position.start.line}" data-column="${node.position.start.column}"`
        : "";

    switch (node.type) {
        case "admonition": {
            const type = node.kind || "note";
            return `${indent}<div class="admonition" data-type="${type}"${position}>\n${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("\n")}\n${indent}</div>`;
        }
        case "admonitionTitle":
            return `${indent}<p class="admonition-title"${position}>${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("")}</p>`;
        case "text":
            return `${indent}${node.value}`;
        case "grid":
            return `${indent}<div class="grid"${position}>\n${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("\n")}\n${indent}</div>`;
        case "card":
            return `${indent}<div class="card"${position}>\n${node.children.map(child => convertNodeToHtml(child, depth + 1)).join("\n")}\n${indent}</div>`;
        case "code":
            return `${indent}<pre><code${position}>${node.value}</code></pre>`;
        case "image":
            return `${indent}<img src="${node.url}" alt="Image"${position} style="height:${node.height}; text-align:${node.align};">`;
        default:
            return node.children
                ? node.children.map(child => convertNodeToHtml(child, depth)).join("\n")
                : "";
    }
}

async function convertMySTAstToHTML(jsonFile, outputFile) {
    try {
        const jsonData = await fs.readFile(jsonFile, 'utf8');
        const ast = JSON.parse(jsonData);
        const htmlContent = convertNodeToHtml(ast);
        const fullHtml = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyST AST to HTML</title>
    <style>
    .admonition {
        border-left: 4px solid #007ACC;
        padding: 10px 16px;
        border-radius: 8px;
        background: #f0f8ff;
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .admonition-title {
        font-weight: bold;
        font-size: 1.2em;
        color: #007ACC;
        margin-bottom: 12px;
    }
    pre {
        background-color: #2d2d2d;
        color: #f5f5f5;
        padding: 16px 20px;
        border-radius: 8px;
        font-size: 1em;
        font-family: "Courier New", monospace;
        overflow-x: auto;
        word-wrap: break-word;
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
    }
    code {
        background-color: #2d2d2d;
        color: #f5f5f5;
        padding: 4px 6px;
        border-radius: 4px;
        font-size: 0.9em;
        font-family: "Courier New", monospace;
    }
    </style>
</head>
<body>
    ${htmlContent}
</body>
</html>`;

        await fs.writeFile(outputFile, fullHtml, 'utf8');
        console.log(`[✅] Conversion terminée : ${outputFile}`);
    } catch (error) {
        console.error("[ERREUR] Conversion échouée :", error);
    }
}

// —————————————————————————————————————
// Boucle principale sur les fichiers JSON
// —————————————————————————————————————
try {
    const fichiers = await readdir(dossierCible);
    for (const fichier of fichiers) {
        if (fichier.endsWith('.json')) {
            const cheminJson = join(dossierCible, fichier);
            const cheminHtml = join(dossierSortie, fichier.replace(/\.json$/, '.html'));
            const cheminCache = join(dossierCache, fichier);

            if (fichierModifie(cheminJson, cheminCache)) {
                console.log(`[→] Génération HTML : ${fichier}`);
                await convertMySTAstToHTML(cheminJson, cheminHtml);
            } else {
                console.log(`[⏩] HTML inchangé : ${fichier}`);
            }
        }
    }
} catch (err) {
    console.error("❌ Erreur lors de la lecture du dossier JSON :", err);
}
