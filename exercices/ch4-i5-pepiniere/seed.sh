git init pepiniere
cd pepiniere
printf "Pepiniere des Coteaux\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la pepiniere"
git switch -c feature/semis
printf "Semis : fevrier sous abri\n" > semis.txt
git add semis.txt
git commit -m "feat(semis): calendrier des semis"
git switch main
git switch -c feature/greffes
printf "Greffes : mars\n" > greffes.txt
git add greffes.txt
git commit -m "feat(greffes): calendrier des greffes"
git switch main
