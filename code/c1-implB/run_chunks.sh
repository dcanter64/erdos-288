#!/bin/bash
# Resumable chunked driver: chunks of 250 in b, claimed in descending
# order via atomic mkdir locks so two workers can share the queue.
# Usage: run_chunks.sh <worker_tag> <max_b>
set -u
cd "$(dirname "$0")"
TAG="$1"; MAXB="${2:-20000}"
mkdir -p outputs locks
nchunks=$(( MAXB / 250 ))
for (( ci = nchunks - 1; ci >= 0; ci-- )); do
  lo=$(( ci * 250 + 1 )); hi=$(( ci * 250 + 250 ))
  out="outputs/chunk_$(printf %04d $lo)_$(printf %04d $hi).json"
  if [ -f "$out" ]; then continue; fi
  if mkdir "locks/chunk_$ci" 2>/dev/null; then
    echo "[$TAG] chunk $ci: b=$lo..$hi start $(date +%T)"
    ./engine "$lo" "$hi" "$out.tmp" && mv "$out.tmp" "$out"
    echo "[$TAG] chunk $ci: done $(date +%T)"
  fi
done
echo "[$TAG] queue drained"
