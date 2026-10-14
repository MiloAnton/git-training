git init escape
cd escape
printf "Salle 1 : le coffre\n" > salles.txt
git add salles.txt
git commit -m "feat(salles): premiere salle"
git switch -c enigmes
printf "Enigme du cadran\n" > enigmes.txt
git add enigmes.txt
git commit -m "feat(enigmes): enigme du cadran"
git switch main
