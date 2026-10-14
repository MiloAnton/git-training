printf "mardi : fractionne\njeudi : endurance\n" > planning.txt
printf "12 plots\n4 chronos\n" > materiel.txt
printf "demander une augmentation au président\n" > brouillon-perso.txt
git status
git add planning.txt
git commit -m "feat(planning): ajout des séances de la semaine"
git add materiel.txt
git commit -m "feat(materiel): ajout du matériel du club"
printf "brouillon-perso.txt\n" > .gitignore
git status
git add .gitignore
git commit -m "config(depot): exclusion du brouillon personnel"
git status
