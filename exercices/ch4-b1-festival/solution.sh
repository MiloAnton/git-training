git switch main
git merge fix/typo
git merge --no-ff feature/scene
git merge --ff-only feature/buvette
git merge feature/buvette
git branch -d fix/typo
git branch -d feature/scene
git branch -d feature/buvette
git branch -d abandonnee
git branch
git log --oneline --all
