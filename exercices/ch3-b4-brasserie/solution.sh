git switch -c feature/blonde
printf "Blonde : malt pale, houblon Saaz\n" > blonde.txt
git add blonde.txt
git commit -m "feat(blonde): recette de la blonde"
git switch main
git switch -c feature/ambree
printf "Ambree : malt caramel\n" > ambree.txt
git add ambree.txt
git commit -m "feat(ambree): recette de l'ambree"
git switch main
git switch -c feature/brune
printf "Brune : malt torrefie\n" > brune.txt
git add brune.txt
git commit -m "feat(brune): recette de la brune"
git switch main
printf "Etiquettes rondes, papier kraft\n" > etiquettes.txt
git add etiquettes.txt
git commit -m "feat(etiquettes): choix du support"
git branch -v
git log --oneline --all
