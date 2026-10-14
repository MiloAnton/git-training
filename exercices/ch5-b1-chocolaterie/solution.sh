git log --oneline
git commit --amend -m "feat(recettes): ajout de la ganache"
git revert HEAD~2 --no-edit
git restore conditionnement.txt
git status
git log --oneline
git reflog
