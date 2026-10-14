git init poterie
cd poterie
printf "Atelier poterie du jeudi\n" > atelier.txt
git add atelier.txt
git commit -m "feat(atelier): presentation"
git switch -c feature/four
printf "Four : cuisson 1000 degres\n" > four.txt
git add four.txt
git commit -m "feat(four): fiche du four"
printf "Four : cuisson 1000 degres\nEmaillage : apres biscuitage\n" > four.txt
git commit -am "feat(four): procedure d'emaillage"
git switch main
