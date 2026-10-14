git switch -c feature/rayons
printf "Rayon poche\nRayon jeunesse\n" > rayons.txt
git add rayons.txt
git commit -m "feat(rayons): plan des rayons"
git switch main
git switch -c feature/site
printf "Page accueil\n" > site.txt
git add site.txt
git commit -m "feat(site): page d'accueil"
printf "Page accueil\nPage contact\n" > site.txt
git stash
git switch main
git switch feature/site
git stash pop
git branch -v
git log --oneline --all
