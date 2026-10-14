git init tarte
cd tarte
printf "Pate brisee\nPommes\nCuisson : a definir\nServir tiede\n" > tarte.txt
git add tarte.txt
git commit -m "feat(tarte): recette de base"
git switch -c feature/cuisson
printf "Pate brisee\nPommes\nCuisson : 35 min a 180 degres\nServir tiede\n" > tarte.txt
git commit -am "feat(tarte): cuisson 35 min"
git switch main
printf "Pate brisee\nPommes golden\nCuisson : 45 min a 170 degres\nServir tiede\n" > tarte.txt
git commit -am "feat(tarte): pommes golden et cuisson 45 min"
