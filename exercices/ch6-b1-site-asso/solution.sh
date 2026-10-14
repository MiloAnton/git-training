git merge feature/refonte
git status
git diff --name-only --diff-filter=U
cat accueil.txt
git log --oneline --all
git restore --ours -- accueil.txt
git add accueil.txt
git commit -m "fix(accueil): resolution du conflit, on garde le slogan actuel"
git status
git log --oneline --all
git show HEAD --stat
