#!/usr/bin/env python3
"""Bereitet exportierte Fotos für die Website vor.

Pro Bild entsteht eine Datei: assets/images/<serie>/<name>.jpg
Die lange Kante steht in _config.yml unter "bildgroesse" (Standard 1600 px).

Alle Metadaten werden entfernt, auch GPS-Daten. Gesetzt werden nur Urheber und
Copyright. Am Ende steht der Eintrag für die Serien-Datei.

Beispiele:
  python3 tools/bilder.py ~/Export/kyoto.jpg --serie japan --name kyoto-torii --format 6x6
  python3 tools/bilder.py ~/Export/japan/*.jpg --serie japan --format 6x9

Voraussetzung: Python 3 und Pillow (python3 -m pip install Pillow)
"""
import argparse
import datetime
import io
import re
import sys
import unicodedata
from pathlib import Path

try:
    from PIL import Image, ImageCms, ImageOps
except ImportError:
    sys.exit("Pillow fehlt. Installation: python3 -m pip install Pillow")

QUALITAET = 88
AUTOR = "Christopher Schmidtke"
ROOT = Path(__file__).resolve().parent.parent
GPS_IFD = 0x8825


def bildgroesse():
    """Liest "bildgroesse" aus _config.yml, sonst 1600."""
    try:
        text = (ROOT / "_config.yml").read_text(encoding="utf-8")
        m = re.search(r"^bildgroesse:\s*(\d+)", text, re.M)
        return int(m.group(1)) if m else 1600
    except OSError:
        return 1600


def slug(text):
    text = text.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(a, b)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "bild"


def nach_srgb(im):
    """Bringt das Bild nach RGB/sRGB. Gibt (Bild, ICC-Bytes) zurück."""
    ziel = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
    icc = im.info.get("icc_profile")
    if icc:
        try:
            quelle = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            name = ImageCms.getProfileDescription(quelle) or ""
            if "srgb" not in name.lower():
                im = ImageCms.profileToProfile(im, quelle, ziel, outputMode="RGB")
                print(f"  Farbprofil „{name.strip()}“ nach sRGB umgerechnet")
        except Exception as fehler:  # defektes Profil: einfach umwandeln
            print(f"  Hinweis: Farbprofil nicht lesbar ({fehler}), wandle ohne Profil um")
    if im.mode != "RGB":
        im = im.convert("RGB")
    return im, ziel.tobytes()


# Typische Seitenverhältnisse der Filmformate (lange : kurze Seite)
TYPISCH = {"6x45": (1.333, 1.35), "6x6": (1.0,), "6x7": (1.167, 1.24), "6x9": (1.5,), "kb": (1.5,)}


def format_raten(w, h, vorgabe):
    verhaeltnis = max(w, h) / min(w, h)
    if vorgabe:
        if not any(abs(verhaeltnis - t) < 0.03 for t in TYPISCH[vorgabe]):
            print(f"  Hinweis: Seitenverhältnis {verhaeltnis:.2f} ist für {vorgabe} untypisch (beschnitten?). Format bleibt {vorgabe}.")
        return vorgabe
    if abs(verhaeltnis - 1) < 0.02:
        return "6x6"
    if abs(verhaeltnis - 1.5) < 0.03:
        return "6x9 oder kb"
    if any(abs(verhaeltnis - t) < 0.03 for t in TYPISCH["6x7"]):
        return "6x7"
    if any(abs(verhaeltnis - t) < 0.02 for t in TYPISCH["6x45"]):
        return "6x45"
    print(f"  Hinweis: Seitenverhältnis {verhaeltnis:.2f} passt zu keinem Filmformat (beschnitten?). Bitte --format angeben.")
    return "?"


