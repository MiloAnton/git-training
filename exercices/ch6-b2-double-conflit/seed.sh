git init saison
cd saison
printf "Entree : 5 euros\n" > tarifs.txt
printf "Ouverture : 10h\n" > horaires.txt
git add .
git commit -m "feat(saison): tarifs et horaires"
git switch -c feature/saison
printf "Entree : 7 euros\n" > tarifs.txt
printf "Ouverture : 9h\n" > horaires.txt
git commit -am "feat(saison): nouvelle saison"
git switch main
printf "Entree : 6 euros\n" > tarifs.txt
printf "Ouverture : 11h\n" > horaires.txt
git commit -am "feat(saison): ajustement de la saison"
