import AppKit
import MetalKit
import SchematicMetal

let app = NSApplication.shared
app.setActivationPolicy(.regular)

let frame = NSRect(x: 0, y: 0, width: 1000, height: 700)
let window = NSWindow(contentRect: frame, styleMask: [.titled, .closable, .resizable],
                      backing: .buffered, defer: false)
window.title = "CALORIA — rendu schéma Metal (PoC, fork QET)"

let mtkView = MTKView(frame: frame, device: MTLCreateSystemDefaultDevice())
mtkView.enableSetNeedsDisplay = true
let renderer = Renderer(mtkView: mtkView, model: .sample())
mtkView.delegate = renderer
window.contentView = mtkView
window.center(); window.makeKeyAndOrderFront(nil)
app.activate(ignoringOtherApps: true)
app.run()
