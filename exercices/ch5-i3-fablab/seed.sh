git init fablab
cd fablab
printf "Imprimante 3D : 1\n" > machines.txt
git add machines.txt
git commit -m "feat(machines): imprimante 3D"
printf "Imprimante 3D : 1\nDecoupe laser : 900 W\n" > machines.txt
git commit -am "feat(machines): decoupe laser"
printf "Fraiseuse : 1\n" > fraiseuse.txt
git add fraiseuse.txt
git commit -m "feat(fraiseuse): nouvelle fraiseuse"
