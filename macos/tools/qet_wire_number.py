#!/usr/bin/env python3
"""qet_wire_number — numérotation automatique des conducteurs d'un .qet (style SEE/EPLAN).
Attribue un numéro aux conducteurs sans numéro. Préserve le format (édition ciblée) + sauvegarde .bak.
Schémas : --scheme global (1,2,3...) ou folio (F1-1, F1-2...). --force renumérote tout.
Usage : python3 qet_wire_number.py projet.qet [--scheme folio|global] [--force] [--prefix N]"""
import re, sys, os, argparse, shutil
import xml.etree.ElementTree as ET

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("qet")
    ap.add_argument("--scheme",choices=["global","folio"],default="folio")
    ap.add_argument("--force",action="store_true"); ap.add_argument("--prefix",default="")
    a=ap.parse_args()
    txt=open(a.qet,encoding="utf-8").read()
    # bornes de folios (offsets des <diagram )
    dia_pos=[m.start() for m in re.finditer(r'<diagram\b', txt)]
    def folio_of(pos):
        f=0
        for p in dia_pos:
            if p<=pos: f+=1
            else: break
        return max(f,1)
    counters={}; gcount=0; changed=0
    def repl(m):
        nonlocal gcount,changed
        tag=m.group(0); pos=m.start()
        cur=re.search(r'\bnum="([^"]*)"',tag)
        has=cur and cur.group(1).strip()
        if has and not a.force: return tag
        f=folio_of(pos)
        if a.scheme=="folio":
            counters[f]=counters.get(f,0)+1; val=f"{a.prefix}F{f}-{counters[f]}"
        else:
            gcount+=1; val=f"{a.prefix}{gcount}"
        changed+=1
        if cur: return tag[:cur.start()]+f'num="{val}"'+tag[cur.end():]
        return tag[:-1]+f' num="{val}">'
    new=re.sub(r'<conductor\b[^>]*>', repl, txt)
    # validation : XML bien formé
    try: ET.fromstring(new)
    except ET.ParseError as e:
        print("ERREUR: XML invalide après édition, abandon:",e); sys.exit(1)
    shutil.copyfile(a.qet, a.qet+".bak")
    open(a.qet,"w",encoding="utf-8").write(new)
    print(f"OK : {changed} conducteurs numérotés (schéma {a.scheme}). Sauvegarde : {os.path.basename(a.qet)}.bak")
if __name__=="__main__": main()
