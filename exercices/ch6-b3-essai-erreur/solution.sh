git merge feature/affiche
git restore --ours -- affiche.txt
git add affiche.txt
git merge --abort
git status
git merge feature/affiche
git restore --theirs -- affiche.txt
git add affiche.txt
git commit -m "fix(affiche): resolution, on garde leur visuel"
cat affiche.txt
git log --oneline --all
