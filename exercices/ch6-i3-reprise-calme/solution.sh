git merge feature/adresse
git merge --abort
git status
git merge feature/adresse
git restore --ours -- contact.txt
git add contact.txt
git commit -m "fix(contact): resolution du conflit d'adresse"
git log --oneline --all
