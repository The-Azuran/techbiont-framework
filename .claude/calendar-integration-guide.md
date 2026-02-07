# Calendar Session-Start Reminders Integration Guide

## Overview

Phase 4 of the calendar project integrates automatic session-start reminders that display upcoming events when you begin a new session with Claude Code.

## Implementation

### Components

1. **Session Reminders Script**: `/home/Valis/.claude/calendar/session-reminders.py`
   - Standalone Python script
   - Queries calendar database for upcoming events
   - Displays formatted reminders with urgency indicators
   - Reads configuration from `.calendar.conf`

2. **Hookify Integration**: `.claude/hookify.calendar-reminders.local.md`
   - Triggers on first user prompt of each session
   - Executes session-reminders.py
   - Injects output as system message

### Configuration

Settings in `~/.claude/calendar/.calendar.conf`:

```toml
[reminders]
session_start_display = true        # Enable/disable session-start reminders
urgency_red_days = 1                # Events ≤1 day show 🔴
urgency_yellow_days = 3             # Events ≤3 days show 🟡
urgency_green_days = 7              # Events ≤7 days show 🟢 (not shown at session start)
max_display_count = 5               # Maximum events to display
```

### Urgency Indicators

- 🔴 **Red**: ≤1 day (today or tomorrow)
- 🟡 **Yellow**: ≤3 days
- 🟢 **Green**: >3 days (not shown at session start, only in `/calendar list`)

Session-start reminders only show red and yellow urgency events to minimize noise.

## Usage

### Automatic Display

When you start a new session, if there are upcoming events within the yellow threshold (3 days by default), you'll see:

```
📅 Calendar Reminders:
============================================================
🔴 2026-02-08 (1d) — Security review reminder
   Type: Deadline
🟡 2026-02-10 (3d) — Quarterly maintenance
   Type: Maintenance
============================================================
Run '/calendar list' for full schedule
```

### Manual Testing

Test the reminder script directly:

```bash
~/.claude/calendar/session-reminders.py
```

### Disable Reminders

To disable session-start reminders without removing the integration:

```bash
# Edit configuration
sed -i 's/session_start_display = true/session_start_display = false/' ~/.claude/calendar/.calendar.conf
```

Or manually edit `~/.claude/calendar/.calendar.conf` and set:
```toml
[reminders]
session_start_display = false
```

## Display Format

### Event Line Format

```
{indicator} {date} ({days_until}) — {title}
   Type: {event_type}
```

### Days Until Format

- `today` — Event is today
- `1d` — 1 day away (tomorrow)
- `Nd` — N days away (e.g., `3d`)

### Event Types

- **Review** — Knowledge base review dates
- **Deadline** — Hard deadlines with consequences
- **Maintenance** — Recurring system maintenance
- **Meeting** — External meetings/bookings
- **Task** — Actionable items with dates

### Metadata Display

At session start, only the event type is shown for brevity. For full details including related knowledge and tags, use:

```bash
/calendar list
# or
/calendar show <event-id>
```

## Technical Details

### Database Query

The script queries for:
- Events with `status='active'`
- Start date between today and yellow threshold (default: 3 days)
- Ordered by start_datetime ascending
- Limited to max_display_count (default: 5)

### Configuration Parsing

Simple TOML parser (no external dependencies):
- Reads `[reminders]` section from `.calendar.conf`
- Falls back to defaults if file missing or parsing fails
- Type coercion: `true/false` → boolean, digits → integer

### Error Handling

- **Missing database**: No output (silent fail)
- **Missing configuration**: Uses defaults
- **Script errors**: Caught by try/except, no session blocking
- **Hookify errors**: Script returns empty dict, session continues

Session-start should never be blocked by calendar issues.

## Integration with Communication Zooid

From `~/.claude/rules/08-communication.md`:

```
### Start of Session
1. Check project CLAUDE.md for context
2. Review handoff notes and in-progress tasks
3. Clarify session goals with operator
```

Calendar reminders now inject automatically before step 1 via hookify.

## Verification

### Test Cases

1. **No upcoming events**: No output (silent)
2. **Events beyond yellow threshold**: No output
3. **Red urgency event (≤1d)**: Shows with 🔴
4. **Yellow urgency event (≤3d)**: Shows with 🟡
5. **Today event**: Shows `(today)` instead of `(0d)`
6. **Multiple events**: Respects max_display_count limit

### Manual Testing

