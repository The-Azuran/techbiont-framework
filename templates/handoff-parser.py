#!/usr/bin/env python3
"""
Handoff Transcript Parser
Extracts session data from Claude Code JSONL transcripts.

Usage:
    python3 handoff-parser.py <transcript_path> [output_path]

If output_path is provided, generates handoff skeleton.
If output_path is /dev/null, prints JSON to stdout.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_transcript(transcript_path: str) -> Dict[str, Any]:
    """
    Parse JSONL session transcript and extract session data.

    Returns dict with:
    - session_id: str
    - time_start: ISO timestamp
    - time_end: ISO timestamp
    - duration_minutes: int
    - project: str (cwd)
    - git_branch: str
    - files_modified: list of {path, tool, line_count}
    - commands_run: list of {command, description, timestamp}
    - tasks_completed: list of {id, subject, status}
    - commits: list of {hash, message, timestamp}
    """

    session_data = {
        'session_id': 'unknown',
        'time_start': None,
        'time_end': None,
        'duration_minutes': 0,
        'project': 'unknown',
        'git_branch': 'unknown',
        'files_modified': [],
        'commands_run': [],
        'tasks_completed': [],
        'commits': []
    }

    file_operations = {}  # Track unique files

    try:
        with open(transcript_path, 'r') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            try:
                entry = json.loads(line.strip())

                # Extract timestamps
                if 'timestamp' in entry:
                    ts = entry['timestamp']
                    if session_data['time_start'] is None:
                        session_data['time_start'] = ts
                    session_data['time_end'] = ts

                # Extract session ID from first message
                if line_num == 1 and 'session_id' in entry:
                    session_data['session_id'] = entry['session_id']

                # Extract project path (cwd)
                if 'cwd' in entry:
                    session_data['project'] = entry['cwd']

                # Look for content blocks with tool uses
                if 'content' in entry and isinstance(entry['content'], list):
                    for block in entry['content']:
                        if not isinstance(block, dict):
                            continue

                        # Extract file operations (Edit/Write)
                        if block.get('type') == 'tool_use':
                            tool_name = block.get('name')
                            tool_input = block.get('input', {})

                            if tool_name == 'Edit':
                                file_path = tool_input.get('file_path')
                                if file_path:
                                    if file_path not in file_operations:
                                        file_operations[file_path] = {
                                            'path': file_path,
                                            'tool': 'Edit',
                                            'count': 0
                                        }
                                    file_operations[file_path]['count'] += 1

                            elif tool_name == 'Write':
                                file_path = tool_input.get('file_path')
                                content = tool_input.get('content', '')
                                if file_path:
                                    file_operations[file_path] = {
                                        'path': file_path,
                                        'tool': 'Write',
                                        'line_count': len(content.split('\n'))
                                    }

                            # Extract bash commands
                            elif tool_name == 'Bash':
                                command = tool_input.get('command')
                                description = tool_input.get('description', '')
                                if command:
                                    # Extract git commits
                                    if 'git commit' in command:
                                        session_data['commits'].append({
                                            'command': command,
                                            'timestamp': entry.get('timestamp', '')
                                        })

                                    # Track git branch
                                    if command.startswith('git branch --show-current') or \
                                       command.startswith('git rev-parse --abbrev-ref HEAD'):
                                        # Branch detection command
                                        pass

                                    session_data['commands_run'].append({
                                        'command': command,
                                        'description': description,
                                        'timestamp': entry.get('timestamp', '')
                                    })

                            # Extract task completions
                            elif tool_name == 'TaskUpdate':
                                if tool_input.get('status') == 'completed':
                                    task_id = tool_input.get('taskId')
                                    session_data['tasks_completed'].append({
                                        'id': task_id,
                                        'timestamp': entry.get('timestamp', '')
                                    })

                        # Extract tool results for git branch
                        elif block.get('type') == 'tool_result':
                            content = block.get('content')
                            if isinstance(content, str) and content.strip():
                                # Check if this looks like a branch name
                                if '\n' not in content and len(content) < 100 and '/' in content:
                                    # Could be a branch name
                                    if session_data['git_branch'] == 'unknown':
                                        session_data['git_branch'] = content.strip()

            except json.JSONDecodeError:
                # Skip malformed lines
                print(f"Warning: Skipping malformed line {line_num}", file=sys.stderr)
                continue
            except Exception as e:
                print(f"Warning: Error processing line {line_num}: {e}", file=sys.stderr)
                continue

        # Convert file_operations dict to list
        session_data['files_modified'] = list(file_operations.values())

        # Calculate duration
        if session_data['time_start'] and session_data['time_end']:
            try:
                start = datetime.fromisoformat(session_data['time_start'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(session_data['time_end'].replace('Z', '+00:00'))
                duration = end - start
                session_data['duration_minutes'] = int(duration.total_seconds() / 60)
            except Exception as e:
                print(f"Warning: Could not calculate duration: {e}", file=sys.stderr)

        # Extract session ID from transcript filename if not found
        if session_data['session_id'] == 'unknown':
            session_data['session_id'] = Path(transcript_path).stem

    except FileNotFoundError:
        print(f"Error: Transcript not found: {transcript_path}", file=sys.stderr)
    except Exception as e:
        print(f"Error: Failed to parse transcript: {e}", file=sys.stderr)

    return session_data


def generate_handoff_skeleton(session_data: Dict[str, Any], template_path: str, output_path: str):
    """
    Fill handoff template with auto-generated data.
    Leaves manual-input fields with PLACEHOLDER markers.
    """

    try:
        with open(template_path, 'r') as f:
            template = f.read()

        # Format files modified
        files_list = []
        for file_info in session_data['files_modified']:
            if 'line_count' in file_info:
                files_list.append(f"- {file_info['path']} ({file_info['tool']}, {file_info['line_count']} lines)")
            else:
                files_list.append(f"- {file_info['path']} ({file_info['tool']}, {file_info.get('count', 1)} edits)")
        files_modified = '\n'.join(files_list) if files_list else '(none)'

        # Format commands (limit to last 20)
        commands = []
        for cmd in session_data['commands_run'][-20:]:
            if cmd['description']:
                commands.append(f"# {cmd['description']}")
            commands.append(cmd['command'])
            commands.append('')
        commands_run = '\n'.join(commands) if commands else '(none)'

        # Format tasks completed
        completed_tasks = []
        for task in session_data['tasks_completed']:
            completed_tasks.append(f"- Task {task['id']}")
        completed = '\n'.join(completed_tasks) if completed_tasks else '(none)'

        # Format commits
        commits_list = []
        for commit in session_data['commits']:
            commits_list.append(f"- {commit['command']}")
        commits_str = '\n'.join(commits_list) if commits_list else '[]'

        # Format date/time
        if session_data['time_start']:
            try:
                dt = datetime.fromisoformat(session_data['time_start'].replace('Z', '+00:00'))
                date_str = dt.strftime('%Y-%m-%d')
                time_start_str = dt.strftime('%H:%M')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')
                time_start_str = 'unknown'
        else:
            date_str = datetime.now().strftime('%Y-%m-%d')
            time_start_str = 'unknown'

        if session_data['time_end']:
            try:
                dt = datetime.fromisoformat(session_data['time_end'].replace('Z', '+00:00'))
                time_end_str = dt.strftime('%H:%M')
            except:
                time_end_str = 'unknown'
        else:
            time_end_str = 'unknown'

        # Fill template
        handoff = template.format(
            session_id=session_data['session_id'],
            date=date_str,
            time_start=time_start_str,
            time_end=time_end_str,
            duration_minutes=session_data['duration_minutes'],
            project=session_data['project'],
            topic='[MANUAL: Enter topic/focus]',
            tags='[]',
            git_branch=session_data['git_branch'],
            commits=commits_str,
            title='[MANUAL: Enter title]',
            summary='[MANUAL: 1-2 sentence summary of what was accomplished]',
            completed=completed,
            in_progress='[MANUAL: What work is partially complete?]',
            next_steps='[MANUAL: What should be done next?]\n1. \n2. \n3. ',
            blockers='[MANUAL: What is blocking progress?]',
            decisions='[MANUAL: What decisions were made and why?]',
            files_modified=files_modified,
            commands_run=commands_run,
            context_notes='[MANUAL: Any other context worth preserving?]'
        )

        with open(output_path, 'w') as f:
            f.write(handoff)

        print(f"Handoff skeleton written to: {output_path}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: Template not found: {template_path}", file=sys.stderr)
    except Exception as e:
        print(f"Error: Failed to generate handoff: {e}", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        print("Usage: handoff-parser.py <transcript_path> [output_path]", file=sys.stderr)
        sys.exit(1)

    transcript_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    # Parse transcript
    session_data = parse_transcript(transcript_path)

    if output_path == '/dev/null':
        # Print JSON to stdout
        print(json.dumps(session_data, indent=2))
    elif output_path:
        # Generate handoff skeleton
        template_path = Path(__file__).parent / 'handoff.md.template'
        generate_handoff_skeleton(session_data, str(template_path), output_path)
    else:
        # Print JSON to stdout (default)
        print(json.dumps(session_data, indent=2))


if __name__ == '__main__':
    main()
