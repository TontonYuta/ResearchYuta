#!/usr/bin/env bash
# ==============================================================================
# 🚀 1-Click Research Skills Installer for Antigravity & AI Coding Agents
# ==============================================================================
# Usage:
#   ./install.sh           # Installs (symlinks) skills to ~/.gemini/config/skills
#   ./install.sh --copy    # Copies instead of symlinking
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"
TARGET_DIR="$HOME/.gemini/config/skills"
USE_SYMLINK=true

if [ "$1" == "--copy" ]; then
    USE_SYMLINK=false
fi

echo "=========================================================="
echo "🔬 Installing Research Skills (AI Research & Academic Tools)"
echo "Source: $SKILLS_SRC"
echo "Target: $TARGET_DIR"
echo "=========================================================="

mkdir -p "$TARGET_DIR"

for skill in "$SKILLS_SRC"/*; do
    if [ -d "$skill" ]; then
        skill_name="$(basename "$skill")"
        dest="$TARGET_DIR/$skill_name"
        
        rm -rf "$dest"
        if [ "$USE_SYMLINK" = true ]; then
            ln -s "$skill" "$dest"
            echo "🔗 Symlinked: $skill_name -> $dest"
        else
            cp -r "$skill" "$dest"
            echo "📦 Copied: $skill_name -> $dest"
        fi
    fi
done

echo -e "\n✅ Research skills installed and active!"
