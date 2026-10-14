git init ressourcerie
cd ressourcerie
printf "Ressourcerie du Pont\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la ressourcerie"
git switch -c feature/collecte
printf "Collecte : mardi et samedi\n" > collecte.txt
git add collecte.txt
git commit -m "feat(collecte): jours de collecte"
git switch main
printf "Ressourcerie du Pont\nOuverte a tous\n" > presentation.txt
git commit -am "feat(presentation): precision"
