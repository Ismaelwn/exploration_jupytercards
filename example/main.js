import { exec } from 'child_process';

console.log("Exécution du script Python...");
exec("python index.py", (error, stdout, stderr) => {
    if (error) {
        console.error(`Erreur : ${error.message}`);
        return;
    }
    console.log(`Sortie Python :\n${stdout}`);

    console.log("Exécution du script JavaScript...");
    exec("node index.js", (error, stdout, stderr) => {
        if (error) {
            console.error(`Erreur : ${error.message}`);
            return;
        }
        console.log(`Sortie JavaScript :\n${stdout}`);
    });
});

