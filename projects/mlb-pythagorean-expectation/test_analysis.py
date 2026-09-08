"""Offline regression tests for the published method and retained results."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import pandas as pd
import requests
from analyze import PROJECT_DIR, calculate_expectation, fetch_standings, save_chart
from reproduce import INPUT_COLUMNS, load_snapshot


class AnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved = pd.read_csv(PROJECT_DIR / "data/mlb_pythagorean_2025.csv")
        cls.inputs = load_snapshot(PROJECT_DIR / "data/mlb_pythagorean_2025.csv")

    def test_thirty_distinct_complete_team_records(self):
        self.assertEqual(len(self.inputs), 30)
        self.assertEqual(self.inputs.team.nunique(), 30)
        self.assertTrue(((self.inputs.wins + self.inputs.losses) == 162).all())

    def test_equal_runs_produce_half_expected_wins(self):
        sample = pd.DataFrame([dict(team="Synthetic Team", division="Test", wins=90, losses=72, runs_scored=700, runs_allowed=700)])
        row = calculate_expectation(sample).iloc[0]
        self.assertAlmostEqual(row.expected_win_pct, 0.5)
        self.assertAlmostEqual(row.expected_wins, 81)
        self.assertAlmostEqual(row.wins_above_expectation, 9)

    def test_calculation_matches_all_retained_derived_fields(self):
        actual = calculate_expectation(self.inputs).set_index("team").sort_index()
        expected = self.saved.set_index("team").sort_index()
        for field in ["actual_win_pct", "expected_win_pct", "difference", "expected_wins", "wins_above_expectation"]:
            self.assertLessEqual(float((actual[field] - expected[field]).abs().max()), 0.000051, field)

    def test_sort_order_and_input_immutability(self):
        before = self.inputs.copy(deep=True)
        result = calculate_expectation(self.inputs)
        self.assertTrue(result.difference.is_monotonic_decreasing)
        self.assertEqual(result.iloc[0].team, "Los Angeles Angels")
        self.assertEqual(result.iloc[-1].team, "Chicago White Sox")
        pd.testing.assert_frame_equal(self.inputs, before)

    def test_invalid_snapshot_rejected(self):
        bad_frames = [self.inputs.iloc[:-1], self.inputs.assign(runs_scored=-1), self.inputs.drop(columns="wins")]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            for frame in bad_frames:
                frame.to_csv(path, index=False)
                with self.assertRaises(ValueError):
                    load_snapshot(path)

    def test_api_mapping_without_network(self):
        records = [{"team": {"name": r.team, "division": {"name": r.division}}, "wins": int(r.wins), "losses": int(r.losses), "runsScored": int(r.runs_scored), "runsAllowed": int(r.runs_allowed)} for r in self.inputs.itertuples()]
        response = Mock()
        response.json.return_value = {"records": [{"teamRecords": records}]}
        with patch("analyze.requests.get", return_value=response) as get:
            actual = fetch_standings(2025)
            self.assertEqual(get.call_args.kwargs["params"]["season"], 2025)
            self.assertEqual(get.call_args.kwargs["timeout"], 30)
        pd.testing.assert_frame_equal(actual[INPUT_COLUMNS], self.inputs.reset_index(drop=True))

    def test_http_failure_propagates(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("Synthetic 503")
        with patch("analyze.requests.get", return_value=response):
            with self.assertRaises(requests.HTTPError):
                fetch_standings(2025)

    def test_chart_is_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chart.png"
            save_chart(calculate_expectation(self.inputs), 2025, path)
            self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertGreater(path.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
