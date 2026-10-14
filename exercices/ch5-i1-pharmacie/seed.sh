git init pharmacie
cd pharmacie
printf "Garde : nuit du lundi\n" > planning.txt
git add planning.txt
git commit -m "feat(planning): garde du lundi"
printf "Garde : nuit du lundi\nGarde : nuit du jeudi\n" > planning.txt
git commit -am "feat(planning): garde du jeudi"
printf "Garde : nuit du lundi\nGarde : nuit du jeudi\nGarde : week-end\n" > planning.txt
git commit -am "feat(planning): garde du week-end"
