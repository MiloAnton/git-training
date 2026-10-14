git commit --amend -m "feat(stands): ajout du stand des livres"
git log --oneline
git restore tarifs.txt
git restore --staged brouillon.txt
git status
git revert HEAD~2 --no-edit
git show HEAD --stat
git log --oneline
git reflog
