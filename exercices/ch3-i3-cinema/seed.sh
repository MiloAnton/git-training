git init cineclub
cd cineclub
printf "Lundi : Les Temps modernes\n" > programme.txt
git add programme.txt
git commit -m "feat(programme): premiere seance"
git switch -c feature/programme
printf "Lundi : Les Temps modernes\nCycle Chaplin\n" > programme.txt
git commit -am "feat(programme): cycle Chaplin"
