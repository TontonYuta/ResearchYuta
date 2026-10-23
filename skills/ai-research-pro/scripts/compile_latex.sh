#!/usr/bin/env bash
# Quick helper to compile Vietnamese LaTeX with pdflatex non-interactively
if [ -z "$1" ]; then
    echo "Usage: ./compile_latex.sh <path_to_file.tex>"
    exit 1
fi

TEX_FILE="$1"
DIR=$(dirname "$TEX_FILE")
BASE=$(basename "$TEX_FILE")

cd "$DIR" || exit 1
echo "Compiling $BASE with pdflatex (Pass 1)..."
pdflatex -interaction=nonstopmode "$BASE" > /dev/null 2>&1
echo "Compiling $BASE with pdflatex (Pass 2 for outlines and links)..."
pdflatex -interaction=nonstopmode "$BASE" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    PDF_NAME="${BASE%.tex}.pdf"
    rm -f "${BASE%.tex}.aux" "${BASE%.tex}.log" "${BASE%.tex}.out" "${BASE%.tex}.toc" "${BASE%.tex}.synctex.gz"
    echo "✅ Successfully generated: $DIR/$PDF_NAME (Cleaned intermediate build files)"
else
    echo "❌ Compilation failed. Check the .log file in $DIR."
    exit 1
fi
