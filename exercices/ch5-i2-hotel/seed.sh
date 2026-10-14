git init hotel
cd hotel
printf "Hotel du Lac\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): l'hotel"
printf "Navette gare : 8h et 18h\n" > navette.txt
git add navette.txt
git commit -m "feat(services): navette et petit dejeuner"
printf "Petit dejeuner : 7h-10h\n" > petit-dejeuner.txt
