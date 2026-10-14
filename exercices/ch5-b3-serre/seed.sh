git init serre
cd serre
printf "Serre municipale\n" > presentation.txt
git add presentation.txt
git commit -m "feat(presentation): la serre"
git switch -c feature/semis
printf "Janvier : poireaux\n" > semis.txt
git add semis.txt
git commit -m "wip 1"
printf "Janvier : poireaux\nFevrier : tomates\n" > semis.txt
git commit -am "wip 2"
printf "Janvier : poireaux\nFevrier : tomates\nMars : courges\n" > semis.txt
git commit -am "wip 3"
printf "Janvier : poireaux\nFevrier : tomates\nMars : courges\nAvril : haricots\n" > semis.txt
git commit -am "wip 4"
printf "Janvier : poireaux\nFevrier : tomates\nMars : courges\nAvril : haricots\nMai : courgettes\n" > semis.txt
git commit -am "wip 5"
git switch main
