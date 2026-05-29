#!/usr/bin/env python3
"""qet_parts — BOM chiffrée par jointure .qet × catalogue d'articles (style EPLAN parts).
Lecture seule : associe chaque appareil (par repère ou type) à une ligne catalogue CSV
(colonnes: cle, designation, fabricant, reference, prix). Sort une BOM chiffrée MD/CSV.
Usage : python3 qet_parts.py projet.qet --catalog articles.csv [--by label|type] [--csv out.csv]"""
import os, csv, argparse, collections
import xml.etree.ElementTree as ET
def bn(t): return os.path.splitext(os.path.basename((t or '').replace('\\','/')))[0]
def lab(e):
    for ei in e.findall(".//elementInformation"):
        if ei.attrib.get("name")=="label" and (ei.text or "").strip(): return ei.text.strip()
    return ""
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("qet"); ap.add_argument("--catalog",required=True)
    ap.add_argument("--by",choices=["label","type"],default="type"); ap.add_argument("--csv")
    a=ap.parse_args()
    cat={}
    with open(a.catalog,encoding="utf-8") as f:
        for row in csv.DictReader(f): cat[(row.get("cle") or "").strip()]=row
    root=ET.parse(a.qet).getroot()
    IGNORE=("folio","renvoi","nomenclatur","spec_cablage","cartouche")
    keycount=collections.Counter()
    for e in root.findall(".//element"):
        t=bn(e.attrib.get("type"))
        if any(k in t.lower() for k in IGNORE): continue
        key = lab(e) if a.by=="label" else t
        if key: keycount[key]+=1
    rows=[]; total=0.0
    for key,qte in keycount.most_common():
        c=cat.get(key,{})
        prix=float(c.get("prix","0") or 0); sous=prix*qte; total+=sous
        rows.append({"clé":key,"qté":qte,"désignation":c.get("designation",""),
                     "fabricant":c.get("fabricant",""),"référence":c.get("reference",""),
                     "PU":f"{prix:.2f}","total":f"{sous:.2f}"})
    cols=["clé","qté","désignation","fabricant","référence","PU","total"]
    print(f"# BOM chiffrée — {os.path.basename(a.qet)} (jointure sur {a.by})\n")
    print("| "+" | ".join(cols)+" |"); print("| "+" | ".join("---" for _ in cols)+" |")
    for r in rows: print("| "+" | ".join(str(r[k]) for k in cols)+" |")
    print(f"\n**Total estimé : {total:.2f} €**")
    if a.csv:
        with open(a.csv,"w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
if __name__=="__main__": main()
