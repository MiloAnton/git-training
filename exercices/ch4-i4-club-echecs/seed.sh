git init echecs
cd echecs
printf "Club d'echecs de la Tour\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le club"
git switch -c feature/tournoi
printf "Tournoi : 12 janvier\n" > tournoi.txt
git add tournoi.txt
git commit -m "feat(tournoi): date du tournoi"
git switch main
git switch -c feature/cours
printf "Cours debutants : mercredi\n" > cours.txt
git add cours.txt
git commit -m "feat(cours): cours debutants"
git switch main
