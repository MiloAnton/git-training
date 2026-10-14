printf "lundi : mise en route\nmercredi : premiers essais\nvendredi : revue de la semaine\n" > avancement.txt
git add avancement.txt
git diff
git diff --staged
git commit -m "feat(avancement): point du vendredi"
git log --oneline --graph
git log --stat -n 3
git diff HEAD~3 HEAD
git diff HEAD~3 HEAD --name-only
