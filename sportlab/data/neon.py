from __future__ import annotations
import json, os
from contextlib import contextmanager

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:
    psycopg = None
    dict_row = None

@contextmanager
def connect():
    url = os.environ.get("SPORTLAB_DATABASE_URL")
    if not url:
        raise RuntimeError("SPORTLAB_DATABASE_URL is not set")
    if psycopg is None:
        raise RuntimeError("Install psycopg[binary] to use the Neon adapter")
    with psycopg.connect(url) as conn:
        yield conn

def latest_form_snapshot(team_code: str, season_label: str, as_of_date: str):
    sql = """
    SELECT window_size, sample_games, offense_rate, defense_allowed_rate,
           form_differential, scoring_environment, win_rate, status, as_of_date
    FROM core.form_strength_snapshots
    WHERE sport_code='MLB' AND subject_type='team' AND subject_key=%s
      AND season_label=%s AND as_of_date <= %s
    ORDER BY as_of_date DESC, window_size
    """
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql,(team_code,season_label,as_of_date))
        return list(cur.fetchall())

def pitcher_vs_opponent(pitcher_name: str, opponent_team_code: str, as_of_date: str):
    sql = """
    SELECT * FROM mlb.pitcher_opponent_matchup_snapshots
    WHERE pitcher_name=%s AND opponent_team_code=%s AND as_of_date <= %s
    ORDER BY as_of_date DESC LIMIT 1
    """
    with connect() as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql,(pitcher_name,opponent_team_code,as_of_date))
        return cur.fetchone()

def save_simulation(event_id: int, simulations: int, seed: int, inputs: dict, outputs: dict, contradictions: list[str]) -> int:
    sql = """
    INSERT INTO core.simulation_runs
      (event_id, model_config_id, runs, provisional, inputs, outputs, contradiction_notes, status)
    VALUES (%s,NULL,%s,FALSE,%s::jsonb,%s::jsonb,%s::jsonb,'completed_mc_verified')
    RETURNING id
    """
    with connect() as conn, conn.cursor() as cur:
        cur.execute(sql,(event_id,simulations,json.dumps({**inputs,"seed":seed,"actually_executed":True}),json.dumps(outputs),json.dumps(contradictions)))
        sim_id = int(cur.fetchone()[0])
        conn.commit()
        return sim_id
