const fs=require('fs');const G=require('./public/assets/gitleo.js');
const MASQUES=[[/^\[([\w./-]+) \(root-commit\) [0-9a-f]{7,40}\]/,'[$1 (root-commit) ...]'],
[/^\[([\w./-]+) [0-9a-f]{7,40}\]/,'[$1 ...]'],[/^commit [0-9a-f]{40}/,'commit ...'],
[/^([*|\\/ ]*)([0-9a-f]{7,8}) /,'$1... '],[/\b[0-9a-f]{7,8}\.\.[0-9a-f]{7,8}\b/g,'...'],
[/^index [0-9a-f]{7,40}\.\.[0-9a-f]{7,40}/,'index ...'],
[/^([ *]\s+[\w./-]+\s+)[0-9a-f]{7,8} /,'$1... '],[/\(was [0-9a-f]{7,40}\)/,'(was ...)'],
[/(WIP on [\w./-]+: )[0-9a-f]{7,40} /,'$1... '],[/^(HEAD is now at )[0-9a-f]{7,40} /,'$1... '],
[/^(Dropped refs\/stash@\{\d+\} \()[0-9a-f]{40}\)/,'$1...)']];
const m=l=>{MASQUES.forEach(([r,p])=>l=l.replace(r,p));return l;};
const d='exercices/'+process.argv[2];
const seed=fs.existsSync(d+'/seed.sh')?fs.readFileSync(d+'/seed.sh','utf8'):'';
const vm=G.creerSession(seed);
const obt=G.jouer(vm,fs.readFileSync(d+'/solution.sh','utf8')).map(m);
const att=fs.readFileSync(d+'/exemple.txt','utf8').replace(/\n$/,'').split('\n');
for(let i=0;i<Math.max(att.length,obt.length);i++){
 if(att[i]!==obt[i]){for(let k=Math.max(0,i-2);k<=i+4;k++)console.log(' a['+k+'] '+JSON.stringify(att[k])+'\n o['+k+'] '+JSON.stringify(obt[k]));break;}}
