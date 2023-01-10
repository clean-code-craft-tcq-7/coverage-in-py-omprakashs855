#!/bin/bash
set -e

if grep -q _enter *.md; then
  echo "Replace all text having with your input"
  exit 1
fi
