git init supervision
cd supervision
printf "cpu = 80\nmemoire = 75\n" > seuils.txt
git add seuils.txt
git commit -m "feat(seuils): seuils d'alerte initiaux"
printf "Alerte par courriel\n" > alertes.txt
git add alertes.txt
git commit -m "feat(alertes): canal courriel"
printf "cpu = 99\nmemoire = 98\n" > seuils.txt
git commit -am "fix(seuils): seuils remontes en urgence"
printf "cpu = 99\nmemoire = 98\ndisque = 95\n" > seuils.txt
git commit -am "feat(seuils): ajout du seuil disque"
