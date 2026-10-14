git status
git rm --cached cles-api.txt
git status
printf "cles-api.txt\n" > .gitignore
git status
git add .gitignore
git commit -m "config(depot): retrait des clés du suivi et ajout du gitignore"
git status
ls
cat cles-api.txt
