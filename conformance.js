/* Test de conformite : le moteur du site doit reproduire exactement
   la transcription produite par le vrai Git. */
const fs = require('fs');
const path = require('path');
const Gitleo = require('./public/assets/gitleo.js');

const BASE = 'exercices';

const MASQUES = [
  [/^\[([\w./-]+) \(root-commit\) [0-9a-f]{7,40}\]/, '[$1 (root-commit) ...]'],
  [/^\[([\w./-]+) [0-9a-f]{7,40}\]/, '[$1 ...]'],
  [/^commit [0-9a-f]{40}/, 'commit ...'],
  [/^([*|\\/ ]*)([0-9a-f]{7,8}) /, '$1... '],
  [/\b[0-9a-f]{7,8}\.\.[0-9a-f]{7,8}\b/g, '...'],
  [/^index [0-9a-f]{7,40}\.\.[0-9a-f]{7,40}/, 'index ...'],
  [/^([ *]\s+[\w./-]+\s+)[0-9a-f]{7,8} /, '$1... '],
  [/\(was [0-9a-f]{7,40}\)/, '(was ...)'],
  [/^Merge: [0-9a-f]{7,40} [0-9a-f]{7,40}/, 'Merge: ...'],
  [/^(    This reverts commit )[0-9a-f]{40}\./, '$1....'],
  [/(WIP on [\w./-]+: )[0-9a-f]{7,40} /, '$1... '],
  [/^(HEAD is now at )[0-9a-f]{7,40} /, '$1... '],
  [/^(Dropped refs\/stash@\{\d+\} \()[0-9a-f]{40}\)/, '$1...)'],


];

function masque(l) {
  MASQUES.forEach(([rx, rep]) => { l = l.replace(rx, rep); });
  return l;
}

function lis(p) { return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null; }

let total = 0, ok = 0;
const echecs = [];

for (const d of fs.readdirSync(BASE).sort()) {
  const p = path.join(BASE, d);
  if (!fs.existsSync(path.join(p, 'meta.json'))) continue;
  total++;
  const seed = lis(path.join(p, 'seed.sh')) || '';
  const sol = lis(path.join(p, 'solution.sh'));
  const attendu = lis(path.join(p, 'exemple.txt')).replace(/\n$/, '').split('\n');

  let obtenu;
  try {
    const vm = Gitleo.creerSession(seed);
    obtenu = Gitleo.jouer(vm, sol).map(masque);
  } catch (e) {
    echecs.push({ d, err: e.message + '\n' + e.stack.split('\n')[1] });
    continue;
  }

  let diff = null;
  const n = Math.max(attendu.length, obtenu.length);
  for (let i = 0; i < n; i++) {
    if (attendu[i] !== obtenu[i]) {
      diff = { i, a: attendu[i], o: obtenu[i] };
      break;
    }
  }
  if (!diff) { ok++; console.log('OK    ' + d); }
  else {
    echecs.push({ d, diff, attendu, obtenu });
    console.log('ECHEC ' + d + '  (ligne ' + (diff.i + 1) + ')');
  }
}

console.log('\n' + ok + '/' + total + ' exercices conformes');

if (process.argv[2] === '-v' && echecs.length) {
  const e = echecs[0];
  console.log('\n=== premier ecart : ' + e.d);
  if (e.err) { console.log(e.err); }
  else {
    const i = e.diff.i;
    for (let k = Math.max(0, i - 6); k <= Math.min(i + 4, Math.max(e.attendu.length, e.obtenu.length) - 1); k++) {
      const marque = k === i ? ' <<<' : '';
      console.log('  [' + k + '] attendu: ' + JSON.stringify(e.attendu[k]) + marque);
      console.log('  [' + k + '] obtenu : ' + JSON.stringify(e.obtenu[k]) + marque);
    }
  }
}
process.exit(ok === total ? 0 : 1);
