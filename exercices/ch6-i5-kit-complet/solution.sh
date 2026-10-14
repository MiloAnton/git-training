git status
git diff --name-only --diff-filter=U
cat regles.txt
git log --oneline --all
git restore --theirs -- regles.txt
git add regles.txt
git commit -m "fix(regles): resolution, on garde la version du club"
git log --oneline --all
