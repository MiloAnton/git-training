git switch -c feature/vrac
printf "Vrac : legumineuses\n" > vrac.txt
git add vrac.txt
git commit -m "feat(vrac): legumineuses"
printf "Vrac : legumineuses\nVrac : cereales\n" > vrac.txt
git commit -am "feat(vrac): cereales"
git switch main
printf "Ouvert du mardi au samedi\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): jours d'ouverture"
git switch -c fix/etiquette
printf "Etiquettes : prix au kilo\n" > etiquettes.txt
git add etiquettes.txt
git commit -m "fix(etiquettes): prix au kilo"
git switch main
git merge fix/etiquette
git merge --no-ff feature/vrac
git branch -d fix/etiquette
git branch -d feature/vrac
git log --oneline --all
git show HEAD --stat
