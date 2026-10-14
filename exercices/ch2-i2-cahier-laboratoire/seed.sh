git init laboratoire
cd laboratoire
printf "Experience A : temoin\nResultat : stable\n" > exp-a.txt
git add exp-a.txt
git commit -m "feat(exp-a): protocole temoin"
printf "Experience B : dose faible\nResultat : en cours\n" > exp-b.txt
git add exp-b.txt
git commit -m "feat(exp-b): protocole dose faible"
printf "Experience A : temoin\nResultat : stable sur 48h\n" > exp-a.txt
printf "Experience C : dose forte\nResultat : en cours\n" > exp-c.txt
git add .
git commit -m "feat(exp-c): protocole dose forte et mise a jour du temoin"
