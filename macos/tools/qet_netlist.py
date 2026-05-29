#!/usr/bin/env python3
"""qet_netlist — liste des connexions (netlist) depuis un .qet.
Pour chaque conducteur : folio, num, de (élément/borne) -> vers (élément/borne), couleur, section.
Usage: python3 qet_netlist.py projet.qet [--csv sortie.csv]"""
import sys, os, csv, argparse
import xml.etree.ElementTree as ET

def bn(t): return os.path.splitext(os.path.basename((t or '').replace('\\','/')))[0]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("qet"); ap.add_argument("--csv")
    a=ap.parse_args(); root=ET.parse(a.qet).getroot()
    rows=[]
    for i,d in enumerate(root.findall("diagram"),1):
        # index élément par uuid -> repère/type
        elem={}
        for e in d.findall(".//element"):
            lab=""
            for ei in e.findall(".//elementInformation"):
                if ei.attrib.get("name")=="label" and (ei.text or "").strip(): lab=ei.text.strip()
            elem[e.attrib.get("uuid")]= lab or bn(e.attrib.get("type"))
        for c in d.findall(".//conductor"):
            ca=c.attrib
            rows.append({"folio":i,"num":ca.get("num",""),
                         "borne1":ca.get("terminal1",""),"borne2":ca.get("terminal2",""),
                         "couleur":ca.get("conductor_color",""),"section":ca.get("conductor_section",""),
                         "fonction":ca.get("function",""),"câble":ca.get("cable",""),"type":ca.get("type","")})
    cols=["folio","num","borne1","borne2","couleur","section","fonction","câble","type"]
    print(f"# Netlist — {os.path.basename(a.qet)} ({len(rows)} connexions)\n")
    print("| "+" | ".join(cols)+" |"); print("| "+" | ".join("---" for _ in cols)+" |")
    for r in rows: print("| "+" | ".join(str(r.get(k,"")) for k in cols)+" |")
    if a.csv:
        with open(a.csv,"w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
        print(f"\nCSV: {a.csv}", file=sys.stderr)
if __name__=="__main__": main()
