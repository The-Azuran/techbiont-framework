-- Schema version tracking
CREATE TABLE schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO schema_version (version) VALUES (1);

-- Core artifacts table
CREATE TABLE artifacts (
    id TEXT PRIMARY KEY,
    path TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT,
    description TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    promoted_from TEXT,
    source_session TEXT,
    domain TEXT,
    tags TEXT,
    metadata TEXT,
    status TEXT DEFAULT 'active'
);

-- Full-text search index
CREATE VIRTUAL TABLE artifacts_fts USING fts5(
    title,
    description,
    content,
    tags,
    content='artifacts',
    content_rowid='rowid'
);

-- Session archives
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    project_path TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    archived_at TEXT,
    artifact_count INTEGER DEFAULT 0,
    summary TEXT,
    metadata TEXT
);

-- Symlinks tracking
CREATE TABLE symlinks (
    id TEXT PRIMARY KEY,
    artifact_id TEXT NOT NULL,
    target_path TEXT NOT NULL,
    created_at TEXT NOT NULL,
    project_path TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifacts(id)
);

-- Retention policy tracking
CREATE TABLE retention_log (
    artifact_id TEXT NOT NULL,
    action TEXT NOT NULL,
    reason TEXT,
    executed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artifact_id) REFERENCES artifacts(id)
);

-- Indexes for performance
CREATE INDEX idx_artifacts_type ON artifacts(type);
CREATE INDEX idx_artifacts_created ON artifacts(created_at DESC);
CREATE INDEX idx_artifacts_status ON artifacts(status);
CREATE INDEX idx_artifacts_session ON artifacts(source_session);
CREATE INDEX idx_sessions_project ON sessions(project_path);
CREATE INDEX idx_sessions_ended ON sessions(ended_at DESC);
CREATE INDEX idx_symlinks_artifact ON symlinks(artifact_id);
