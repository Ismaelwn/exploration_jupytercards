import { exec } from 'child_process';
import path from 'path';

// 1ᵉʳ argument : chemin du dossier « content » ; défaut = "./content"
const contentDir = process.argv[2] ?? 'content';

console.log(`🧬  Extraction des définitions dans : ${contentDir}`);

// ————————————————————————————
// ÉTAPE 1 : index.py — extraction JSON → AST
// ————————————————————————————
exec(`python index.py "${contentDir}"`, (error, stdout, stderr) => {
  if (error) {
    console.error(`🚨  Erreur Python (index.py) : ${error.message}`);
    console.error(stderr);
    return;
  }
  console.log(`🧪  Sortie index.py :\n${stdout}`);

  console.log('🔬  Conversion HTML…');

  // ————————————————————————————
  // ÉTAPE 2 : index.js — AST → fichiers .html
  // ————————————————————————————
  exec('node index.js', (error2, stdout2, stderr2) => {
    if (error2) {
      console.error(`🚨  Erreur JavaScript (index.js) : ${error2.message}`);
      console.error(stderr2);
      return;
    }
    console.log(`🧪  Sortie index.js :\n${stdout2}`);

    console.log('🧬  Création du dictionnaire (index2.py)…');

    // ————————————————————————————
    // ÉTAPE 3 : index2.py — titre def + .html → dictionnaire JSON
    // ————————————————————————————
    exec('python index2.py', (error3, stdout3, stderr3) => {
      if (error3) {
        console.error(`🚨  Erreur Python (index2.py) : ${error3.message}`);
        console.error(stderr3);
        return;
      }
      console.log(`🧪  Sortie index2.py :\n${stdout3}`);
    });
  });
});