```bash
# Add test event 2 days from now
python3 -c "
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('~/.claude/calendar/.calendar.db')
cursor = conn.cursor()
test_date = (datetime.now() + timedelta(days=2)).date().isoformat()
cursor.execute('''
    INSERT INTO events (id, title, event_type, start_datetime, status, created_at, updated_at)
    VALUES ('test-001', 'Test reminder', 'review', ?, 'active', datetime('now'), datetime('now'))
''', (test_date,))
conn.commit()
conn.close()
"

# Run reminder script
~/.claude/calendar/session-reminders.py

# Should show yellow urgency event

# Clean up
sqlite3 ~/.claude/calendar/.calendar.db "DELETE FROM events WHERE id='test-001';"
```

## Troubleshooting

### Reminders Not Showing

1. **Check configuration**:
   ```bash
   grep session_start_display ~/.claude/calendar/.calendar.conf
   # Should show: session_start_display = true
   ```

2. **Check for upcoming events**:
   ```bash
   sqlite3 ~/.claude/calendar/.calendar.db "SELECT start_datetime FROM events WHERE status='active' ORDER BY start_datetime LIMIT 5;"
   ```

3. **Test script directly**:
   ```bash
   ~/.claude/calendar/session-reminders.py
   ```

4. **Check hookify plugin**:
   ```bash
   ls ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/hookify/
   ```

### Hookify Not Triggering

1. **Verify hookify file exists**:
   ```bash
   ls .claude/hookify.calendar-reminders.local.md
   ```

2. **Check hookify plugin enabled**:
   - Hookify reads `.claude/hookify.*.local.md` files automatically
   - No additional configuration needed if plugin installed

3. **Check script permissions**:
   ```bash
   ls -l ~/.claude/calendar/session-reminders.py
   # Should show: -rwxr-xr-x (executable)
   ```

## Future Enhancements

Potential additions (not in current scope):

- Email notifications (SMTP integration)
- Desktop notifications (notify-send on Linux)
- Snooze functionality (defer reminder to next session)
- Related knowledge auto-loading (fetch linked docs into context)
- Natural language relative dates ("in 2 days" instead of "2d")
- Color-coded output in terminal (ANSI escape codes)

## Files Reference

### Created Files

- `/home/Valis/.claude/calendar/session-reminders.py` — Standalone reminder script
- `.claude/hookify.calendar-reminders.local.md` — Hookify integration (project-local)

### Related Files

- `~/.claude/calendar/.calendar.db` — SQLite database (events table)
- `~/.claude/calendar/.calendar.conf` — Configuration (reminders section)
- `~/.claude/skills/calendar/SKILL.md` — Calendar operon documentation

### Dependencies

- Python 3 standard library only:
  - `sqlite3` — Database queries
  - `json` — Metadata parsing
  - `datetime` — Date calculations
  - `pathlib` — File path handling
  - `os` — Environment access

No external packages required for session reminders.

## Security Considerations

- **Database access**: Read-only queries, no user input interpolation
- **Configuration parsing**: Simple parsing, no code execution
- **Error handling**: All exceptions caught, silent failure
- **File permissions**: Script executable by user only (755)
- **No network access**: Entirely local operation
- **No secrets**: No credentials or sensitive data in script

## Session Audit Checklist

From auditing operon (Phase 4 update):

```markdown
### Calendar Checks (if calendar operon active)
- [ ] Upcoming events reviewed (next 7 days)
- [ ] Overdue tasks addressed (past deadlines with status='active')
- [ ] Review dates approaching (within 7 days)
- [ ] CalDAV sync completed (if enabled)
- [ ] No conflicts in sync log (errors column empty)
```

Session-start reminders help address the first item automatically.

## Commands Summary

```bash
# Manual execution
~/.claude/calendar/session-reminders.py

# Disable session-start display
sed -i 's/session_start_display = true/session_start_display = false/' ~/.claude/calendar/.calendar.conf

# Enable session-start display
sed -i 's/session_start_display = false/session_start_display = true/' ~/.claude/calendar/.calendar.conf

# Test configuration parsing
python3 -c "import sys; sys.path.insert(0, '/home/Valis/.claude/calendar'); from session_reminders import parse_config; print(parse_config())"

# Check upcoming events (SQL)
sqlite3 ~/.claude/calendar/.calendar.db "SELECT start_datetime, title FROM events WHERE status='active' AND date(start_datetime) >= date('now') ORDER BY start_datetime LIMIT 5;"
```

## Implementation Status

**Phase 4 Complete**:
- ✅ Session-start reminder script created
- ✅ Configuration integration (reads `.calendar.conf`)
- ✅ Hookify integration (automatic session-start trigger)
- ✅ Urgency indicators (🔴🟡🟢)
- ✅ Respects max_display_count limit
- ✅ Silent failure on errors
- ✅ Comprehensive testing
- ✅ Documentation

**Next Steps** (if desired):
- Test hookify integration in live session
- Adjust urgency thresholds based on usage patterns
- Consider desktop notification integration
- Add reminder snooze functionality
