/* Plateforme d'entrainement Leonis - logique de la page chapitre */
(function () {
  'use strict';

  var MASQUES = [
    [/^\[([\w./-]+) \(root-commit\) [0-9a-f]{7,40}\]/, '[$1 (root-commit) ...]'],
    [/^\[([\w./-]+) [0-9a-f]{7,40}\]/, '[$1 ...]'],
    [/^commit [0-9a-f]{40}/, 'commit ...'],
    [/^([*|\\/ ]*)([0-9a-f]{7,8}) /, '$1... '],
    [/\b[0-9a-f]{7,8}\.\.[0-9a-f]{7,8}\b/g, '...'],
    [/^index [0-9a-f]{7,40}\.\.[0-9a-f]{7,40}/, 'index ...']
  ];

  function masque(l) {
    MASQUES.forEach(function (m) { l = l.replace(m[0], m[1]); });
    return l;
  }

  // un "..." dans l'attendu vaut n'importe quoi, le reste est compare au caractere pres
  function correspond(attendu, obtenu) {
    if (obtenu === undefined) return false;
    if (attendu.indexOf('...') === -1) return attendu === obtenu;
    var parts = attendu.split('...');
    var pos = 0;
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      if (p === '') continue;
      var k = obtenu.indexOf(p, pos);
      if (k === -1) return false;
      if (i === 0 && k !== 0) return false;
      pos = k + p.length;
    }
    if (parts[parts.length - 1] !== '' && pos !== obtenu.length) return false;
    return true;
  }

  // ------------------------------------------------------------------ crypto

  function b64(s) {
    var bin = atob(s), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  function dechiffre(blob, code, iterations) {
    var oct = b64(blob);
    var sel = oct.slice(0, 16), iv = oct.slice(16, 28), ct = oct.slice(28);
    return crypto.subtle.importKey('raw', new TextEncoder().encode(code),
                                   'PBKDF2', false, ['deriveKey'])
      .then(function (mat) {
        return crypto.subtle.deriveKey(
          { name: 'PBKDF2', salt: sel, iterations: iterations, hash: 'SHA-256' },
          mat, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
      })
      .then(function (cle) {
        return crypto.subtle.decrypt({ name: 'AES-GCM', iv: iv }, cle, ct);
      })
      .then(function (clair) {
        return JSON.parse(new TextDecoder().decode(clair));
      });
  }

  // -------------------------------------------------------------------- rendu

  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt !== undefined) e.textContent = txt;
    return e;
  }

  function rendTerminal(noeud, lignes) {
    noeud.textContent = '';
    if (!lignes.length) {
      noeud.appendChild(el('span', 'vide', 'Rien pour le moment.'));
      return;
    }
    lignes.forEach(function (l) {
      if (l.indexOf('$ ') === 0) {
        var s = el('span', 'invite', l);
        noeud.appendChild(s);
      } else {
        noeud.appendChild(document.createTextNode(l));
      }
      noeud.appendChild(document.createTextNode('\n'));
    });
  }

  // --------------------------------------------------------------------- app

  var D = null, INDICES = null, CORRECTIONS = null;
  var vms = {};

  function cle(ident) { return 'leonis-git-' + D.chapitre + '-' + ident; }

  function charge(ident) {
    try { return localStorage.getItem(cle(ident)); } catch (e) { return null; }
  }
  function sauve(ident, v) {
    try { localStorage.setItem(cle(ident), v); } catch (e) { /* mode prive */ }
  }

  function construitExercice(ex, index) {
    var carte = el('section', 'exo');
    carte.id = ex.ident;

    var h3 = el('h3');
    h3.appendChild(el('span', 'num', index + '.'));
    h3.appendChild(document.createTextNode(ex.titre));
    carte.appendChild(h3);

    var en = el('div', 'enonce');
    en.innerHTML = ex.enonce;
    carte.appendChild(en);

    carte.appendChild(el('div', 'etiquette', 'Exemple attendu'));
    var attendu = el('pre', 'terminal');
    rendTerminal(attendu, ex.exemple);
    carte.appendChild(attendu);

    if (ex.graphe && ex.graphe.commits && ex.graphe.commits.length) {
      carte.appendChild(el('div', 'etiquette', 'Sch\u00e9ma attendu'));
      var boiteAttendu = el('div', 'schema');
      boiteAttendu.innerHTML = Schema.dessine(ex.graphe, { titre: 'Sch\u00e9ma attendu' });
      carte.appendChild(boiteAttendu);
    }

    carte.appendChild(el('div', 'etiquette', 'Tes commandes'));
    var ta = el('textarea');
    var sauvegarde = charge(ex.ident);
    ta.value = sauvegarde !== null ? sauvegarde : '';
    carte.appendChild(ta);

    var outils = el('div', 'outils');
    var bLancer = el('button', 'principal', 'Lancer');
    var bVerif = el('button', 'jaune', 'V\u00e9rifier mon programme');
    var bReset = el('button', '', 'R\u00e9initialiser');
    var bascule = el('label', 'bascule');
    var chk = document.createElement('input');
    chk.type = 'checkbox';
    bascule.appendChild(chk);
    bascule.appendChild(document.createTextNode('Autocompl\u00e9tion'));
    outils.appendChild(bLancer);
    outils.appendChild(bVerif);
    outils.appendChild(bReset);
    outils.appendChild(bascule);
    carte.appendChild(outils);

    carte.appendChild(el('div', 'etiquette', 'R\u00e9sultat'));
    var sortie = el('pre', 'terminal sortie');
    rendTerminal(sortie, []);
    carte.appendChild(sortie);

    var etiqSchema = el('div', 'etiquette', 'Ton sch\u00e9ma');
    etiqSchema.style.display = 'none';
    var boiteSchema = el('div', 'schema');
    boiteSchema.style.display = 'none';

    var saisie = el('div', 'ligne-saisie');
    saisie.appendChild(el('span', '', '$'));
    var champ = document.createElement('input');
    champ.type = 'text';
    champ.placeholder = 'tape une commande pour explorer l’état laissé par ton dernier lancement';
    saisie.appendChild(champ);
    carte.appendChild(saisie);

    carte.appendChild(etiqSchema);
    carte.appendChild(boiteSchema);

    var verdict = el('div', 'verdict');
    carte.appendChild(verdict);

    // aide
    var aide = el('div', 'aide');
    var zoneInd = el('div');
    var bInd = el('button', '', 'Afficher un indice');
    var verrouInd = el('span', 'verrou', ' Saisis le code de s\u00e9ance des indices en haut de page.');
    aide.appendChild(bInd);
    aide.appendChild(verrouInd);
    aide.appendChild(zoneInd);

    var details = el('details', 'correction');
    var som = el('summary', '', 'Voir la correction');
    details.appendChild(som);
    var preCor = el('pre');
    details.appendChild(preCor);
    aide.appendChild(details);
    carte.appendChild(aide);

    var editeur = CodeMirror.fromTextArea(ta, {
      mode: 'shell',
      lineNumbers: true,
      lineWrapping: true,
      viewportMargin: Infinity,
      extraKeys: {}
    });

    editeur.on('change', function () { sauve(ex.ident, editeur.getValue()); });

    chk.addEventListener('change', function () {
      if (chk.checked) {
        editeur.setOption('extraKeys', {
          'Ctrl-Space': 'autocomplete',
          "'g'": function (cm) { cm.replaceSelection('g'); completeDouce(cm); }
        });
        editeur.on('inputRead', completeDouce);
      } else {
        editeur.off('inputRead', completeDouce);
        editeur.setOption('extraKeys', {});
      }
    });

    var MOTS = ['git', 'status', 'add', 'commit', 'init', 'clone', 'push', 'pull',
                'reset', 'rm', '--cached', '--bare', '--no-edit', '-m', '-am',
                'echo', 'printf', 'cat', 'ls', 'cd', 'mkdir', 'pwd', '.gitignore'];

    function completeDouce(cm) {
      var cur = cm.getCursor();
      var jeton = cm.getTokenAt(cur).string.trim();
      if (jeton.length < 2) return;
      CodeMirror.showHint(cm, function () {
        var liste = MOTS.filter(function (m) { return m.indexOf(jeton) === 0 && m !== jeton; });
        if (!liste.length) return null;
        return {
          list: liste,
          from: CodeMirror.Pos(cur.line, cur.ch - jeton.length),
          to: cur
        };
      }, { completeSingle: false });
    }

    function execute(script) {
      var vm = Gitleo.creerSession(ex.seed);
      vms[ex.ident] = vm;
      return Gitleo.jouer(vm, script, { limiteMs: 4000 });
    }

    function montreSchema() {
      var vm = vms[ex.ident];
      if (!vm) return;
      var g = null;
      try { g = Gitleo.graphe(vm); } catch (e) { return; }
      if (!g || !g.commits.length) { 
        etiqSchema.style.display = 'none';
        boiteSchema.style.display = 'none';
        return;
      }
      boiteSchema.innerHTML = Schema.dessine(g, { titre: 'Ton sch\u00e9ma' });
      etiqSchema.style.display = '';
      boiteSchema.style.display = '';
    }

    bLancer.addEventListener('click', function () {
      verdict.className = 'verdict';
      var lignes;
      try { lignes = execute(editeur.getValue()); }
      catch (err) { lignes = ['Erreur interne du moteur : ' + err.message]; }
      rendTerminal(sortie, lignes);
      montreSchema();
    });

    bReset.addEventListener('click', function () {
      editeur.setValue('');
      rendTerminal(sortie, []);
      etiqSchema.style.display = 'none';
      boiteSchema.style.display = 'none';
      verdict.className = 'verdict';
    });

    champ.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      var cmd = champ.value.trim();
      if (!cmd) return;
      champ.value = '';
      if (!vms[ex.ident]) vms[ex.ident] = Gitleo.creerSession(ex.seed);
      var r = Gitleo.executeLigne(vms[ex.ident], cmd);
      var actuel = sortie.textContent.replace(/\n$/, '');
      var lignes = actuel && actuel.indexOf('Rien pour le moment') === -1
        ? actuel.split('\n') : [];
      lignes.push('$ ' + cmd);
      r.lignes.forEach(function (l) { lignes.push(l); });
      rendTerminal(sortie, lignes);
      sortie.scrollTop = sortie.scrollHeight;
      montreSchema();
    });

    bVerif.addEventListener('click', function () {
      var obtenu;
      try { obtenu = execute(editeur.getValue()).map(masque); }
      catch (err) {
        verdict.className = 'verdict ko';
        verdict.textContent = 'Le moteur n’a pas pu exécuter ton programme : ' + err.message;
        return;
      }
      rendTerminal(sortie, obtenu);
      montreSchema();
      var att = ex.exemple;
      var n = Math.max(att.length, obtenu.length);
      var ecart = -1;
      for (var i = 0; i < n; i++) {
        if (!correspond(att[i] === undefined ? '\u0000' : att[i], obtenu[i])) { ecart = i; break; }
      }
      verdict.textContent = '';
      if (ecart === -1) {
        verdict.className = 'verdict ok';
        verdict.appendChild(document.createTextNode(
          'C’est exactement la sortie attendue, ligne par ligne. Exercice réussi.'));
      } else {
        verdict.className = 'verdict ko';
        verdict.appendChild(document.createTextNode(
          'Premi\u00e8re diff\u00e9rence \u00e0 la ligne ' + (ecart + 1) + '.'));
        var bloc = el('div', 'ecart');
        bloc.textContent =
          'attendu : ' + (att[ecart] === undefined ? '(rien de plus)' : JSON.stringify(att[ecart])) +
          '\nobtenu  : ' + (obtenu[ecart] === undefined ? '(rien)' : JSON.stringify(obtenu[ecart]));
        verdict.appendChild(bloc);
      }
    });

    // indices et correction
    var vus = 0;
    bInd.addEventListener('click', function () {
      if (!INDICES) return;
      var liste = INDICES[ex.ident] || [];
      if (vus >= liste.length) { bInd.disabled = true; return; }
      zoneInd.appendChild(el('div', 'indice', 'Indice ' + (vus + 1) + '. ' + liste[vus]));
      vus++;
      if (vus >= liste.length) { bInd.disabled = true; bInd.textContent = 'Plus d’indice'; }
    });

    carte._deverrouilleIndices = function () {
      verrouInd.textContent = ' ' + ex.nb_indices + ' indices disponibles.';
      bInd.disabled = false;
    };
    carte._deverrouilleCorrection = function () {
      preCor.textContent = CORRECTIONS[ex.ident];
      som.textContent = 'Voir la correction';
    };

    bInd.disabled = true;
    som.textContent = 'Correction verrouill\u00e9e';
    details.addEventListener('click', function (e) {
      if (!CORRECTIONS) { e.preventDefault(); }
    });

    return carte;
  }

  function demarre(donnees) {
    D = donnees;
    document.getElementById('titre-ch').textContent =
      'Chapitre ' + D.chapitre + '. ' + D.titre;
    document.getElementById('sous-ch').textContent = D.sous_titre;
    document.title = 'Chapitre ' + D.chapitre + ' - Entrainement Git - Leonis';

    var ul = document.getElementById('limites');
    D.limites.forEach(function (l) { ul.appendChild(el('li', '', l)); });

    var conteneur = document.getElementById('exercices');
    var niveauCourant = null, compteur = 0;
    var cartes = [];
    D.exercices.forEach(function (ex) {
      if (ex.niveau !== niveauCourant) {
        niveauCourant = ex.niveau;
        compteur = 0;
        conteneur.appendChild(el('h2', 'niveau', ex.niveau));
      }
      compteur++;
      var c = construitExercice(ex, compteur);
      cartes.push(c);
      conteneur.appendChild(c);
    });

    function brancheCode(idInput, idEtat, blob, apres) {
      var input = document.getElementById(idInput);
      var etat = document.getElementById(idEtat);
      input.addEventListener('keydown', function (e) {
        if (e.key !== 'Enter') return;
        etat.textContent = 'v\u00e9rification...';
        dechiffre(blob, input.value.trim(), D.iterations).then(function (obj) {
          apres(obj);
          etat.textContent = 'ouvert';
          etat.className = 'etat ouvert';
          input.disabled = true;
        }).catch(function () {
          etat.textContent = 'code refus\u00e9';
          etat.className = 'etat';
        });
      });
    }

    brancheCode('code-indices', 'etat-indices', D.indices, function (obj) {
      INDICES = obj;
      cartes.forEach(function (c) { c._deverrouilleIndices(); });
    });
    brancheCode('code-corrections', 'etat-corrections', D.corrections, function (obj) {
      CORRECTIONS = obj;
      cartes.forEach(function (c) { c._deverrouilleCorrection(); });
    });
  }

  window.addEventListener('DOMContentLoaded', function () {
    var ch = document.body.getAttribute('data-chapitre');
    fetch('data/chapitre-' + ch + '.json')
      .then(function (r) { return r.json(); })
      .then(demarre)
      .catch(function (e) {
        document.getElementById('exercices').textContent =
          'Impossible de charger les exercices : ' + e.message;
      });
  });
})();
