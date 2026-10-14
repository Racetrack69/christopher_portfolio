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
| `assets/images/vorschau/` | Vorschaubilder für Link-Vorschauen (1200 × 630 px) |
| `robots.txt` | Regeln für Suchmaschinen und KI-Crawler |
| `_config.yml` | Name, Adresse, Kontakt, Hängung, Suchmaschinen |
| `tools/bilder.py` | Bereitet Exporte für die Seite vor |

## Ein Bild austauschen oder hinzufügen

1. **Exportieren** (Lightroom, Capture One o. ä.): JPEG oder TIFF, sRGB, lange Kante mindestens 2400 px,
   Standortinformationen entfernen.
2. **Vorbereiten:**
   ```
   python3 tools/bilder.py ~/Export/kyoto.jpg --serie japan --name kyoto-torii --format 6x6
   ```
   `--format` ist `6x45`, `6x6`, `6x7`, `6x9` oder `kb` (das Aufnahmeformat, auch bei beschnittenen Bildern). Bei 3:2 ist die Angabe nötig, weil 6×9 und Kleinbild
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
z. B. `island.md` → `/serien/island/`), `title`, `kurz` (eine Zeile für die Startseite),
`reihenfolge` und Bilder anpassen. Den Text oben auf der Startseite ändert man in `_config.yml`
unter `einleitung`.

## Journal-Beitrag

Datei `_posts/JJJJ-MM-TT-titel.md` anlegen:

```
---
title: Titel des Beitrags
description: Ein Satz, worum es geht (erscheint in der Liste und bei Google).
---
Text in Markdown …
```

Bilder für Beiträge liegen in `assets/images/journal/`. Vorbereiten wie Serienbilder, nur mit
`--serie journal`. Das Skript gibt dann die fertige Zeile für den Beitrag aus:

```
python3 tools/bilder.py ~/Export/kamera.jpg --serie journal --name rolleiflex-oben
```

Ein Bild im Text:
`{% include beitragsbild.html serie="journal" datei="rolleiflex-oben" w="1600" h="900" alt="…" text="Bildunterschrift" %}`

Zwei Hochformate nebeneinander (auch am Handy):

```
<div class="paar">
{% include beitragsbild.html serie="journal" datei="bild-a" w="900" h="1600" alt="…" text="…" %}
{% include beitragsbild.html serie="journal" datei="bild-b" w="1066" h="1600" alt="…" text="…" %}
</div>
```

Entwürfe kommen ohne Datum in `_drafts/` und erscheinen nicht auf der Seite. Zum Veröffentlichen
nach `_posts/` verschieben und das Datum vorne an den Dateinamen setzen.

## Einstellungen in `_config.yml`

- Die Adresse der Seite setzt GitHub automatisch, auch später mit eigener Domain. `url` und
  `baseurl` deshalb nicht eintragen
- `author.email`: erscheint in Impressum und Datenschutzerklärung, sobald eingetragen. Erst
  eintragen, wenn das Postfach funktioniert
- `author.instagram`: wird in den strukturierten Daten mit der Person verknüpft
- `anschrift`: Straße und Ort für Impressum und Datenschutzerklärung
- `haengung`: `reihen`, `raster` oder `einzeln` (nur Desktop, am Handy immer eine Spalte)
- `bildgroesse`: lange Kante der Bilder in Pixel (Standard 1600). Nach einer Änderung alle Bilder
  mit `tools/bilder.py` neu erzeugen
- `indexierung`: `true` = die Seite darf in Suchmaschinen erscheinen (seit 14.10.2026). `false` setzt
  auf allen Seiten „noindex“. Impressum, Datenschutz und 404 bleiben immer „noindex“
- `og_bild`: Vorschaubild für Seiten ohne eigenes Bild. Ideal 1200 × 630 px
- KI: In `robots.txt` sind Suchmaschinen und KI-Suche erlaubt, KI-Training (GPTBot, ClaudeBot,
  Google-Extended) ist gesperrt. Das ist eine Bitte, die diese Anbieter nach eigenen Angaben beachten,
  kein technischer Schutz
- `rechtliches`: `true` blendet die Links zu Impressum und Datenschutz im Fußbereich ein.
  Die Texte liegen in `impressum.html` und `datenschutz.html`

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

## Änderungen hochladen (Update-Pakete)

Nach dem ersten Upload muss nie wieder alles hochgeladen werden, nur was sich geändert hat.

1. Update-Paket entpacken. Darin liegen der Ordner `hochladen` und die Datei `LIESMICH.txt`.
2. Auf GitHub „Add file → Upload files“ und den **Inhalt** des Ordners `hochladen` hineinziehen
   (also z. B. `_serien` und `assets`, nicht den Ordner `hochladen` selbst). GitHub legt die
   Dateien an die richtige Stelle und überschreibt vorhandene mit gleichem Namen.
3. Was gelöscht werden soll, steht in `LIESMICH.txt`. Hochladen löscht nichts. Löschen geht auf
   GitHub über die Datei, dann oben rechts „…“ → „Delete file“. Dateien, die dort als „kann weg“
   markiert sind, stören nicht, wenn sie liegen bleiben.

## Eigene Domain

Die Seite läuft unter `https://christopherschmidtke.de` (Domain bei INWX, HTTPS über GitHub).

- Die Datei `CNAME` im Repository gehört zur Domain. Nicht löschen.
- Bei INWX stehen: vier A-Einträge auf die GitHub-Adressen, ein CNAME `www` auf
  `racetrack69.github.io.` und ein TXT-Eintrag `_github-pages-challenge-racetrack69` für die
  Verifizierung bei GitHub. Alle stehen lassen, NS- und SOA-Einträge ebenfalls.
- Wenn die Seite gefunden werden soll: in `_config.yml` `indexierung: true` setzen.

## Lokale Vorschau (optional)

Braucht Ruby und Bundler:
```
bundle install
bundle exec jekyll serve
```
Dann im Browser `http://localhost:4000` öffnen.
