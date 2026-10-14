git init savonnerie
cd savonnerie
printf "Savonnerie du Moulin\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la savonnerie"
git switch -c feature/parfums
printf "Lavande\n" > parfums.txt
git add parfums.txt
git commit -m "wip parfum 1"
printf "Lavande\nVerveine\n" > parfums.txt
git commit -am "wip parfum 2"
printf "Lavande\nVerveine\nMiel\n" > parfums.txt
git commit -am "wip parfum 3"
printf "Lavande\nVerveine\nMiel\nRomarin\n" > parfums.txt
git commit -am "wip parfum 4"
git switch main
