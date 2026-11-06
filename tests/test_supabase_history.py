import os
import sys
import types
import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from sportlab.data.supabase_history import pitcher_strikeout_frequency


class SupabaseHistoryTests(unittest.TestCase):
    def test_reads_only_pregame_logs_and_reports_ambiguous_exclusions(self):
        cursor = MagicMock()
        cursor.__enter__.return_value = cursor
        cursor.fetchone.return_value = {
            "pitcher_games": 29, "pitcher_hits": 16,
            "opponent_games": 129, "opponent_hits": 67,
            "league_games": 3823, "league_hits": 1441,
            "ambiguous_rows_excluded": 435, "missing_game_id_rows_excluded": 0,
        }
        connection = MagicMock()
        connection.__enter__.return_value = connection
        connection.cursor.return_value = cursor
        fake_psycopg = types.ModuleType("psycopg")
        fake_psycopg.connect = MagicMock(return_value=connection)
        fake_psycopg.rows = types.ModuleType("psycopg.rows")
        fake_psycopg.rows.dict_row = object()

        with patch.dict(os.environ, {"SPORTLAB_SUPABASE_DATABASE_URL": "postgresql://placeholder"}), \
                patch.dict(sys.modules, {"psycopg": fake_psycopg, "psycopg.rows": fake_psycopg.rows}):
            result = pitcher_strikeout_frequency("Cade Cavalli", "NYY", date(2026, 9, 11),
                                                  2026, 5.5, simulations=100, seed=1)

        self.assertEqual(result["subject"]["games"], 29)
        self.assertEqual(result["opponent_allowed"]["games"], 129)
        self.assertEqual(result["ambiguous_rows_excluded"], 435)
        self.assertEqual(cursor.execute.call_args_list[0].args[0], "SET TRANSACTION READ ONLY")
        statement, parameters = cursor.execute.call_args_list[1].args
        self.assertIn("rows_per_game_and_rival = 1", statement)
        self.assertEqual(parameters[:2], (2026, date(2026, 9, 11)))

    def test_whole_strikeout_line_is_rejected_before_connecting(self):
        with self.assertRaises(ValueError):
            pitcher_strikeout_frequency("Pitcher", "NYY", date(2026, 9, 11), 2026, 5.0)


if __name__ == "__main__":
    unittest.main()
