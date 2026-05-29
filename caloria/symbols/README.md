# Symboles CALORIA (qet-life)

Collection de symboles QElectroTech spécifiques à CALORIA :
nœud GPU, CDU, échangeur, PAC eau/eau, dry-cooler, digesteur, onduleur/UPS, batterie LFP.

## Utilisation dans QElectroTech
La collection commune (`elements/`) est un sous-module pointant vers l'upstream qelectrotech-elements,
donc on versionne ces symboles ici, dans le dépôt parent.

Pour que QET les charge, au choix :
- copier/lier `80_caloria/` dans le dossier `elements/` à côté du binaire
  (le build macOS lie déjà `elements/` → la collection ; `cp -R caloria/symbols/80_caloria elements/`),
- ou les définir comme **collection personnelle** via le réglage QSettings
  `elements-collections/common-collection-path` ou le dossier custom de QET.

Format : `.elmt` (XML) — rectangle + bornes (terminaux) + libellé dynamique (`label`).
