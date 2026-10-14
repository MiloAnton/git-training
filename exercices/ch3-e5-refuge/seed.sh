git init refuge
cd refuge
printf "Nuitee : 22 euros\n" > tarifs.txt
git add tarifs.txt
git commit -m "feat(tarifs): tarifs de base"
git switch -c fix/tarifs
printf "Nuitee : 24 euros\nRepas : 18 euros\n" > tarifs.txt
git commit -am "fix(tarifs): mise a jour 2026"
git switch main
git merge fix/tarifs
