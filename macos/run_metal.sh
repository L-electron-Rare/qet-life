#!/usr/bin/env bash
# Lance QET en forçant le backend Metal de Qt RHI (utile pour les vues accélérées).
export QSG_RHI_BACKEND=metal
export QT_RHI_BACKEND=metal
BIN="$(cd "$(dirname "$0")/.." && pwd)/build/macos-metal/qelectrotech"
exec "$BIN" "$@"
