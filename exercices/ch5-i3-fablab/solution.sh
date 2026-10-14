git log --oneline
git revert HEAD~1 --no-edit
git commit --amend -m "fix(machines): annulation de la ligne du laser"
git log --oneline
cat machines.txt
