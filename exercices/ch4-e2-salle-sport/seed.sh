git init sport
cd sport
printf "Tarif annuel : 240 euros\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): tarif annuel"
git switch -c feature/planning
printf "Lundi 18h : cardio\n" > planning.txt
git add planning.txt
git commit -m "feat(planning): creneau cardio"
git switch main
printf "Tarif annuel : 240 euros\nTarif etudiant : 150 euros\n" > tarifs.txt
git commit -am "feat(tarifs): tarif etudiant"
