-- Schema version tracking
CREATE TABLE schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO schema_version (version) VALUES (1);

-- Core events table
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK(event_type IN ('review', 'deadline', 'maintenance', 'meeting', 'task')),
    start_datetime TEXT NOT NULL,
    end_datetime TEXT,
    all_day INTEGER DEFAULT 0 CHECK(all_day IN (0, 1)),
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'cancelled')),
    caldav_uid TEXT UNIQUE,
    caldav_etag TEXT,
    source TEXT DEFAULT 'internal' CHECK(source IN ('internal', 'caldav', 'calcom')),
    metadata TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Reminders table
CREATE TABLE reminders (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    reminder_datetime TEXT NOT NULL,
    sent INTEGER DEFAULT 0 CHECK(sent IN (0, 1)),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- CalDAV sync log
CREATE TABLE sync_log (
    id TEXT PRIMARY KEY,
    sync_datetime TEXT NOT NULL,
    direction TEXT NOT NULL CHECK(direction IN ('pull', 'push', 'bidirectional')),
    events_added INTEGER DEFAULT 0,
    events_updated INTEGER DEFAULT 0,
    events_deleted INTEGER DEFAULT 0,
    conflicts INTEGER DEFAULT 0,
    errors TEXT
);

-- Indexes for performance
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_start ON events(start_datetime ASC);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_source ON events(source);
CREATE INDEX idx_events_caldav_uid ON events(caldav_uid);
CREATE INDEX idx_reminders_event ON reminders(event_id);
CREATE INDEX idx_reminders_datetime ON reminders(reminder_datetime ASC);
CREATE INDEX idx_sync_log_datetime ON sync_log(sync_datetime DESC);

-- Enable WAL mode for better concurrency
PRAGMA journal_mode=WAL;
