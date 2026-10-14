git merge feature/edito
git status
git diff --name-only --diff-filter=U
cat une.txt
git restore --ours -- une.txt
git add une.txt
git commit -m "fix(une): resolution du conflit sur le titre"
git log --oneline --all
