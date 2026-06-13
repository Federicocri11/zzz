// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "Zzz",
    platforms: [.macOS(.v12)],
    targets: [
        .executableTarget(name: "Zzz", path: "Sources")
    ]
)
