git init cave
cd cave
printf "Bordeaux 2018 : 24 bouteilles\n" > cave.txt
git add cave.txt
git commit -m "feat(cave): stock initial"
printf "Bordeaux 2018 : 24 bouteilles\nBordeaux 2018 : 2400 bouteilles\n" > cave.txt
git commit -am "feat(cave): erreur de saisie"
