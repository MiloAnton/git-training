git switch main
git diff --stat main feature/salles
git merge --no-ff feature/salles
git show HEAD --stat
git log --oneline --all
git diff --stat main feature/tarifs
git merge --no-ff feature/tarifs
git show HEAD --stat
git branch -d feature/salles
git branch -d feature/tarifs
git log --oneline --all
