# Legacy StrikeoutLab material

The existing packages/ and supabase/ directories come from the original MLB-only StrikeoutLab project.

They are retained temporarily because they contain useful tested strikeout/calibration logic, SQL migrations and source-history needed for audit and migration.

Rules:
- no new universal features should be added there;
- migrate useful logic into sportlab/ with tests;
- Neon SportLab is the primary dynamic database;
- Supabase StrikeoutLab is historical/auxiliary only;
- once migrated and validated, legacy files may be archived or removed in a later cleanup commit.
