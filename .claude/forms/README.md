# Forms Repository

**Purpose**: Store completed form exports for future reference and idea mining

## Directory Structure

```
.claude/forms/
  exports/          # JSON exports from completed forms
  archives/         # Older forms, organized by date
  README.md         # This file
```

## Usage

### Exporting Forms

When you complete a form:
1. Click "📥 Export JSON" button in the form
2. Save the JSON file to `.claude/forms/exports/` in the relevant project
3. Name format: `YYYY-MM-DD-form-topic.json`
   - Example: `2026-02-07-ticker-architecture.json`

### Organizing Exports

**Active decisions** (current/recent):
- Location: `.claude/forms/exports/`
- Keep here while actively referencing

**Archived decisions** (historical):
- Location: `.claude/forms/archives/YYYY/`
- Move here after implementation or when superseded

### JSON Structure

Exported forms contain:
```json
{
  "formTitle": "Form Name",
  "exportDate": "2026-02-07T10:30:00Z",
  "data": {
    "q1-1": "answer",
    "q1-1-reasoning": "because...",
    "q1-1-comments": "also, I was thinking..."
  }
}
```

### Integration with Knowledge Operon

Form exports can be processed into knowledge documents:

```bash
# Export form to JSON
# Then ask: "Convert this form export to a knowledge document"
```

AI will:
1. Parse the JSON
2. Extract key decisions
3. Generate structured markdown in `docs/knowledge/`
4. Create decision log entries
5. Update relevant indexes

### Mining Ideas

Forms capture:
- **Decisions made**: What was chosen and why
- **Reasoning**: Formal justifications
- **Comments**: Informal thoughts, concerns, tangents
- **Context**: Background information from questions
- **Trade-offs**: Pros/cons considered

Review exports periodically to:
- Revisit decisions when context changes
- Extract patterns across multiple projects
- Generate new ideas from old comments
- Identify recurring concerns or themes
- Build decision templates for common scenarios

### Search & Query

```bash
# Find all architectural decision forms
grep -r "Architectural Decision" .claude/forms/exports/

# Find forms mentioning specific technology
jq '.data | to_entries[] | select(.value | contains("PostgreSQL"))' exports/*.json

# Extract all comments from a form
jq '.data | to_entries[] | select(.key | endswith("-comments"))' exports/2026-02-07-ticker-architecture.json
```

## Project-Specific Forms

Each project should have its own `.claude/forms/` directory:

- **techbiont-framework**: MESO development, meta-decisions
- **margin**: Product decisions, architecture, features
- Other projects: As needed

Forms are project-scoped, not global. This keeps context clear.

## Maintenance

**Quarterly review** (March, June, September, December):
1. Archive old exports (>90 days) to `archives/YYYY/`
2. Review archived decisions for lessons learned
3. Update templates based on recurring patterns
4. Prune outdated forms (superseded decisions)

## Related Operons

- **forms**: Generate interactive decision forms
- **knowledge**: Process forms into knowledge docs
- **evolution**: Use AAR forms for retrospectives
- **workspace**: Long-term artifact storage

---

**Status**: Active system
**Last updated**: 2026-02-07
**Maintainer**: Rowan Valle
