# MESO Tools

Utility scripts for the MESO framework.

Authored by Rowan Valle; Executed by Claude Code
Symbiont Systems LLC

---

## form-gen.py

**Form Generator** - Converts YAML form definitions to self-contained HTML forms.

### Usage

```bash
python3 tools/form-gen.py INPUT.yaml [-o OUTPUT.html] [--theme THEME]
```

### Arguments

- `INPUT.yaml` - YAML form definition (required)
- `-o, --output` - Output HTML file path (default: `INPUT.html`)
- `--theme` - Theme to use: `terminal` (default) or `biopunk`

### Examples

```bash
# Generate form with default settings (terminal theme)
python3 tools/form-gen.py templates/forms/example-architecture.yaml

# Specify output location
python3 tools/form-gen.py my-form.yaml -o ~/.claude/my-form.html

# Use biopunk theme (Phase 3+)
python3 tools/form-gen.py my-form.yaml --theme biopunk
```

### Features

✅ **Auto-save** - Progress saves to localStorage automatically
✅ **Progress tracking** - Visual progress bar and completion percentage
✅ **JSON export** - Download form data as structured JSON
✅ **Offline-first** - Self-contained HTML, no external dependencies
✅ **Mobile-responsive** - Works on phones and tablets
✅ **Validation** - YAML schema validation with clear error messages

### YAML Schema

See `templates/forms/example-*.yaml` for complete examples.

**Minimal structure:**

```yaml
title: "Form Title"
description: "Form description"
total_questions: N

sections:
  - name: "SECTION NAME"
    questions:
      - id: "unique-id"
        title: "Question text"
        type: "radio"  # radio, checkbox, text, textarea, number, ranking
        options:
          - value: "option-a"
            label: "Option A"
        reasoning: true   # Optional: add reasoning textarea
        comments: true    # Optional: add comments textarea
```

### Question Types

| Type | Description | Use Case |
|------|-------------|----------|
| `radio` | Single choice | Mutually exclusive options |
| `checkbox` | Multiple choice | Select multiple answers |
| `text` | Short text input | Names, identifiers |
| `textarea` | Long text input | Explanations, descriptions |
| `number` | Numeric input | Ratings, quantities |
| `ranking` | Rank options | Prioritization |

### Error Handling

The generator validates:
- ✅ Required fields (title, sections, questions)
- ✅ Question structure (id, title, type)
- ✅ File existence
- ✅ YAML syntax

Error messages are clear and actionable:

```bash
✗ Error: Missing required field: sections
✗ Error: Question 'q1' missing 'type'
✗ Error: YAML file not found: /path/to/file.yaml
```

### Output

Generated HTML forms are **self-contained** and include:
- Embedded CSS (terminal or biopunk theme)
- Embedded JavaScript (auto-save, progress tracking, export logic)
- No external dependencies (works offline)

Open generated forms directly in any browser:

```bash
firefox ~/.claude/my-form.html
# or
open ~/.claude/my-form.html  # macOS
```

### Development Status

**Phase 1 (✅ Complete)**: Generator MVP
- YAML parsing and validation
- HTML generation for all v1.0 question types
- CLI interface with theme support
- Error handling

**Phase 2 (Planned)**: Validation + Conditionals
- Validation framework (`show_if`, `required_if`)
- Expression language for conditional logic
- Inline validation errors

**Phase 3 (Planned)**: Biopunk Theme + New Components
- Biopunk aesthetic CSS theme
- Star rating component
- Likert scale component
- Range slider component
- Importance gauge component

**Phase 4 (Planned)**: Conversational Mode
- One-question-at-a-time interface
- Smooth transitions
- Typeform-style UX

**Phase 5 (Planned)**: Advanced Features
- Repeating sections
- Calculated fields
- Expression evaluator

### Testing

Test the generator with example forms:

```bash
# Architecture decision template
python3 tools/form-gen.py templates/forms/example-architecture.yaml -o /tmp/test-arch.html

# After Action Report template
python3 tools/form-gen.py templates/forms/example-aar.yaml -o /tmp/test-aar.html

# Simple survey template
python3 tools/form-gen.py templates/forms/example-survey.yaml -o /tmp/test-survey.html
```

Open generated forms in browser to verify:
- Form renders correctly
- Auto-save works (fill out fields, refresh page)
- Progress tracking updates
- Export generates valid JSON

### Troubleshooting

**Error: "No module named 'yaml'"**

Install PyYAML:
```bash
pip3 install pyyaml
# or
pip3 install --user pyyaml
```

**Error: "Permission denied"**

Make script executable:
```bash
chmod +x tools/form-gen.py
```

**Generated form doesn't load CSS/JS**

Check that `templates/forms/` directory exists and contains:
- `terminal-theme.css`
- `biopunk-theme.css` (Phase 3+)
- `form-logic.js`

**Form doesn't auto-save**

Check browser localStorage settings. Some privacy modes block localStorage.

### Contributing

When adding new question types:

1. Update YAML schema in SKILL.md
2. Add rendering logic in `render_question()` function
3. Add CSS styling in theme files
4. Update this README with examples
5. Create test YAML in `templates/forms/`

### Version

**v1.0.0** - Phase 1 MVP (2026-02-08)

See `~/.claude/skills/forms/SKILL.md` for complete forms operon documentation.
