git switch -c feature/visites
printf "Visite 1 : la basse-cour\n" > visites.txt
git add visites.txt
git commit -m "feat(visites): visite de la basse-cour"
printf "Visite 1 : la basse-cour\nVisite 2 : la bergerie\n" > visites.txt
git commit -am "feat(visites): visite de la bergerie"
git switch main
git switch -c brouillon-ateliers
printf "Atelier pain\n" > ateliers.txt
git add ateliers.txt
git commit -m "feat(ateliers): atelier pain"
git branch -m feature/ateliers
git switch main
printf "Ferme ouverte du mardi au dimanche\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): jours d'ouverture"
git switch feature/visites
printf "Visite 1 : la basse-cour\nVisite 2 : la bergerie\nVisite 3 : le potager\n" > visites.txt
git stash
git switch main
git switch feature/visites
git stash pop
git commit -am "feat(visites): visite du potager"
git branch -v
git log --oneline --all
