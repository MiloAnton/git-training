1. Le réglage n'agit que sur les fichiers que Git ne suit pas encore. Celui-là, il le suit déjà.
2. Cherche la commande qui retire un fichier du dépôt sans le supprimer du disque. C'est une option de `git rm`.
3. Fais-le dans cet ordre : retirer du suivi, puis écrire le réglage, puis valider. Le `ls` final doit encore montrer le fichier.
