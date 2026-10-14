git init jardinerie
cd jardinerie
printf "Jardinerie des Quatre Saisons\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la jardinerie"
git switch -c feature/arrosage
printf "Arrosage automatique : 6h et 20h\n" > arrosage.txt
git add arrosage.txt
git commit -m "feat(arrosage): horaires d'arrosage"
git switch main
