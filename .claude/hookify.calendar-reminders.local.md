---
event: prompt
priority: 100
---

# Calendar Session-Start Reminders

## Matcher

```python
def match(context):
    """
    Display calendar reminders at the start of a new session.
    Only run on first prompt of a session.
    """
    # Check if this is the first user prompt in the session
    conversation = context.get('conversation', {})
    messages = conversation.get('messages', [])

    # Count user messages (excluding system messages)
    user_message_count = sum(1 for msg in messages if msg.get('role') == 'user')

    # Only run on first user message
    return user_message_count <= 1
```

## Action

```python
import subprocess
import os

def execute(context):
    """
    Execute session-reminders.py script to display upcoming calendar events.
    """
    script_path = os.path.expanduser('~/.claude/calendar/session-reminders.py')

    if not os.path.exists(script_path):
        return {}

    try:
        # Run the calendar reminder script
        result = subprocess.run(
            [script_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        # If there's output, inject it as a system message
        if result.stdout.strip():
            return {
                'systemMessage': result.stdout
            }
    except Exception:
        # Fail silently - calendar reminders should not block session start
        pass

    return {}
```
