#!/usr/bin/env bash
# MESO Install Script (Spore)
# Symbiont Systems LLC — https://symbiont.systems
#
# Installs the MESO colony into ~/.claude/
#
# Trust model (Model C — Hybrid):
#   Symlinked: Genome (STANDING-ORDERS.md) — reference material, auto-updates on git pull
#   Copied:    Zooids, operons, stolon, pneumatophore — behavioral rules, decoupled from git
#
# This means edits to your zooids and operons stay local. They won't leak
# back to the repo on git add/push. Use --update to pull upstream changes
# into your local copies after reviewing diffs.
#
# Usage:
#   ./install.sh            First-time install
#   ./install.sh --update   Show diffs and apply upstream changes to local copies

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
RULES_DIR="$CLAUDE_DIR/rules"
SKILLS_DIR="$CLAUDE_DIR/skills"
SCRATCHPAD_DIR="$CLAUDE_DIR/scratchpad"
MODE="${1:-install}"

# --- Helpers ---

# Replace a symlink with a copy (migration from old install model)
migrate_symlink_to_copy() {
    local source="$1"
    local target="$2"
    if [ -L "$target" ]; then
        rm "$target"
        cp -r "$source" "$target"
        return 0  # migrated
    fi
    return 1  # not a symlink
}

# Copy a file if target doesn't exist, or migrate if it's a stale symlink
install_copy() {
    local source="$1"
    local target="$2"
    local label="$3"

    if [ -L "$target" ]; then
        # Migrate from symlink to copy
        rm "$target"
        cp "$source" "$target"
        echo "  [migrate] $label (symlink → copy)"
    elif [ ! -e "$target" ]; then
        cp "$source" "$target"
        echo "  [copy]    $label"
    else
        echo "  [skip]    $label exists — not overwriting (use --update)"
    fi
}

# Copy a directory if target doesn't exist, or migrate if it's a stale symlink
install_copy_dir() {
    local source="$1"
    local target="$2"
    local label="$3"

    if [ -L "$target" ]; then
        # Migrate from symlink to copy
        rm "$target"
        cp -r "$source" "$target"
        echo "  [migrate] $label (symlink → copy)"
    elif [ ! -e "$target" ]; then
        cp -r "$source" "$target"
        echo "  [copy]    $label"
    else
        echo "  [skip]    $label exists — not overwriting (use --update)"
    fi
}

# --- Update mode ---

if [ "$MODE" = "--update" ]; then
    echo "MESO: Checking for upstream changes"
    echo ""

    CHANGED=0

    # Check zooids
    OPERON_ZOOIDS="03-context.md 05-auditing.md 06-orchestration.md 07-recovery.md 09-evolution.md"
    for zooid in "$SCRIPT_DIR"/zooids/*.md; do
        name="$(basename "$zooid")"
        if echo "$OPERON_ZOOIDS" | grep -qw "$name"; then
            continue
        fi
        target="$RULES_DIR/$name"
        if [ -e "$target" ] && ! diff -q "$zooid" "$target" > /dev/null 2>&1; then
            echo "=== rules/$name ==="
            diff -u "$target" "$zooid" --label "installed" --label "upstream" || true
            echo ""
            CHANGED=1
        fi
    done

    # Check operons
    for operon_dir in "$SCRIPT_DIR"/operons/*/; do
        name="$(basename "$operon_dir")"
        for source_file in "$operon_dir"*; do
            fname="$(basename "$source_file")"
            target_file="$SKILLS_DIR/$name/$fname"
            if [ -e "$target_file" ] && ! diff -q "$source_file" "$target_file" > /dev/null 2>&1; then
                echo "=== skills/$name/$fname ==="
                diff -u "$target_file" "$source_file" --label "installed" --label "upstream" || true
                echo ""
                CHANGED=1
            elif [ ! -e "$target_file" ]; then
                echo "=== skills/$name/$fname (new file) ==="
                echo "  File exists in upstream but not installed."
                echo ""
                CHANGED=1
            fi
        done
    done

    # Check genome symlink
    if [ -L "$CLAUDE_DIR/STANDING-ORDERS.md" ]; then
        echo "  Genome: symlinked (auto-updates) ✓"
    elif [ -e "$CLAUDE_DIR/STANDING-ORDERS.md" ]; then
        echo "  Genome: WARNING — regular file, not symlinked. Consider re-symlinking."
    fi
    echo ""

    if [ "$CHANGED" -eq 0 ]; then
        echo "No changes between upstream and installed copies."
        exit 0
    fi

    echo "Apply these changes? This will overwrite your local copies."
    read -rp "[y/N] " confirm
    if [[ "$confirm" != [yY] ]]; then
        echo "Aborted. No changes made."
        exit 0
    fi

    # Apply zooid updates
    for zooid in "$SCRIPT_DIR"/zooids/*.md; do
        name="$(basename "$zooid")"
        if echo "$OPERON_ZOOIDS" | grep -qw "$name"; then
            continue
        fi
        target="$RULES_DIR/$name"
        if [ -e "$target" ] && ! diff -q "$zooid" "$target" > /dev/null 2>&1; then
            cp "$zooid" "$target"
            echo "  [update]  rules/$name"
        fi
    done

    # Apply operon updates
    for operon_dir in "$SCRIPT_DIR"/operons/*/; do
        name="$(basename "$operon_dir")"
        mkdir -p "$SKILLS_DIR/$name"
        for source_file in "$operon_dir"*; do
            fname="$(basename "$source_file")"
            target_file="$SKILLS_DIR/$name/$fname"
            if ! diff -q "$source_file" "$target_file" > /dev/null 2>&1; then
                cp "$source_file" "$target_file"
                echo "  [update]  skills/$name/$fname"
            fi
        done
    done

    echo ""
    echo "Updates applied."
    exit 0
