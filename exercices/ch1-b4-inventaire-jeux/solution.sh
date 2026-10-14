git add .
git status
git reset export.tmp
git reset photos
git status
printf "*.tmp\nphotos/\n" > .gitignore
git status
git add .
git commit -m "config(depot): inventaire et exclusion des fichiers temporaires"
git status
ls
