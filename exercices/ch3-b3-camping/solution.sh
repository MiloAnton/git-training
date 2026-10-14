printf "Emplacement 1 : ombrage\nEmplacement 2 : plein soleil\n" > carte.txt
printf "penser a racheter des piquets\n" > notes-perso.txt
git stash -u
git switch main
printf "Silence a partir de 22h\n" > reglement.txt
git add reglement.txt
git commit -m "feat(reglement): horaires de silence"
git switch feature/emplacements
git stash pop
git add carte.txt
git commit -m "feat(carte): ajout du second emplacement"
git status
