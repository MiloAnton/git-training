/* schema.js - dessine le graphe des commits en SVG, a la maniere des schemas
   du cours : le temps va de gauche a droite, chaque branche a sa ligne.
   Fonctionne dans le navigateur et sous Node. */
(function (global) {
  'use strict';

  var VERT = '#109391', ENCRE = '#222725', JAUNE = '#fff81f';
  var GRIS = '#8a8a80', TRAIT = '#d8d6ca';
  var LANES = ['#109391', '#9a5b2f', '#4a5bb0', '#7a3f8f', '#2f7a46'];

  var PAS_X = 164, PAS_Y = 104, RAYON = 13;
  var MARGE_G = 96, MARGE_H = 40, MARGE_B = 40, MARGE_D = 96;

  function echappe(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // place chaque commit : x = profondeur depuis la racine, y = ligne de branche
  function place(g) {
    var par = {};
    g.commits.forEach(function (c) { par[c.h] = c; });

    var ordre = g.commits.slice().sort(function (a, b) { return a.date - b.date; });
    var col = {};
    ordre.forEach(function (c) {
      var m = -1;
      c.parents.forEach(function (p) {
        if (col[p] !== undefined && col[p] > m) m = col[p];
      });
      col[c.h] = m + 1;
    });

    // les branches en premier, la courante en haut
    var noms = [];
    g.commits.forEach(function (c) {
      c.etiquettes.forEach(function (e) { if (noms.indexOf(e) === -1) noms.push(e); });
    });
    noms.sort(function (a, b) {
      if (a === g.tete) return -1;
      if (b === g.tete) return 1;
      if (a === 'main') return -1;
      if (b === 'main') return 1;
      return a < b ? -1 : 1;
    });

    var ligne = {}, prochaine = 0;
    noms.forEach(function (nom) {
      var tete = null;
      g.commits.forEach(function (c) {
        if (c.etiquettes.indexOf(nom) !== -1) tete = c.h;
      });
      if (!tete || ligne[tete] !== undefined) return;
      var l = prochaine++;
      var h = tete;
      while (h && ligne[h] === undefined) {
        ligne[h] = l;
        var c = par[h];
        h = c && c.parents.length ? c.parents[0] : null;
      }
    });
    g.commits.forEach(function (c) { if (ligne[c.h] === undefined) ligne[c.h] = prochaine++; });

    var maxCol = 0, maxLigne = 0;
    g.commits.forEach(function (c) {
      if (col[c.h] > maxCol) maxCol = col[c.h];
      if (ligne[c.h] > maxLigne) maxLigne = ligne[c.h];
    });
    return { col: col, ligne: ligne, maxCol: maxCol, maxLigne: maxLigne, par: par };
  }

  function dessine(g, options) {
    options = options || {};
    if (!g || !g.commits.length) {
      return '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="56" ' +
        'role="img" aria-label="Aucun commit"><text x="8" y="34" font-family="Outfit,sans-serif" ' +
        'font-size="14" fill="' + GRIS + '">Aucun commit pour le moment.</text></svg>';
    }
    var p = place(g);
    var L = MARGE_G + (p.maxCol + 1) * PAS_X + MARGE_D;
    var H = MARGE_H + (p.maxLigne + 1) * PAS_Y + MARGE_B;

    function X(h) { return MARGE_G + p.col[h] * PAS_X; }
    function Y(h) { return MARGE_H + p.ligne[h] * PAS_Y + RAYON + 6; }

    var s = [];
    s.push('<svg xmlns="http://www.w3.org/2000/svg" width="' + L + '" height="' + H +
           '" viewBox="0 0 ' + L + ' ' + H + '" role="img" aria-label="' +
           echappe(options.titre || 'Graphe des commits') + '">');
    s.push('<rect width="' + L + '" height="' + H + '" fill="#ffffff"/>');

    // noms de branche a gauche
    var vues = {};
    g.commits.forEach(function (c) {
      var l = p.ligne[c.h];
      if (vues[l] !== undefined) return;
      vues[l] = true;
    });

    // liens parent vers enfant
    g.commits.forEach(function (c) {
      c.parents.forEach(function (ph, k) {
        if (p.col[ph] === undefined) return;
        var x1 = X(ph), y1 = Y(ph), x2 = X(c.h), y2 = Y(c.h);
        var couleur = LANES[p.ligne[c.h] % LANES.length];
        if (y1 === y2) {
          s.push('<line x1="' + (x1 + RAYON) + '" y1="' + y1 + '" x2="' + (x2 - RAYON) +
                 '" y2="' + y2 + '" stroke="' + couleur + '" stroke-width="2.5"/>');
        } else {
          var mx = (x1 + x2) / 2;
          s.push('<path d="M ' + (x1 + RAYON) + ' ' + y1 + ' C ' + mx + ' ' + y1 + ', ' +
                 mx + ' ' + y2 + ', ' + (x2 - RAYON) + ' ' + y2 +
                 '" fill="none" stroke="' + (k === 0 ? couleur : GRIS) +
                 '" stroke-width="2.5"' + (k > 0 ? ' stroke-dasharray="5 4"' : '') + '/>');
        }
      });
    });

    // commits
    g.commits.forEach(function (c) {
      var x = X(c.h), y = Y(c.h);
      var couleur = LANES[p.ligne[c.h] % LANES.length];
      var fusion = c.parents.length > 1;
      s.push('<circle cx="' + x + '" cy="' + y + '" r="' + RAYON + '" fill="' +
             (fusion ? '#ffffff' : couleur) + '" stroke="' + couleur + '" stroke-width="3"/>');
      if (fusion) {
        s.push('<circle cx="' + x + '" cy="' + y + '" r="4.5" fill="' + couleur + '"/>');
      }
      s.push('<title>' + echappe(c.court + '  ' + c.message) + '</title>');
      s.push('<text x="' + x + '" y="' + (y + RAYON + 15) + '" text-anchor="middle" ' +
             'font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="' +
             GRIS + '">' + echappe(c.court) + '</text>');
      var msg = c.message.length > 26 ? c.message.slice(0, 25) + '…' : c.message;
      s.push('<text x="' + x + '" y="' + (y + RAYON + 29) + '" text-anchor="middle" ' +
             'font-family="Outfit,sans-serif" font-size="11.5" fill="' + ENCRE + '">' +
             echappe(msg) + '</text>');
    });

    // etiquettes de branche
    g.commits.forEach(function (c) {
      if (!c.etiquettes.length) return;
      var x = X(c.h), y = Y(c.h);
      c.etiquettes.slice().sort().forEach(function (nom, i) {
        var courant = (nom === g.tete);
        var texte = (courant ? 'HEAD → ' : '') + nom;
        var larg = texte.length * 6.6 + 16;
        var ey = y - RAYON - 14 - i * 22;
        s.push('<rect x="' + (x - larg / 2) + '" y="' + (ey - 13) + '" width="' + larg +
               '" height="20" rx="10" fill="' + (courant ? JAUNE : '#eeece0') +
               '" stroke="' + (courant ? ENCRE : TRAIT) + '" stroke-width="1"/>');
        s.push('<text x="' + x + '" y="' + (ey + 1.5) + '" text-anchor="middle" ' +
               'font-family="Outfit,sans-serif" font-size="11.5" font-weight="600" fill="' +
               ENCRE + '">' + echappe(texte) + '</text>');
      });
    });

    s.push('<text x="10" y="' + (H - 10) + '" font-family="Outfit,sans-serif" ' +
           'font-size="11" fill="' + GRIS + '">le temps va de la gauche vers la droite</text>');
    s.push('</svg>');
    return s.join('');
  }

  var API = { dessine: dessine };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  else global.Schema = API;
})(typeof window !== 'undefined' ? window : globalThis);
