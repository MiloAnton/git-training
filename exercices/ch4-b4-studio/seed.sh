git init studio
cd studio
printf "Studio Les Ondes\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): le studio"
git switch -c feature/micros
printf "Micro statique : 2\nMicro dynamique : 4\n" > micros.txt
git add micros.txt
git commit -m "feat(micros): parc de micros"
git switch main
git switch -c feature/cabine
printf "Cabine : 12 m2, traitement acoustique\n" > cabine.txt
git add cabine.txt
git commit -m "feat(cabine): dimensions"
git switch main
