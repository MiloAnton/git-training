git init regles
cd regles
printf "Nombre de joueurs : a definir\nDuree : 90 min\n" > regles.txt
git add regles.txt
git commit -m "feat(regles): premieres regles"
git switch -c feature/club
printf "Nombre de joueurs : 7\nDuree : 90 min\n" > regles.txt
git commit -am "feat(regles): sept joueurs"
git switch main
printf "Nombre de joueurs : 11\nDuree : 90 min\n" > regles.txt
git commit -am "feat(regles): onze joueurs"
git merge feature/club
