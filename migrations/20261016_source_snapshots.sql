CREATE TABLE IF NOT EXISTS core.source_snapshots (
    provider text NOT NULL,
    resource_key text NOT NULL,
    payload_hash text NOT NULL,
    fetched_at timestamptz NOT NULL,
    last_seen_at timestamptz NOT NULL,
    source_url text NOT NULL,
    payload jsonb NOT NULL,
    PRIMARY KEY (provider, resource_key, fetched_at),
    CHECK (last_seen_at >= fetched_at)
);
CREATE INDEX IF NOT EXISTS source_snapshots_latest
    ON core.source_snapshots (provider, resource_key, fetched_at DESC);
