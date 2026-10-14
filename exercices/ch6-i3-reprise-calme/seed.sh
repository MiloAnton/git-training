git init contact
cd contact
printf "Adresse : a completer\nTelephone : 01 02 03 04 05\n" > contact.txt
git add contact.txt
git commit -m "feat(contact): fiche de contact"
git switch -c feature/adresse
printf "Adresse : 4 rue des Lilas\nTelephone : 01 02 03 04 05\n" > contact.txt
git commit -am "feat(contact): adresse rue des Lilas"
git switch main
printf "Adresse : 12 place du Marche\nTelephone : 01 02 03 04 05\n" > contact.txt
git commit -am "feat(contact): adresse place du Marche"
