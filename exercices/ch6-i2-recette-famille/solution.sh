git merge feature/cuisson
cat tarte.txt
git restore --theirs -- tarte.txt
git add tarte.txt
git commit -m "fix(tarte): resolution sur le temps de cuisson"
cat tarte.txt
