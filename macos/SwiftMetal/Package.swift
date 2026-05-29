// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "SchematicMetal",
    platforms: [.macOS(.v13)],
    products: [
        .library(name: "SchematicMetal", targets: ["SchematicMetal"]),
        .executable(name: "schematic-metal-demo", targets: ["SchematicMetalDemo"])
    ],
    targets: [
        .target(name: "SchematicMetal", exclude: ["Shaders.metal"]),
        .executableTarget(name: "SchematicMetalDemo", dependencies: ["SchematicMetal"])
    ]
)
