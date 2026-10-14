git switch -c feature/programme
printf "Samedi : concert\nDimanche : a definir\n" > programme.txt
git add programme.txt
git commit -m "feat(programme): concert du samedi"
printf "Samedi : concert\nDimanche : brocante\n" > programme.txt
git commit -am "feat(programme): brocante le dimanche"
git switch main
printf "Samedi : a definir\nDimanche : vide-grenier\n" > programme.txt
git add programme.txt
git commit -m "feat(programme): vide-grenier le dimanche"
git merge feature/programme
git status
git diff --name-only --diff-filter=U
cat programme.txt
git log --oneline --all
git restore --theirs -- programme.txt
git add programme.txt
git status
git commit -m "fix(programme): resolution, on garde le programme de la branche"
git log --oneline --all
git show HEAD --stat
cat programme.txt
git branch
git branch -d feature/programme
