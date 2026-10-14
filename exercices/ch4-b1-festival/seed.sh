git init festival
cd festival
printf "Festival des Rives\nEdition 2026\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le festival"
git switch -c fix/typo
printf "Festival des Rives\nEdition 2026, 3 jours\n" > presentation.txt
git commit -am "fix(presentation): precision sur la duree"
git switch main
git switch -c feature/scene
printf "Scene principale : 2000 places\n" > scene.txt
git add scene.txt
git commit -m "feat(scene): capacite"
printf "Scene principale : 2000 places\nScene acoustique : 300 places\n" > scene.txt
git commit -am "feat(scene): seconde scene"
git switch main
git switch -c feature/buvette
printf "Buvette : 4 points de vente\n" > buvette.txt
git add buvette.txt
git commit -m "feat(buvette): points de vente"
git switch main
git switch -c abandonnee
printf "idee non retenue\n" > idee.txt
git add idee.txt
git commit -m "feat(idee): piste non retenue"
git switch main
