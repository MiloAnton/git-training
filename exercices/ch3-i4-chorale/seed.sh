git init chorale
cd chorale
printf "Ave Maria\n" > repertoire.txt
git add repertoire.txt
git commit -m "feat(repertoire): premier chant"
git switch -c feature/concert
printf "Salle des fetes, 20h\n" > concert.txt
git add concert.txt
git commit -m "feat(concert): lieu et horaire"
git switch main
git switch -c feature/costumes
printf "Tuniques bleues\n" > costumes.txt
git add costumes.txt
git commit -m "feat(costumes): choix des tuniques"
git switch main
printf "Ave Maria\nCantique de Jean Racine\n" > repertoire.txt
git commit -am "feat(repertoire): ajout du cantique"
