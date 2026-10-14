git init horaires
cd horaires
printf "Ouverture : 9h\nFermeture : a definir\n" > horaires.txt
git add horaires.txt
git commit -m "feat(horaires): ouverture"
git switch -c feature/soir
printf "Ouverture : 9h\nFermeture : 20h\n" > horaires.txt
git commit -am "feat(horaires): fermeture a 20h"
git switch main
printf "Ouverture : 9h\nFermeture : 18h\n" > horaires.txt
git commit -am "feat(horaires): fermeture a 18h"
git merge feature/soir
