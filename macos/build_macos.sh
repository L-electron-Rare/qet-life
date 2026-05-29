#!/usr/bin/env bash
# Build natif macOS de QElectroTech (Qt6 + Metal RHI, sans KF6).
# Prérequis : brew install qt cmake ninja extra-cmake-modules
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
cmake --preset macos-metal -S . --fresh
cmake --build --preset macos-metal -j"$(sysctl -n hw.ncpu)"
echo "Binaire : $ROOT/build/macos-metal/qelectrotech"
