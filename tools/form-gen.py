#!/usr/bin/env python3
"""
MESO Forms Generator
Converts YAML form definitions to self-contained HTML forms.

Authored by Rowan Valle; Executed by Claude Code
Symbiont Systems LLC
"""

import argparse
import json
import os
import sys
import yaml
from pathlib import Path
from datetime import datetime


def load_yaml(yaml_path):
    """Load and parse YAML form definition."""
    yaml_path = Path(yaml_path)
    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML file not found: {yaml_path}")

    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


def validate_schema(config):
    """Validate YAML schema has required fields."""
    required_fields = ['title', 'sections']

    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(config['sections'], list) or len(config['sections']) == 0:
        raise ValueError("'sections' must be a non-empty list")

    for section_idx, section in enumerate(config['sections']):
        if 'name' not in section:
            raise ValueError(f"Section {section_idx} missing 'name' field")
        if 'questions' not in section or not section['questions']:
            raise ValueError(f"Section '{section['name']}' has no questions")

        for q_idx, question in enumerate(section['questions']):
            if 'id' not in question:
                raise ValueError(f"Question {q_idx} in section '{section['name']}' missing 'id'")
            if 'title' not in question:
                raise ValueError(f"Question '{question['id']}' missing 'title'")
            if 'type' not in question:
                raise ValueError(f"Question '{question['id']}' missing 'type'")


def build_data_attributes(question):
    """Build data-* attributes for v2.0 features (validation, conditionals)."""
    attrs = []

    # Validation attributes
    validation = question.get('validation')
    if validation:
        attrs.append(f'data-validation=\'{json.dumps(validation)}\'')

    # Conditional logic attributes
    show_if = question.get('show_if')
    if show_if:
        attrs.append(f'data-show-if="{show_if}"')

    required_if = question.get('required_if')
    if required_if:
        attrs.append(f'data-required-if="{required_if}"')

    disabled_if = question.get('disabled_if')
    if disabled_if:
        attrs.append(f'data-disabled-if="{disabled_if}"')

    return ' '.join(attrs)


