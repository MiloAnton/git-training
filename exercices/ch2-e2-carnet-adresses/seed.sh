git init carnet
cd carnet
printf "Sarah Benali\n" > adresses.txt
git add adresses.txt
git commit -m "feat(adresses): ajout de Sarah"
printf "Tom Rivet\n" >> adresses.txt
git commit -am "feat(adresses): ajout de Tom"
printf "Amel Diarra\n" >> adresses.txt
git commit -am "feat(adresses): ajout d'Amel"
printf "Reunions le mardi a 18h\n" > infos.txt
git add infos.txt
git commit -m "feat(infos): horaire des reunions"
printf "Local : salle B12\n" >> infos.txt
git commit -am "feat(infos): ajout du local"
