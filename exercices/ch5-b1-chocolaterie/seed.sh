git init chocolaterie
cd chocolaterie
printf "Chocolaterie Les Trois Feves\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la chocolaterie"
printf "Praline : 40 pourcent cacao\n" > recettes.txt
git add recettes.txt
git commit -m "feat(recettes): la praline"
printf "Horaires : 7h-23h\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): horaires errones"
printf "Boites de 12\n" > conditionnement.txt
git add conditionnement.txt
git commit -m "feat(conditionnement): boites de 12"
printf "Praline : 40 pourcent cacao\nGanache : creme et chocolat\n" > recettes.txt
git commit -am "ganache"
printf "n importe quoi\n" > conditionnement.txt
