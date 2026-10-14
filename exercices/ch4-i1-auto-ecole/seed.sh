git init autoecole
cd autoecole
printf "Auto-ecole du Centre\nOuvert 9h-18h\n" > infos.txt
git add infos.txt
git commit -m "feat(infos): informations generales"
git switch -c fix/horaires
printf "Auto-ecole du Centre\nOuvert 8h-19h\n" > infos.txt
git commit -am "fix(infos): correction des horaires"
git switch main
git switch -c feature/simulateur
printf "Simulateur : 2 postes\n" > simulateur.txt
git add simulateur.txt
git commit -m "feat(simulateur): deux postes"
printf "Simulateur : 2 postes\nSeances de 45 minutes\n" > simulateur.txt
git commit -am "feat(simulateur): duree des seances"
git switch main