def verarbeiten(quelle, serie, name, vorgabe_format, autor, groesse_px):
    im = Image.open(quelle)
    exif_alt = im.getexif()
    gps = exif_alt.get_ifd(GPS_IFD) if exif_alt else {}
    im = ImageOps.exif_transpose(im)  # Ausrichtung übernehmen, bevor die Metadaten wegfallen
    im, icc = nach_srgb(im)

    w, h = im.size
    lang = max(w, h)
    if lang < groesse_px:
        print(f"  ACHTUNG: lange Kante nur {lang} px (Ziel {groesse_px} px). Das Bild wird nicht vergrößert")
        print(f"           und kann auf großen Bildschirmen weich wirken. Besser neu exportieren.")
        groesse_px = lang

    faktor = groesse_px / lang
    neu = (round(w * faktor), round(h * faktor))
    bild = im if neu == im.size else im.resize(neu, Image.LANCZOS)

    exif = Image.Exif()
    exif[0x013B] = autor                                                  # Artist
    exif[0x8298] = f"Copyright {datetime.date.today().year} {autor}"       # Copyright

    ziel = ROOT / "assets" / "images" / serie
    ziel.mkdir(parents=True, exist_ok=True)
    datei = ziel / f"{name}.jpg"
    bild.save(datei, "JPEG", quality=QUALITAET, optimize=True, progressive=True,
              icc_profile=icc, exif=exif.tobytes())
    print(f"  {neu[0]} × {neu[1]} px, {datei.stat().st_size // 1024} KB")

    fmt = format_raten(w, h, vorgabe_format)
    if gps:
        print("  ACHTUNG: Das Original enthielt GPS-Daten. In der Web-Datei sind sie entfernt.")
        print("           Tipp: im Export-Preset „Standortinformationen entfernen“ aktivieren.")
    return {"datei": name, "format": fmt, "w": neu[0], "h": neu[1]}


def main():
    ap = argparse.ArgumentParser(description="Fotos für die Website vorbereiten (eine Größe, ohne Metadaten).")
    ap.add_argument("dateien", nargs="+", help="exportierte Bilddateien (JPEG oder TIFF)")
    ap.add_argument("--serie", required=True, help="Ordnername der Serie, z. B. japan")
    ap.add_argument("--name", help="Dateiname ohne Endung (nur bei einer Datei). Standard: aus dem Dateinamen")
    ap.add_argument("--format", choices=sorted(TYPISCH), help="Filmformat (Aufnahmeformat, auch bei beschnittenen Bildern). Nötig bei 3:2, weil 6×9 und Kleinbild gleich proportioniert sind")
    ap.add_argument("--autor", default=AUTOR)
    args = ap.parse_args()

    if args.name and len(args.dateien) > 1:
        sys.exit("--name geht nur bei einer einzelnen Datei.")

    groesse_px = bildgroesse()
    eintraege = []
    for pfad in args.dateien:
        quelle = Path(pfad).expanduser()
        if not quelle.is_file():
            print(f"{quelle}: nicht gefunden")
            continue
        name = slug(args.name or quelle.stem)
        print(f"{quelle.name} → assets/images/{slug(args.serie)}/{name}.jpg")
        eintrag = verarbeiten(quelle, slug(args.serie), name, args.format, args.autor, groesse_px)
        if eintrag:
            eintraege.append(eintrag)

    if not eintraege:
        return
    if slug(args.serie) == "journal":
        print("\nIm Beitrag an der passenden Stelle einfügen, alt und text ergänzen:\n")
        for e in eintraege:
            print(f'{{% include beitragsbild.html serie="journal" datei="{e["datei"]}" w="{e["w"]}" h="{e["h"]}" alt="" text="" %}}')
        return
    print("\nIn _serien/" + slug(args.serie) + ".md unter „bilder:“ einfügen und ergänzen:\n")
    for e in eintraege:
        print(f"  - datei: {e['datei']}")
        print(f"    format: {e['format']}")
        print(f"    w: {e['w']}")
        print(f"    h: {e['h']}")
        print('    ort: ""')
        print('    jahr: ""')
        print('    kamera: ""')
        print('    film: ""')
        print('    alt: ""   # in einem Satz: was ist zu sehen?')


if __name__ == "__main__":
    main()
