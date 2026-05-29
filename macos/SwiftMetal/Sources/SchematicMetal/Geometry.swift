import simd

/// Sommet GPU : position en coordonnées « schéma » (pixels logiques) + couleur RGBA.
public struct Vertex {
    public var position: SIMD2<Float>
    public var color: SIMD4<Float>
    public init(_ x: Float, _ y: Float, _ c: SIMD4<Float>) {
        position = .init(x, y); color = c
    }
}

/// Modèle de schéma : segments (conducteurs) + triangles (blocs pleins).
/// Pensé pour être alimenté par un export JSON depuis QElectroTech
/// (géométrie de la QGraphicsScene), d'où l'intérêt d'une couche Metal native.
public struct SchematicModel {
    public var lineVertices: [Vertex] = []      // paires de sommets (primitive .line)
    public var triangleVertices: [Vertex] = []  // triplets (primitive .triangle)
    public var bounds: SIMD4<Float> = .init(0, 0, 1000, 700) // minX,minY,maxX,maxY

    public init() {}

    /// Couleurs charte CALORIA.
    public static let green: SIMD4<Float> = .init(0.122, 0.557, 0.353, 1)
    public static let red: SIMD4<Float>   = .init(0.824, 0.290, 0.212, 1)
    public static let dark: SIMD4<Float>  = .init(0.106, 0.165, 0.188, 1)

    public mutating func addLine(_ x1: Float, _ y1: Float, _ x2: Float, _ y2: Float, _ c: SIMD4<Float>) {
        lineVertices.append(Vertex(x1, y1, c)); lineVertices.append(Vertex(x2, y2, c))
    }
    public mutating func addRect(_ x: Float, _ y: Float, _ w: Float, _ h: Float, _ c: SIMD4<Float>) {
        let v = [Vertex(x, y, c), Vertex(x+w, y, c), Vertex(x+w, y+h, c),
                 Vertex(x, y, c), Vertex(x+w, y+h, c), Vertex(x, y+h, c)]
        triangleVertices.append(contentsOf: v)
    }

    /// Exemple minimal façon « schéma » (un bus + deux blocs + un conducteur).
    public static func sample() -> SchematicModel {
        var m = SchematicModel()
        m.addRect(80, 300, 160, 90, dark)     // bloc 1
        m.addRect(760, 300, 160, 90, red)     // bloc 2
        m.addLine(50, 200, 950, 200, dark)    // jeu de barres
        m.addLine(240, 345, 760, 345, red)    // conducteur
        m.addLine(160, 200, 160, 300, green)  // descente verte
        return m
    }
}
