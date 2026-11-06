-- SOLO LECTURA. Ejecutar con la conexión local autorizada a la base sportlab.
BEGIN TRANSACTION READ ONLY;
SELECT rule_key,rule_version,active,rule,notes,updated_at
FROM core.framework_rules
WHERE active
ORDER BY rule_key;

WITH latest AS (
  SELECT DISTINCT ON (provider,resource_key)
    provider,resource_key,payload_hash,fetched_at,last_seen_at,source_url,payload
  FROM core.source_snapshots
  WHERE provider='SportLab_Universal'
    AND resource_key IN (
      'slate:2026-10-21:nba-nhl:attack-defense-sgp10:v1',
      'slate:2026-10-21:nba-nhl:conditional-selections:v1',
      'slate:2026-10-21:nba:starter-eligibility-review:v1'
    )
  ORDER BY provider,resource_key,fetched_at DESC
)
SELECT * FROM latest ORDER BY resource_key;
COMMIT;
