git init aeroclub
cd aeroclub
printf "1. Verifier le niveau d'huile\n2. Controler les gouvernes\n3. Tester la radio\n" > checklist.txt
git add checklist.txt
git commit -m "feat(checklist): version de janvier"
printf "1. Verifier le niveau d'huile\n2. Controler les gouvernes\n3. Tester la radio\n4. Verifier le carburant\n" > checklist.txt
git commit -am "feat(checklist): ajout du controle carburant"
printf "1. Verifier le niveau d'huile\n2. Controler les gouvernes et les volets\n3. Tester la radio\n4. Verifier le carburant\n" > checklist.txt
git commit -am "fix(checklist): precision sur les gouvernes"
