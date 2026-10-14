git init camping
cd camping
printf "Emplacement 1 : ombrage\n" > carte.txt
git add carte.txt
git commit -m "feat(carte): premier emplacement"
git switch -c feature/emplacements
