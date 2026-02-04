#!/usr/bin/env bash
# MESO Install Script (Spore)
# Symbiont Systems LLC — https://symbiont.systems
#
# Installs the MESO colony into ~/.claude/
# Zooids and genome are symlinked (auto-update on git pull).
# Operons are symlinked into ~/.claude/skills/ (trigger-activated).
# Stolon and pneumatophore are copied (personal, you customize them).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
RULES_DIR="$CLAUDE_DIR/rules"
SKILLS_DIR="$CLAUDE_DIR/skills"

echo "MESO: Modular Exosymbiotic Organelle"
echo "Installing colony into $CLAUDE_DIR"
echo ""

# Create directories
mkdir -p "$RULES_DIR"
mkdir -p "$SKILLS_DIR"
SCRATCHPAD_DIR="$CLAUDE_DIR/scratchpad"

# --- Symlinked files (auto-update on git pull) ---

# Genome
if [ -L "$CLAUDE_DIR/STANDING-ORDERS.md" ] || [ ! -e "$CLAUDE_DIR/STANDING-ORDERS.md" ]; then
    ln -sf "$SCRIPT_DIR/STANDING-ORDERS.md" "$CLAUDE_DIR/STANDING-ORDERS.md"
    echo "  [symlink] STANDING-ORDERS.md (genome)"
else
    echo "  [skip]    STANDING-ORDERS.md exists and is not a symlink — not overwriting"
fi

# Zooids (always-loaded rules)
# Operons are excluded — they install to skills/ below
OPERON_ZOOIDS="03-context.md 05-auditing.md 06-orchestration.md 07-recovery.md 09-evolution.md"
for zooid in "$SCRIPT_DIR"/zooids/*.md; do
    name="$(basename "$zooid")"

    # Skip zooids that have been promoted to operons
    if echo "$OPERON_ZOOIDS" | grep -qw "$name"; then
        continue
    fi

    target="$RULES_DIR/$name"
    if [ -L "$target" ] || [ ! -e "$target" ]; then
        ln -sf "$zooid" "$target"
        echo "  [symlink] rules/$name (zooid)"
    else
        echo "  [skip]    rules/$name exists and is not a symlink — not overwriting"
    fi
done

# Operons (trigger-activated skill modules)
for operon_dir in "$SCRIPT_DIR"/operons/*/; do
    name="$(basename "$operon_dir")"
    target_dir="$SKILLS_DIR/$name"

    if [ -L "$target_dir" ] || [ ! -e "$target_dir" ]; then
        ln -sf "$operon_dir" "$target_dir"
        echo "  [symlink] skills/$name/ (operon)"
    else
        echo "  [skip]    skills/$name/ exists and is not a symlink — not overwriting"
    fi

    # Clean up the corresponding zooid from rules/ if it was previously installed
    case "$name" in
        orchestration)   old="$RULES_DIR/06-orchestration.md" ;;
        recovery)        old="$RULES_DIR/07-recovery.md" ;;
        evolution)       old="$RULES_DIR/09-evolution.md" ;;
        auditing)        old="$RULES_DIR/05-auditing.md" ;;
        context-engineering) old="$RULES_DIR/03-context.md" ;;
        *) old="" ;;
    esac

    if [ -n "$old" ] && [ -L "$old" ]; then
        rm "$old"
        echo "  [clean]   removed rules/$(basename "$old") (promoted to operon)"
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

# --- Scratchpad (persistent staging area) ---

mkdir -p "$SCRATCHPAD_DIR/agent-output"
mkdir -p "$SCRATCHPAD_DIR/snapshots"

if [ ! -e "$SCRATCHPAD_DIR/MANIFEST.md" ]; then
    cat > "$SCRATCHPAD_DIR/MANIFEST.md" << 'MANIFEST'
# Scratchpad Manifest (Global)

Persistent staging area for cross-project work-in-progress.
Governed by the scratchpad operon (Cystozooid).

| File | Purpose | Target | Status | Created | Last Touched |
|------|---------|--------|--------|---------|--------------|
| | | | | | |
MANIFEST
    echo "  [create]  scratchpad/MANIFEST.md (cystozooid)"
else
    echo "  [skip]    scratchpad/MANIFEST.md already exists"
fi

echo ""
echo "Colony installed."
echo ""
echo "Architecture:"
echo "  Zooids     (rules/)      — always-loaded core rules"
echo "  Operons    (skills/)     — trigger-activated knowledge modules"
echo "  Scratchpad (scratchpad/) — persistent staging area"
echo "  Genome                   — canonical reference, read on demand"
echo ""
echo "Next steps:"
echo "  1. Edit ~/.claude/CLAUDE.md with your identity and authorship info"
echo "  2. Edit ~/.claude/rules/00-operator.md with your background and traits"
echo "  3. Start a Claude Code session — the colony loads automatically"
echo ""
echo "The zooids, operons, and genome are symlinked to this repo."
echo "Run 'git pull' to receive updates. Your personal files won't be touched."
