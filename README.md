# Portfolio Christopher Schmidtke

Schwarzweißfotografie auf Film. Statische Website mit Jekyll, gehostet auf GitHub Pages.
Kein Tracking, keine externen Schriften oder Dienste.

**Wichtig:** Das Repository ist öffentlich. Alles, was hier liegt, kann jeder herunterladen.
Nur Web-Exporte hochladen, nie Originalscans.

## Was liegt wo

| Ordner / Datei | Inhalt |
|---|---|
| `_serien/` | Eine Datei pro Serie: Einleitungstext, Bilder, Alt-Texte, Reihen |
| `_posts/` | Journal-Beiträge als Markdown. Entwürfe liegen in `_drafts/` |
| `_data/veroeffentlichungen.yml` | Liste der Magazin-Veröffentlichungen |
| `assets/images/<serie>/` | Bilddateien, erzeugt von `tools/bilder.py` |
| `_config.yml` | Name, Adresse, Kontakt, Hängung, Suchmaschinen |
| `tools/bilder.py` | Bereitet Exporte für die Seite vor |

## Ein Bild austauschen oder hinzufügen

1. **Exportieren** (Lightroom, Capture One o. ä.): JPEG oder TIFF, sRGB, lange Kante mindestens 2400 px,
   Standortinformationen entfernen.
2. **Vorbereiten:**
   ```
   python3 tools/bilder.py ~/Export/kyoto.jpg --serie japan --name kyoto-torii --format 6x6
   ```
   `--format` ist `6x6`, `6x9` oder `kb`. Bei 3:2 ist die Angabe nötig, weil 6×9 und Kleinbild
   gleich proportioniert sind. Das Skript erzeugt eine Datei mit 1600 px langer Kante
   (einstellbar über `bildgroesse` in `_config.yml`), entfernt alle Metadaten (auch GPS)
   und setzt nur Urheber und Copyright.
3. **Eintragen:** Den ausgegebenen Block in `_serien/japan.md` unter `bilder:` einfügen oder einen
   bestehenden Eintrag ersetzen. `ort`, `jahr`, `kamera`, `film` und `alt` ausfüllen.
4. Beim Ersetzen die alten Dateien in `assets/images/japan/` löschen.
5. Committen und pushen. GitHub baut die Seite danach automatisch neu.

Einfacher Weg: das Bild im Claude-Projekt hochladen und sagen, welches ersetzt werden soll.

### Gute Alt-Texte

Ein Satz, was zu sehen ist, so als würdest du es jemandem am Telefon beschreiben.
Ort nennen, wenn er erkennbar ist. Nicht mit „Bild von“ beginnen, keine Stichwortlisten.

> Gut: „Ein einzelner Baum auf einem verschneiten Hügel, dahinter Nebel, Hokkaido.“
> Schlecht: „Japan Schwarzweiß Fotografie Baum Schnee analog“

## Reihen auf der Serienseite

`reihen: [2, 1, 3, 1, 2]` heißt: zwei Bilder nebeneinander, dann eins allein, dann drei, …
Ohne diese Zeile gruppiert die Seite automatisch. Bilder einer Reihe bekommen immer die gleiche
Höhe, die Breite ergibt sich aus dem Format. Beschnitten wird nichts.

## Neue Serie

Eine bestehende Datei in `_serien/` kopieren, umbenennen (der Dateiname wird zur Adresse,
z. B. `island.md` → `/serien/island/`), `title`, `reihenfolge` und Bilder anpassen.

## Journal-Beitrag

Datei `_posts/JJJJ-MM-TT-titel.md` anlegen:

```
---
title: Titel des Beitrags
description: Ein Satz, worum es geht (erscheint in der Liste und bei Google).
---
Text in Markdown …
```

Ein Bild im Text:
`{% include beitragsbild.html serie="japan" datei="japan-01" w="2400" h="2400" alt="…" text="Bildunterschrift" %}`

## Einstellungen in `_config.yml`

- Die Adresse der Seite setzt GitHub automatisch, auch später mit eigener Domain. `url` und
  `baseurl` deshalb nicht eintragen
- `author.email`, `author.instagram`: erscheinen auf „Über mich“
- `haengung`: `reihen`, `raster` oder `einzeln` (nur Desktop, am Handy immer eine Spalte)
- `bildgroesse`: lange Kante der Bilder in Pixel (Standard 1600). Nach einer Änderung alle Bilder
  mit `tools/bilder.py` neu erzeugen
- `indexierung`: `false` in der Testphase. Auf `true` stellen, wenn Bilder, Texte und Domain stehen
- `rechtliches`: auf `true`, sobald `impressum.md` und `datenschutz.md` angelegt sind

## Einmalig: auf GitHub Pages veröffentlichen

1. Auf GitHub ein öffentliches Repository mit dem Namen `BENUTZERNAME.github.io` anlegen.
2. Hochladen über „Add file → Upload files“: den Inhalt dieses Ordners hineinziehen, nicht den
   Ordner `portfolio` selbst. Sonst landet alles eine Ebene zu tief und die Seite bleibt leer.
   Es sind unter 100 Dateien, das passt in einen Durchgang (GitHub nimmt im Browser höchstens
   100 auf einmal).
3. Unter Settings → Pages als Quelle „Deploy from a branch“ wählen, Branch `main`, Ordner `/ (root)`.
4. Nach ein bis zwei Minuten ist die Seite erreichbar: beim Repository `BENUTZERNAME.github.io`
   unter `https://BENUTZERNAME.github.io`, bei jedem anderen Namen unter
   `https://BENUTZERNAME.github.io/REPOSITORY/`.

## Später: eigene Domain

Domain unter Settings → Pages eintragen und beim Domain-Anbieter die DNS-Einträge nach der
GitHub-Anleitung setzen. Die Adresse übernimmt die Seite automatisch. Danach in `_config.yml`
`indexierung: true` und `rechtliches: true` setzen.

## Lokale Vorschau (optional)

Braucht Ruby und Bundler:
```
bundle install
bundle exec jekyll serve
```
Dann im Browser `http://localhost:4000` öffnen.
