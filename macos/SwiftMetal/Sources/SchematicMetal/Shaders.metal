// Référence du shader (le Renderer le compile aussi à l'exécution via makeLibrary).
#include <metal_stdlib>
using namespace metal;
struct V { float2 position; float4 color; };
struct VOut { float4 position [[position]]; float4 color; };
struct Uniforms { float4x4 mvp; };
vertex VOut v_main(uint vid [[vertex_id]],
                   const device V* verts [[buffer(0)]],
                   constant Uniforms& u [[buffer(1)]]) {
    VOut o;
    o.position = u.mvp * float4(verts[vid].position, 0.0, 1.0);
    o.color = verts[vid].color;
    return o;
}
fragment float4 f_main(VOut in [[stage_in]]) { return in.color; }
