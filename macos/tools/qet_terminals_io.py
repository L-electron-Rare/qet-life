#!/usr/bin/env python3
"""qet_terminals_io — plan de bornier + liste d'E/S API depuis un .qet.
Détecte les borniers (terminal_strip) et les éléments d'API (type contenant 'plc'/'automate'/'io').
Usage: python3 qet_terminals_io.py projet.qet"""
import os, argparse
import xml.etree.ElementTree as ET
def bn(t): return os.path.splitext(os.path.basename((t or '').replace('\\','/')))[0]
def lab(e):
    for ei in e.findall(".//elementInformation"):
        if ei.attrib.get("name")=="label" and (ei.text or "").strip(): return ei.text.strip()
    return ""
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("qet"); a=ap.parse_args()
    root=ET.parse(a.qet).getroot()
    strips=root.findall(".//terminal_strip")+root.findall(".//terminalstrip")
    terms=[e for e in root.findall(".//element") if "born" in bn(e.attrib.get("type")).lower() or "terminal" in bn(e.attrib.get("type")).lower()]
    ios=[e for e in root.findall(".//element") if any(k in bn(e.attrib.get("type")).lower() for k in ("plc","automate","_io","entree","sortie","input","output"))]
    print(f"# Bornier & E/S API — {os.path.basename(a.qet)}\n")
    print(f"## Borniers\n\n- terminal_strip déclarés : {len(strips)}\n- éléments bornes détectés : {len(terms)}\n")
    if terms:
        print("| folio? | repère | type |"); print("| --- | --- | --- |")
        for e in terms[:200]: print(f"| - | {lab(e)} | {bn(e.attrib.get('type'))} |")
    print(f"\n## Entrées/Sorties API\n\n- éléments E/S détectés : {len(ios)}\n")
    if ios:
        print("| repère | type |"); print("| --- | --- |")
        for e in ios[:200]: print(f"| {lab(e)} | {bn(e.attrib.get('type'))} |")
    else:
        print("_(aucun élément API détecté dans ce projet)_")
if __name__=="__main__": main()