fi

# --- Install mode ---

echo "MESO: Modular Exosymbiotic Organelle"
echo "Installing colony into $CLAUDE_DIR"
echo ""

# Create directories
mkdir -p "$RULES_DIR"
mkdir -p "$SKILLS_DIR"

# --- Symlinked: Genome only (reference material, safe to auto-update) ---

if [ -L "$CLAUDE_DIR/STANDING-ORDERS.md" ] || [ ! -e "$CLAUDE_DIR/STANDING-ORDERS.md" ]; then
    ln -sf "$SCRIPT_DIR/STANDING-ORDERS.md" "$CLAUDE_DIR/STANDING-ORDERS.md"
    echo "  [symlink] STANDING-ORDERS.md (genome — auto-updates on git pull)"
else
    echo "  [skip]    STANDING-ORDERS.md exists and is not a symlink — not overwriting"
fi

# --- Copied: Zooids (behavioral rules, decoupled from git) ---

OPERON_ZOOIDS="03-context.md 05-auditing.md 06-orchestration.md 07-recovery.md 09-evolution.md"
for zooid in "$SCRIPT_DIR"/zooids/*.md; do
    name="$(basename "$zooid")"

    # Skip zooids that have been promoted to operons
    if echo "$OPERON_ZOOIDS" | grep -qw "$name"; then
        continue
    fi

    install_copy "$zooid" "$RULES_DIR/$name" "rules/$name (zooid)"
done

# --- Copied: Operons (behavioral rules, decoupled from git) ---

for operon_dir in "$SCRIPT_DIR"/operons/*/; do
    name="$(basename "$operon_dir")"
    install_copy_dir "$operon_dir" "$SKILLS_DIR/$name" "skills/$name/ (operon)"

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

# --- Copied: Personal files (customize these) ---

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
    chmod 600 "$RULES_DIR/00-operator.md"
    echo "  [copy]    rules/00-operator.md (stolon) — customize this (mode 600)"
else
    # Ensure existing stolon has restricted permissions
    chmod 600 "$RULES_DIR/00-operator.md"
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
echo "Trust model (Hybrid):"
echo "  Genome     (symlinked)  — auto-updates on git pull"
echo "  Zooids     (copied)    — decoupled from git, your edits stay local"
echo "  Operons    (copied)    — decoupled from git, your edits stay local"
echo "  Scratchpad (local)     — persistent staging area"
echo ""
echo "Next steps:"
echo "  1. Edit ~/.claude/CLAUDE.md with your identity and authorship info"
echo "  2. Edit ~/.claude/rules/00-operator.md with your background and traits"
echo "  3. Start a Claude Code session — the colony loads automatically"
echo ""
echo "To apply upstream updates after 'git pull':"
echo "  ./install.sh --update    (shows diffs, asks before overwriting)"
