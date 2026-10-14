git status
printf "Version 2.1\nDate : 5 janvier\n" > version.txt
printf "correction du calcul de TVA\n" > notes-internes.txt
git add version.txt
git status
git diff
git diff --staged
git diff HEAD
git diff HEAD --name-only
