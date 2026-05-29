import Foundation
import simd

/// Schéma JSON (format d'échange : à terme exporté par QElectroTech depuis la QGraphicsScene).
struct JRect: Codable { let x, y, w, h: Float; let color: String }
struct JLine: Codable { let x1, y1, x2, y2: Float; let color: String }
struct JSchematic: Codable { let bounds: [Float]; let rects: [JRect]?; let lines: [JLine]? }

func colorNamed(_ s: String) -> SIMD4<Float> {
    switch s {
    case "green": return SchematicModel.green
    case "red":   return SchematicModel.red
    case "blue":  return .init(0.169, 0.498, 0.690, 1)
    default:      return SchematicModel.dark
    }
}

extension SchematicModel {
    /// Charge un schéma depuis un fichier JSON.
    public static func load(_ url: URL) throws -> SchematicModel {
        let data = try Data(contentsOf: url)
        let j = try JSONDecoder().decode(JSchematic.self, from: data)
        var m = SchematicModel()
        if j.bounds.count == 4 { m.bounds = .init(j.bounds[0], j.bounds[1], j.bounds[2], j.bounds[3]) }
        for r in j.rects ?? [] { m.addRect(r.x, r.y, r.w, r.h, colorNamed(r.color)) }
        for l in j.lines ?? [] { m.addLine(l.x1, l.y1, l.x2, l.y2, colorNamed(l.color)) }
        return m
    }
}
