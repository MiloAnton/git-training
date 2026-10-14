git init musee
cd musee
printf "Salle antique\n" > salles.txt
git add salles.txt
git commit -m "feat(salles): salle antique"
git switch -c truc
printf "Audioguide FR\n" > audioguide.txt
git add audioguide.txt
git commit -m "feat(audioguide): version francaise"
git switch main
git switch -c vieux-test
printf "Salle antique\nSalle moderne\n" > salles.txt
git commit -am "feat(salles): salle moderne"
git switch main
git merge vieux-test
git switch -c jamais-fini
printf "projet en suspens\n" > suspens.txt
git add suspens.txt
git commit -m "feat(suspens): piste non terminee"
git switch main
