git init serveur
cd serveur
printf "Sauvegarde du serveur\nPassage a 02h00\nDestination : disque externe\n" > procedure.txt
git add procedure.txt
git commit -m "feat(procedure): premiere version"
