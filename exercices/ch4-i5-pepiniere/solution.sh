git switch main
git merge --no-ff feature/semis
git merge --no-ff feature/greffes
git branch -d feature/semis
git branch -d feature/greffes
git branch
git log --oneline --all
