#!/usr/bin/env bash
# MESO Install Script
# Symbiont Systems LLC — https://symbiont.systems
#
# Installs the MESO colony into ~/.claude/
# Zooids and genome are symlinked (auto-update on git pull).
# Stolon and pneumatophore are copied (personal, you customize them).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
RULES_DIR="$CLAUDE_DIR/rules"

echo "MESO: Modular Exosymbiotic Organelle"
echo "Installing colony into $CLAUDE_DIR"
echo ""

# Create directories
mkdir -p "$RULES_DIR"

# --- Symlinked files (auto-update on git pull) ---

# Genome
if [ -L "$CLAUDE_DIR/STANDING-ORDERS.md" ] || [ ! -e "$CLAUDE_DIR/STANDING-ORDERS.md" ]; then
    ln -sf "$SCRIPT_DIR/STANDING-ORDERS.md" "$CLAUDE_DIR/STANDING-ORDERS.md"
    echo "  [symlink] STANDING-ORDERS.md (genome)"
else
    echo "  [skip]    STANDING-ORDERS.md exists and is not a symlink — not overwriting"
fi

# Zooids (01-10)
for zooid in "$SCRIPT_DIR"/zooids/*.md; do
    name="$(basename "$zooid")"
    target="$RULES_DIR/$name"
    if [ -L "$target" ] || [ ! -e "$target" ]; then
        ln -sf "$zooid" "$target"
        echo "  [symlink] rules/$name"
    else
        echo "  [skip]    rules/$name exists and is not a symlink — not overwriting"
    fi
done

# --- Copied files (personal, customize these) ---

# Pneumatophore
if [ ! -e "$CLAUDE_DIR/CLAUDE.md" ]; then
    cp "$SCRIPT_DIR/templates/CLAUDE.md.template" "$CLAUDE_DIR/CLAUDE.md"
    echo "  [copy]    CLAUDE.md (pneumatophore) — customize this"
else
    echo "  [skip]    CLAUDE.md already exists — not overwriting"
fi

# Stolon
if [ ! -e "$RULES_DIR/00-operator.md" ]; then
    cp "$SCRIPT_DIR/templates/00-operator.template.md" "$RULES_DIR/00-operator.md"
    echo "  [copy]    rules/00-operator.md (stolon) — customize this"
else
    echo "  [skip]    rules/00-operator.md already exists — not overwriting"
fi

echo ""
echo "Colony installed."
echo ""
echo "Next steps:"
echo "  1. Edit ~/.claude/CLAUDE.md with your identity and authorship info"
echo "  2. Edit ~/.claude/rules/00-operator.md with your background and traits"
echo "  3. Start a Claude Code session — the colony loads automatically"
echo ""
echo "The zooids and genome are symlinked to this repo."
echo "Run 'git pull' to receive updates. Your personal files won't be touched."
