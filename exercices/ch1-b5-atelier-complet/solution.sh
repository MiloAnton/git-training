git clone https://github.com/leonis-formation/depot-asso.git site
cd site
ls
git status
printf "*.log\n" > .gitignore
git status
printf "Permanence : mardi 18h-20h\n" > horaires.txt
git add .gitignore horaires.txt
git status
git commit -m "feat(horaires): ajout des horaires et exclusion des journaux"
git push
git status
