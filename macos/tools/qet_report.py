#!/usr/bin/env python3
"""
qet_report — rapports automatiques type SEE Electrical / EPLAN à partir d'un projet QElectroTech (.qet).
Génère : liste d'appareils (BOM), liste de fils (conducteurs), liste des folios.
Sorties : Markdown (stdout) + CSV (--csv-dir).
Usage : python3 qet_report.py projet.qet [--csv-dir DIR]
"""
import sys, os, csv, argparse, collections
import xml.etree.ElementTree as ET

def basename_type(t):
    t = t or ""
    return os.path.splitext(os.path.basename(t.replace("\\","/")))[0]

def parse(path, include_all=False):
    root = ET.parse(path).getroot()
    project_title = root.attrib.get("title","")
    folios, devices, wires = [], [], []
    info_fields = set()
    for i, dia in enumerate(root.findall("diagram"), 1):
        ftitle = dia.attrib.get("title","")
        folios.append({"folio": i, "titre": ftitle, "auteur": dia.attrib.get("author",""),
                       "date": dia.attrib.get("date","")})
        for el in dia.findall(".//element"):
            info = {}
            for ei in el.findall(".//elementInformation"):
                n = ei.attrib.get("name"); v = (ei.text or "").strip()
                if n and v: info[n] = v; info_fields.add(n)
            label = info.get("label","")
            etype = basename_type(el.attrib.get("type",""))
            IGNORE = ("folio","renvoi","nomenclatur","spec_cablage","cartouche")
            if (not include_all) and any(k in etype.lower() for k in IGNORE):
                continue
            if not label and not info:
                continue
            row = {"folio": i, "repère": label, "type": etype}
            row.update(info)
            devices.append(row)
        for c in dia.findall(".//conductor"):
            a = c.attrib
            wires.append({"folio": i, "num": a.get("num",""), "type": a.get("type",""),
                          "couleur": a.get("conductor_color",""), "section": a.get("conductor_section",""),
                          "fonction": a.get("function",""), "câble": a.get("cable",""),
                          "phase": a.get("phase",""), "terre": a.get("ground",""),
                          "borne1": a.get("terminal1",""), "borne2": a.get("terminal2","")})
    return project_title, folios, devices, wires, sorted(info_fields)

def md_table(rows, cols):
    if not rows: return "_(vide)_\n"
    out = "| " + " | ".join(cols) + " |\n| " + " | ".join("---" for _ in cols) + " |\n"
    for r in rows:
        out += "| " + " | ".join(str(r.get(c,"")) for c in cols) + " |\n"
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qet"); ap.add_argument("--csv-dir", default=None); ap.add_argument("--all", action="store_true", help="inclure renvois/nomenclatures")
    args = ap.parse_args()
    title, folios, devices, wires, info_fields = parse(args.qet, args.all)
    # colonnes BOM : repère/type + champs article rencontrés
    dev_cols = ["folio","repère","type"] + [f for f in info_fields if f != "label"]
    bom = collections.Counter((d.get("type",""),) for d in devices)
    print(f"# Rapports projet — {title or os.path.basename(args.qet)}\n")
    print(f"Source : `{os.path.basename(args.qet)}` · {len(folios)} folios · "
          f"{len(devices)} appareils · {len(wires)} conducteurs\n")
    print("## 1. Folios\n"); print(md_table(folios, ["folio","titre","auteur","date"]))
    print("\n## 2. Liste d'appareils (BOM)\n"); print(md_table(devices, dev_cols))
    print("\n## 3. Synthèse appareils par type\n")
    print(md_table([{"type":t[0],"quantité":n} for t,n in bom.most_common()], ["type","quantité"]))
    print("\n## 4. Liste de fils (conducteurs)\n")
    print(md_table(wires, ["folio","num","type","couleur","section","fonction","câble","borne1","borne2"]))
    if args.csv_dir:
        os.makedirs(args.csv_dir, exist_ok=True)
        def dump(name, rows, cols):
            with open(os.path.join(args.csv_dir,name),"w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f, fieldnames=cols); w.writeheader()
                for r in rows: w.writerow({k:r.get(k,"") for k in cols})
        dump("folios.csv", folios, ["folio","titre","auteur","date"])
        dump("appareils_bom.csv", devices, dev_cols)
        dump("fils.csv", wires, ["folio","num","type","couleur","section","fonction","câble","borne1","borne2"])
        print(f"\nCSV écrits dans : {args.csv_dir}", file=sys.stderr)

if __name__ == "__main__":
    main()
