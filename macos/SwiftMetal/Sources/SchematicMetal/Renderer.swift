import MetalKit
import simd

struct Uniforms { var mvp: simd_float4x4 }

public final class Renderer: NSObject, MTKViewDelegate {
    let device: MTLDevice
    let queue: MTLCommandQueue
    var pipeline: MTLRenderPipelineState!
    var lineBuffer: MTLBuffer?
    var triBuffer: MTLBuffer?
    var lineCount = 0, triCount = 0
    var model: SchematicModel

    static let shaderSource = """
    #include <metal_stdlib>
    using namespace metal;
    struct V { float2 position; float4 color; };
    struct VOut { float4 position [[position]]; float4 color; };
    struct Uniforms { float4x4 mvp; };
    vertex VOut v_main(uint vid [[vertex_id]], const device V* verts [[buffer(0)]], constant Uniforms& u [[buffer(1)]]) {
        VOut o; o.position = u.mvp * float4(verts[vid].position, 0.0, 1.0); o.color = verts[vid].color; return o;
    }
    fragment float4 f_main(VOut in [[stage_in]]) { return in.color; }
    """

    public init?(mtkView: MTKView, model: SchematicModel) {
        guard let dev = mtkView.device ?? MTLCreateSystemDefaultDevice(),
              let q = dev.makeCommandQueue() else { return nil }
        self.device = dev; self.queue = q; self.model = model
        super.init()
        mtkView.device = dev
        mtkView.clearColor = MTLClearColor(red: 0.969, green: 0.957, blue: 0.941, alpha: 1) // crème
        do {
            let lib = try dev.makeLibrary(source: Renderer.shaderSource, options: nil)
            let d = MTLRenderPipelineDescriptor()
            d.vertexFunction = lib.makeFunction(name: "v_main")
            d.fragmentFunction = lib.makeFunction(name: "f_main")
            d.colorAttachments[0].pixelFormat = mtkView.colorPixelFormat
            pipeline = try dev.makeRenderPipelineState(descriptor: d)
        } catch { print("Metal pipeline error: \(error)"); return nil }
        upload()
    }

    func upload() {
        let lv = model.lineVertices, tv = model.triangleVertices
        lineCount = lv.count; triCount = tv.count
        if lineCount > 0 { lineBuffer = device.makeBuffer(bytes: lv, length: MemoryLayout<Vertex>.stride*lineCount) }
        if triCount > 0 { triBuffer = device.makeBuffer(bytes: tv, length: MemoryLayout<Vertex>.stride*triCount) }
    }

    func mvp() -> simd_float4x4 {
        let b = model.bounds // minX,minY,maxX,maxY
        let sx = 2/(b.z-b.x), sy = -2/(b.w-b.y)
        let tx = -(b.z+b.x)/(b.z-b.x), ty = (b.w+b.y)/(b.w-b.y)
        return simd_float4x4(columns: (SIMD4(sx,0,0,0), SIMD4(0,sy,0,0), SIMD4(0,0,1,0), SIMD4(tx,ty,0,1)))
    }

    public func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {}

    public func draw(in view: MTKView) {
        guard let rpd = view.currentRenderPassDescriptor,
              let drawable = view.currentDrawable,
              let cb = queue.makeCommandBuffer(),
              let enc = cb.makeRenderCommandEncoder(descriptor: rpd) else { return }
        var u = Uniforms(mvp: mvp())
        enc.setRenderPipelineState(pipeline)
        enc.setVertexBytes(&u, length: MemoryLayout<Uniforms>.stride, index: 1)
        if let tb = triBuffer, triCount > 0 {
            enc.setVertexBuffer(tb, offset: 0, index: 0)
            enc.drawPrimitives(type: .triangle, vertexStart: 0, vertexCount: triCount)
        }
        if let lb = lineBuffer, lineCount > 0 {
            enc.setVertexBuffer(lb, offset: 0, index: 0)
            enc.drawPrimitives(type: .line, vertexStart: 0, vertexCount: lineCount)
        }
        enc.endEncoding(); cb.present(drawable); cb.commit()
    }
}