def render_question(question, theme='terminal'):
    """Render a single question to HTML."""
    q_id = question['id']
    q_title = question['title']
    q_type = question['type']
    q_context = question.get('context', '')
    help_text = question.get('help_text', '')
    tooltip = question.get('tooltip', '')

    html_parts = []
    html_parts.append(f'<div class="question" data-question="{q_id}">')
    html_parts.append(f'  <div class="question-title">{q_title}</div>')

    if q_context:
        html_parts.append(f'  <div class="context">{q_context}</div>')

    # Build data attributes for validation and conditional logic
    data_attrs = build_data_attributes(question)

    # Render input based on type
    if q_type == 'radio':
        options = question.get('options', [])
        for idx, option in enumerate(options):
            opt_value = option['value']
            opt_label = option['label']
            opt_desc = option.get('description', '')
            opt_recommended = option.get('recommended', False)
            opt_pros = option.get('pros', [])
            opt_cons = option.get('cons', [])
            opt_impl = option.get('implementation', '')

            option_class = 'option'
            if opt_recommended:
                option_class += ' recommended'

            html_parts.append(f'  <div class="{option_class}">')
            html_parts.append(f'    <label class="option-label">')

            # Add data attributes to first radio button for conditional logic
            radio_attrs = f'id="{q_id}" ' if idx == 0 else ''
            radio_attrs += data_attrs if idx == 0 else ''
            html_parts.append(f'      <input type="radio" name="{q_id}" value="{opt_value}" {radio_attrs}>')
            html_parts.append(f'      <div>')
            html_parts.append(f'        <strong>{opt_label}</strong>')
            if opt_recommended:
                html_parts.append('        <span class="recommended-badge">RECOMMENDED</span>')
            if opt_desc:
                html_parts.append(f'        <div>{opt_desc}</div>')

            if opt_pros or opt_cons:
                html_parts.append('        <div class="pros-cons">')
                for pro in opt_pros:
                    html_parts.append(f'          <div class="pros">{pro}</div>')
                for con in opt_cons:
                    html_parts.append(f'          <div class="cons">{con}</div>')
                html_parts.append('        </div>')

            if opt_impl:
                html_parts.append(f'        <div class="implementation">{opt_impl}</div>')

            html_parts.append('      </div>')
            html_parts.append('    </label>')
            html_parts.append('  </div>')

    elif q_type == 'checkbox':
        options = question.get('options', [])
        html_parts.append('  <div class="checkbox-group">')
        for idx, option in enumerate(options):
            opt_value = option['value']
            opt_label = option['label']
            opt_desc = option.get('description', '')

            html_parts.append('    <label>')
            # Add data attributes to first checkbox for conditional logic
            checkbox_attrs = f'id="{q_id}" ' if idx == 0 else ''
            checkbox_attrs += data_attrs if idx == 0 else ''
            html_parts.append(f'      <input type="checkbox" name="{q_id}-{opt_value}" value="{opt_value}" {checkbox_attrs}>')
            html_parts.append(f'      <strong>{opt_label}</strong>')
            if opt_desc:
                html_parts.append(f'      <div>{opt_desc}</div>')
            html_parts.append('    </label>')
        html_parts.append('  </div>')

    elif q_type == 'text':
        placeholder = question.get('placeholder', '')
        html_parts.append(f'  <label for="{q_id}" class="sr-only">{q_title}</label>')
        html_parts.append(f'  <input type="text" id="{q_id}" name="{q_id}" placeholder="{placeholder}" {data_attrs} aria-label="{q_title}">')

    elif q_type == 'number':
        min_val = question.get('min', '')
        max_val = question.get('max', '')
        placeholder = question.get('placeholder', '')
        html_parts.append(f'  <label for="{q_id}" class="sr-only">{q_title}</label>')
        html_parts.append(f'  <input type="number" id="{q_id}" name="{q_id}" min="{min_val}" max="{max_val}" placeholder="{placeholder}" {data_attrs} aria-label="{q_title}">')

    elif q_type == 'textarea':
        placeholder = question.get('placeholder', '')
        rows = question.get('rows', 4)
        html_parts.append(f'  <label for="{q_id}" class="sr-only">{q_title}</label>')
        html_parts.append(f'  <textarea id="{q_id}" name="{q_id}" rows="{rows}" placeholder="{placeholder}" {data_attrs} aria-label="{q_title}"></textarea>')

    elif q_type == 'ranking':
        options = question.get('options', [])
        for idx, option in enumerate(options):
            opt_value = option['value']
            opt_label = option['label']
            html_parts.append('  <div class="ranking-item">')
            html_parts.append(f'    <input type="number" name="{q_id}-{opt_value}" min="1" max="{len(options)}" value="{idx + 1}">')
            html_parts.append(f'    <span>{opt_label}</span>')
            html_parts.append('  </div>')

    elif q_type == 'star-rating':
        max_stars = question.get('max', 5)
        labels = question.get('labels', {})
        min_label = labels.get('min', '')
        max_label = labels.get('max', '')

        html_parts.append('  <fieldset class="star-rating">')
        html_parts.append(f'    <legend class="sr-only">{q_title}</legend>')
        if min_label or max_label:
            html_parts.append('    <div class="rating-labels">')
            if min_label:
                html_parts.append(f'      <span class="rating-label-min">{min_label}</span>')
            if max_label:
                html_parts.append(f'      <span class="rating-label-max">{max_label}</span>')
            html_parts.append('    </div>')

        # Render stars in reverse order for CSS sibling selector trick
        for i in range(max_stars, 0, -1):
            html_parts.append(f'    <input type="radio" id="{q_id}-star{i}" name="{q_id}" value="{i}" {data_attrs if i == max_stars else ""}>')
            html_parts.append(f'    <label for="{q_id}-star{i}" title="{i} star{"s" if i > 1 else ""}">★</label>')

        html_parts.append('  </fieldset>')

    elif q_type == 'likert':
        min_val = question.get('min', 1)
        max_val = question.get('max', 10)
        min_label = question.get('min_label', '')
        max_label = question.get('max_label', '')

        html_parts.append('  <fieldset class="likert-scale">')
        html_parts.append(f'    <legend class="sr-only">{q_title}</legend>')
        if min_label or max_label:
            html_parts.append('    <div class="scale-labels">')
            if min_label:
                html_parts.append(f'      <span>{min_label}</span>')
            if max_label:
                html_parts.append(f'      <span>{max_label}</span>')
            html_parts.append('    </div>')

        html_parts.append('    <div class="scale-options">')
        for i in range(min_val, max_val + 1):
            option_attrs = f'{data_attrs}' if i == min_val else ''
            html_parts.append(f'      <input type="radio" id="{q_id}-{i}" name="{q_id}" value="{i}" {option_attrs}>')
            html_parts.append(f'      <label for="{q_id}-{i}">{i}</label>')
        html_parts.append('    </div>')
        html_parts.append('  </fieldset>')

    elif q_type == 'range':
        min_val = question.get('min', 0)
        max_val = question.get('max', 100)
        step = question.get('step', 1)
        unit = question.get('unit', '')
        show_value = question.get('show_value', True)
        default = question.get('default', (min_val + max_val) // 2)

        html_parts.append('  <div class="range-input">')
        html_parts.append(f'    <input type="range" id="{q_id}" name="{q_id}" min="{min_val}" max="{max_val}" step="{step}" value="{default}" {data_attrs}>')
        if show_value:
            html_parts.append(f'    <output for="{q_id}" class="range-value" aria-live="polite">{default}{unit}</output>')
        html_parts.append('  </div>')

    elif q_type == 'importance':
        min_val = question.get('min', 1)
        max_val = question.get('max', 10)
        default = question.get('default', 5)
        min_label = question.get('min_label', 'Low')
        max_label = question.get('max_label', 'Critical')

        html_parts.append('  <div class="importance-gauge">')
        html_parts.append('    <div class="gauge-track">')
        gauge_percent = ((default - min_val) / (max_val - min_val)) * 100
        html_parts.append(f'      <div class="gauge-fill" data-value="{default}" style="width: {gauge_percent}%"></div>')
        html_parts.append('    </div>')
        html_parts.append(f'    <input type="range" id="{q_id}" name="{q_id}" min="{min_val}" max="{max_val}" value="{default}" {data_attrs}>')
        html_parts.append('    <div class="gauge-labels">')
        html_parts.append(f'      <span>{min_label}</span>')
        html_parts.append(f'      <span class="gauge-current-value" aria-live="polite">{default}</span>')
        html_parts.append(f'      <span>{max_label}</span>')
        html_parts.append('    </div>')
        html_parts.append('  </div>')

    # Add help text if provided
    if help_text:
        html_parts.append(f'  <div class="help-text">{help_text}</div>')

    # Add tooltip if provided
    if tooltip:
        html_parts.append(f'  <span class="tooltip" title="{tooltip}"></span>')

    # Add reasoning field if requested
    if question.get('reasoning'):
        html_parts.append('  <label class="reasoning-label">Your reasoning:</label>')
        html_parts.append(f'  <textarea name="{q_id}-reasoning" class="reasoning" rows="3" placeholder="Explain your choice..."></textarea>')

    # Add comments field if requested
    if question.get('comments'):
        html_parts.append('  <label class="comments-label">Comments / Additional thoughts:</label>')
        html_parts.append(f'  <textarea name="{q_id}-comments" class="comments" rows="3" placeholder="Any other context, concerns, or ideas..."></textarea>')

    # Add follow-up questions
    follow_ups = question.get('follow_ups', [])
    for fu_idx, follow_up in enumerate(follow_ups):
        fu_title = follow_up['title']
        fu_type = follow_up['type']
        fu_placeholder = follow_up.get('placeholder', '')

        html_parts.append('  <div class="follow-up">')
        html_parts.append(f'    <div class="follow-up-title">{fu_title}</div>')

        if fu_type == 'text':
            html_parts.append(f'    <input type="text" name="{q_id}-followup-{fu_idx}" placeholder="{fu_placeholder}">')
        elif fu_type == 'number':
            html_parts.append(f'    <input type="number" name="{q_id}-followup-{fu_idx}" placeholder="{fu_placeholder}">')
        elif fu_type == 'textarea':
            html_parts.append(f'    <textarea name="{q_id}-followup-{fu_idx}" rows="3" placeholder="{fu_placeholder}"></textarea>')
        elif fu_type == 'radio':
            fu_options = follow_up.get('options', [])
            for fu_opt in fu_options:
                fu_opt_value = fu_opt['value']
                fu_opt_label = fu_opt['label']
                html_parts.append(f'    <label>')
                html_parts.append(f'      <input type="radio" name="{q_id}-followup-{fu_idx}" value="{fu_opt_value}">')
                html_parts.append(f'      {fu_opt_label}')
                html_parts.append(f'    </label><br>')

        html_parts.append('  </div>')

    html_parts.append('</div>')

    return '\n'.join(html_parts)


def render_section(section, theme='terminal'):
    """Render a section with all its questions."""
    section_name = section['name']
    questions = section['questions']

    html_parts = []
    html_parts.append('<div class="section">')
    html_parts.append(f'  <h2 class="section-header">{section_name}</h2>')

    for question in questions:
        html_parts.append(render_question(question, theme))

    html_parts.append('</div>')

    return '\n'.join(html_parts)


def inject_template(config, sections_html, css_content, js_content, theme='terminal'):
    """Inject generated content into base template."""
    title = config.get('title', 'Form')
    description = config.get('description', '')
    total_questions = config.get('total_questions', 0)

    # Create storage key from title
    storage_key = f"meso-form-{title.lower().replace(' ', '-')}"

    # Create export filename
    export_filename = f"{datetime.now().strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.json"

    # Build complete HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css_content}
    </style>
</head>
<body>
    <header>
        <h1>{title}</h1>
        <div class="subtitle">
            {description}<br>
            Progress auto-saves. Export to JSON when done.
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>
        <div class="stats">
            <span>Progress: <span id="progressPercent" aria-live="polite" aria-atomic="true">0</span>%</span>
            <span>Answered: <span id="answeredCount" aria-live="polite" aria-atomic="true">0</span> / {total_questions}</span>
            <span class="saved-indicator" id="savedIndicator" aria-live="polite" aria-atomic="true">✓ Auto-saved</span>
        </div>
    </header>

    <form id="form">
{sections_html}
    </form>

    <div class="actions">
        <button type="button" id="saveBtn">💾 Save</button>
        <button type="button" id="exportBtn">📥 Export JSON</button>
        <button type="button" id="clearBtn" class="secondary">🗑️ Clear</button>
        <button type="button" id="printBtn" class="secondary">🖨️ Print</button>
    </div>

    <script>
{js_content}
    </script>
</body>
</html>"""

    # Replace placeholders in JS
    html = html.replace('{{TOTAL_QUESTIONS}}', str(total_questions))
    html = html.replace('{{STORAGE_KEY}}', storage_key)
    html = html.replace('{{EXPORT_FILENAME}}', export_filename)

    return html


def generate_form(yaml_path, output_path=None, theme='terminal'):
    """Main generation function."""
    # Load YAML
    config = load_yaml(yaml_path)

    # Validate schema
    validate_schema(config)

    # Determine output path
    if output_path is None:
        yaml_file = Path(yaml_path)
        output_path = yaml_file.parent / f"{yaml_file.stem}.html"

    # Load CSS and JS templates
    templates_dir = Path(__file__).parent.parent / 'templates' / 'forms'

    css_path = templates_dir / f'{theme}-theme.css'
    if not css_path.exists():
        css_path = templates_dir / 'terminal-theme.css'

    js_paths = [
        templates_dir / 'validation.js',
        templates_dir / 'conditional-logic.js',
        templates_dir / 'form-logic.js'
    ]

    with open(css_path, 'r') as f:
        css_content = f.read()

    # Load and combine all JavaScript files
    js_parts = []
    for js_path in js_paths:
        if js_path.exists():
            with open(js_path, 'r') as f:
                js_parts.append(f.read())
        else:
            # Skip v2.0 files if they don't exist (backward compatibility)
            if js_path.name not in ['validation.js', 'conditional-logic.js']:
                raise FileNotFoundError(f"Required JS file not found: {js_path}")

    js_content = '\n\n'.join(js_parts)

    # Extract validation presets (v2.0)
    validation_presets = config.get('validation_presets', {})

    # Inject validation presets into JavaScript
    js_content = js_content.replace(
        '{{VALIDATION_PRESETS}}',
        json.dumps(validation_presets)
    )

    # Render sections
    sections_html_parts = []
    for section in config['sections']:
        sections_html_parts.append(render_section(section, theme))

    sections_html = '\n'.join(sections_html_parts)

    # Inject into template
    final_html = inject_template(config, sections_html, css_content, js_content, theme)

    # Write output
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(final_html)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Generate HTML forms from YAML definitions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.yaml
  %(prog)s input.yaml -o output.html
  %(prog)s input.yaml --theme terminal
        """
    )

    parser.add_argument('input', help='YAML form definition file')
    parser.add_argument('-o', '--output', help='Output HTML file (default: input.html)')
    parser.add_argument('--theme', default='terminal', choices=['terminal', 'biopunk', 'artdeco'],
                        help='Theme to use (default: terminal)')

    args = parser.parse_args()

    try:
        output_path = generate_form(args.input, args.output, args.theme)
        print(f"✓ Generated form: {output_path}")
        print(f"  Theme: {args.theme}")
        print(f"  Open in browser: file://{output_path.absolute()}")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
