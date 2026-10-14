cat couleurs.txt
git restore --theirs -- couleurs.txt
git add couleurs.txt
git commit -m "fix(couleurs): resolution du conflit, on garde le vert"
git log --oneline --all
