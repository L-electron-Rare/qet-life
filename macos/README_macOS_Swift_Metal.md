# QElectroTech — config macOS Swift/Metal (fork CALORIA)

Objectif du fork : une variante **macOS native** de QElectroTech, avec un chemin de rendu
**accéléré Metal** et une couche **Swift**, pour fluidifier l'affichage des grands schémas.

## Contenu
- `CMakePresets.json` — preset `macos-metal` : build Qt6, dépendances KDE (KF6) désactivées,
  correctifs des chemins d'install macOS, générateur Ninja.
- `build_macos.sh` — build en une commande (`cmake --preset macos-metal` puis build).
- `run_metal.sh` — lance QET en forçant le backend **Metal** de Qt RHI
  (`QSG_RHI_BACKEND=metal`, `QT_RHI_BACKEND=metal`).
- `SwiftMetal/` — **proof-of-concept Swift/Metal** : un renderer MetalKit qui dessine des
  primitives de schéma (conducteurs = lignes, blocs = triangles) sur GPU.

## Pourquoi Swift/Metal
QElectroTech est en C++/Qt et rend ses schémas via `QGraphicsView` (raster CPU, `QPainter`).
Sur de très grands folios, le rafraîchissement/zoom devient coûteux. Deux pistes d'accélération
macOS-native, posées ici en socle :
1. **Qt RHI Metal** : activer le backend Metal de Qt (utile pour les composants RHI/Quick) — `run_metal.sh`.
2. **Couche de rendu Metal dédiée** : remplacer le viewport `QGraphicsView` par un rendu
   `QRhiWidget` (Qt ≥ 6.7, backend Metal) **ou** une vue MetalKit pilotée en Swift, alimentée par
   la géométrie de la scène exportée (lignes/rectangles/textes). C'est l'objet du PoC `SwiftMetal/`.

## Le PoC Swift/Metal
```bash
cd SwiftMetal
swift run schematic-metal-demo     # ouvre une fenêtre, rend un schéma d'exemple en Metal
```
- `Geometry.swift` : modèle (`SchematicModel`) — segments + triangles, couleurs charte CALORIA,
  pensé pour être alimenté par un **export JSON** de la `QGraphicsScene` de QET.
- `Renderer.swift` : `MTKViewDelegate` — pipeline Metal, projection orthographique
  schéma→écran, dessin des lignes et triangles. Shader compilé au runtime.
- `Shaders.metal` : référence du shader (vertex/fragment).

## Plan d'intégration (roadmap)
1. **Export géométrie** : ajouter à QET un export de la scène (folio) en JSON
   (primitives + couleurs + transform).
2. **Vue Metal** : intégrer la vue MetalKit (ce PoC) comme viewport alternatif, ou via `QRhiWidget`.
3. **Picking & interactions** : remonter les hit-tests GPU→modèle pour l'édition.
4. **Bench** : comparer rafraîchissement/zoom CPU (QGraphicsView) vs GPU (Metal) sur un gros folio.

## Build macOS de QET
```bash
brew install qt cmake ninja extra-cmake-modules
./build_macos.sh        # binaire : build/macos-metal/qelectrotech
./run_metal.sh          # lancement avec backend Metal
```
> Note : le build complet QET sur macOS reste sensible aux dépendances ; ce preset désactive
> KF6 et corrige les chemins d'install pour aboutir. À affiner selon l'environnement.
