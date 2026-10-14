git init annulation
cd annulation
printf "Entree : 5 euros\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): tarif d'entree"
git switch -c feature/reduction
printf "Entree : 3 euros\n" > tarifs.txt
git commit -am "feat(tarifs): tarif reduit"
git switch main
printf "Entree : 6 euros\n" > tarifs.txt
git commit -am "feat(tarifs): hausse du tarif"
git merge feature/reduction
