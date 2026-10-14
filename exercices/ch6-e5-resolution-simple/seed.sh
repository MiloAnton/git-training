git init couleurs
cd couleurs
printf "Couleur principale : a definir\n" > couleurs.txt
git add couleurs.txt
git commit -m "feat(couleurs): charte a definir"
git switch -c feature/charte
printf "Couleur principale : vert\n" > couleurs.txt
git commit -am "feat(couleurs): le vert"
git switch main
printf "Couleur principale : bleu\n" > couleurs.txt
git commit -am "feat(couleurs): le bleu"
git merge feature/charte
