git switch -c feature/nouveau-morceau
git branch
printf "Marche de la Saint-Jean\nValse du 14 juillet\nSamba de la kermesse\n" > repertoire.txt
git commit -am "feat(repertoire): ajout de la samba"
git switch main
cat repertoire.txt
