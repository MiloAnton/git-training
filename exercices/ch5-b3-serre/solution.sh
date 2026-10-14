git switch main
git diff --stat main feature/semis
git merge --squash feature/semis
git status
git commit -m "feat(semis): calendrier complet des semis"
git log --oneline --all
git show HEAD --stat
git branch
