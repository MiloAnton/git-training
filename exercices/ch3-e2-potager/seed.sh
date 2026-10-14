git init potager
cd potager
printf "tomates\ncourgettes\n" > parcelles.txt
git add parcelles.txt
git commit -m "feat(parcelles): premieres parcelles"
git switch -c feature/serre
printf "serre 1 : semis\n" > serre.txt
git add serre.txt
git commit -m "feat(serre): plan de la serre"
git switch main
printf "tomates\ncourgettes\nharicots\n" > parcelles.txt
git commit -am "feat(parcelles): ajout des haricots"
