import AppKit
import MetalKit
import SchematicMetal

let app = NSApplication.shared
app.setActivationPolicy(.regular)

// Modèle : fichier JSON passé en argument, sinon exemple intégré.
var model = SchematicModel.sample()
if CommandLine.arguments.count > 1 {
    let url = URL(fileURLWithPath: CommandLine.arguments[1])
    if let m = try? SchematicModel.load(url) { model = m; print("Schéma chargé : \(url.lastPathComponent)") }
    else { print("Lecture JSON impossible, exemple utilisé.") }
}

let frame = NSRect(x: 0, y: 0, width: 1000, height: 700)
let window = NSWindow(contentRect: frame, styleMask: [.titled, .closable, .resizable],
                      backing: .buffered, defer: false)
window.title = "CALORIA — rendu schéma Metal (fork QET)"
let mtkView = MTKView(frame: frame, device: MTLCreateSystemDefaultDevice())
let renderer = Renderer(mtkView: mtkView, model: model)
mtkView.delegate = renderer
window.contentView = mtkView
window.center(); window.makeKeyAndOrderFront(nil)
app.activate(ignoringOtherApps: true)
app.run()
