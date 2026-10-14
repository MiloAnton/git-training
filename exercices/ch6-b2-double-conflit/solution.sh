git merge feature/saison
git status
git diff --name-only --diff-filter=U
cat tarifs.txt
cat horaires.txt
git restore --ours -- tarifs.txt
git restore --theirs -- horaires.txt
git add tarifs.txt
git add horaires.txt
git status
git commit -m "fix(saison): resolution, nos tarifs et leurs horaires"
cat tarifs.txt
cat horaires.txt
git log --oneline --all
