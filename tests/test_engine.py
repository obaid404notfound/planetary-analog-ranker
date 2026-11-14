"""
Unit tests for Analog Ranker Hackathon Core Engine.
Includes the official NASA Hackathon Guide worked example test (Page 3),
preset validity checks, calibration site checks, and stability tests.
"""

import os
import sys
import unittest
import numpy as np
import pandas as pd

# Works from any folder and on any OS: find the project root from this file's location.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def data_path(name: str) -> str:
    return os.path.join(ROOT, "data", name)


from engine import (
    analog_score, aridity_score, best_portfolio, cold_score, deduplicated_weights, first_place_share,
    normalize_weights, overlapping_pairs, polar_score_from_latitude, portfolio, rank_stability,
    rank_stability_local, relief_score, accessibility_score, crater_score, isolation_score, uv_score,
)
from presets import (
    MOON_PRESETS, MARS_PRESETS,
    MOON_CRITERIA_INFO, MARS_CRITERIA_INFO,
    MOON_MEASURED_TARGET, MARS_MEASURED_TARGET
)


class TestAnalogRankerEngine(unittest.TestCase):
    
    def test_nasa_guide_page3_worked_example(self):
        """
        Worked example from Guide Page 3:
        'Worked example (Moon): scores of Cold 85, Aridity 90, Radiation 70, Surface 80,
        Topography 75, Isolation 60, Polar 50, Accessibility 80 give a final score of 75.5
        (the NASA guide prints 76.0, but the weighted sum is 75.5; use this as your first unit test).'
        """
        weights = {
            "Extreme cold and temperature range": 15.0,
            "Aridity / low humidity": 15.0,
            "High radiation / UV": 10.0,
            "Rocky / regolith-like surface": 15.0,
            "Topographic complexity": 15.0,
            "Isolation": 10.0,
            "Polar / high-latitude conditions": 10.0,
            "Accessibility for testing": 10.0
        }
        
        df = pd.DataFrame([{
            "Extreme cold and temperature range": 85.0,
            "Aridity / low humidity": 90.0,
            "High radiation / UV": 70.0,
            "Rocky / regolith-like surface": 80.0,
            "Topographic complexity": 75.0,
            "Isolation": 60.0,
            "Polar / high-latitude conditions": 50.0,
            "Accessibility for testing": 80.0
        }])
        
        score_series = analog_score(df, weights)
        calculated_score = float(score_series.iloc[0])
        self.assertAlmostEqual(calculated_score, 75.5, places=2)
        print(f"\n[PASS] NASA Worked Example Test: calculated score = {calculated_score:.2f} (expected 75.5)")

    def test_weight_normalization(self):
        """Weights should sum to 1.0 regardless of input scale."""
        raw_weights = {"A": 30.0, "B": 20.0, "C": 50.0}
        norm = normalize_weights(raw_weights)
        self.assertAlmostEqual(sum(norm.values()), 1.0)
        self.assertAlmostEqual(norm["A"], 0.3)
        self.assertAlmostEqual(norm["B"], 0.2)
        self.assertAlmostEqual(norm["C"], 0.5)

    def test_portfolio_greedy_selection(self):
        """Verify greedy portfolio coverage algorithm."""
        df = pd.DataFrame([
            {"site": "Site1", "c1": 90.0, "c2": 20.0, "c3": 30.0},
            {"site": "Site2", "c1": 85.0, "c2": 15.0, "c3": 25.0},
            {"site": "Site3", "c1": 10.0, "c2": 95.0, "c3": 10.0},
            {"site": "Site4", "c1": 20.0, "c2": 10.0, "c3": 95.0},
        ], index=["S1", "S2", "S3", "S4"])
        
        weights = {"c1": 33.33, "c2": 33.33, "c3": 33.34}
        chosen, covered, missing = portfolio(df, weights, k=3, thr=70.0)
        
        self.assertEqual(len(chosen), 3)
        self.assertEqual(chosen[0], "S1")
        self.assertIn("S3", chosen)
        self.assertIn("S4", chosen)
        self.assertEqual(len(missing), 0)

    def test_portfolio_gap_reporting(self):
        """Verify criteria remaining below threshold are reported in missing list."""
        df = pd.DataFrame([
            {"c1": 90.0, "c2": 50.0},
            {"c1": 80.0, "c2": 60.0},
        ], index=["A", "B"])
        
        weights = {"c1": 50.0, "c2": 50.0}
        chosen, covered, missing = portfolio(df, weights, k=2, thr=70.0)
        self.assertIn("c2", missing)
        self.assertNotIn("c1", missing)

    def test_rank_stability_dirichlet(self):
        """Verify Dirichlet Monte Carlo stability generates valid persistence probabilities."""
        cols = ["c1", "c2", "c3"]
        df = pd.DataFrame({
            "c1": [95, 80, 50, 20, 10],
            "c2": [90, 85, 45, 30, 15],
            "c3": [92, 88, 55, 25, 5]
        }, index=["top1", "top2", "mid", "low1", "low2"])
        
        for n in [1, 2, 3]:
            stability = rank_stability(df, cols, num_runs=500, top_n=n, seed=42)
            self.assertEqual(len(stability), len(df))
            self.assertTrue((stability >= 0.0).all() and (stability <= 100.0).all())

    def test_all_presets_and_data_files(self):
        """Validate that all presets in Moon and Mars sum to 100% and score candidate CSV datasets without error."""
        moon_df = pd.read_csv(data_path("moon_sites.csv"))
        mars_df = pd.read_csv(data_path("mars_sites.csv"))
        
        # Test Moon Presets
        for p_name, weights in MOON_PRESETS.items():
            self.assertAlmostEqual(sum(weights.values()), 100.0, places=1, msg=f"Moon preset {p_name} does not sum to 100")
            scores = analog_score(moon_df, normalize_weights(weights))
            self.assertEqual(len(scores), len(moon_df))
            self.assertTrue((scores >= 0.0).all() and (scores <= 100.0).all())

        # Test Mars Presets
        for p_name, weights in MARS_PRESETS.items():
            self.assertAlmostEqual(sum(weights.values()), 100.0, places=1, msg=f"Mars preset {p_name} does not sum to 100")
            scores = analog_score(mars_df, normalize_weights(weights))
            self.assertEqual(len(scores), len(mars_df))
            self.assertTrue((scores >= 0.0).all() and (scores <= 100.0).all())

    def test_best_portfolio_never_worse_than_greedy(self):
        """Exhaustive search must match or beat greedy, and strictly beat it on a known case."""
        from engine import portfolio_value
        for target_csv, presets in [(data_path("moon_sites.csv"), MOON_PRESETS), (data_path("mars_sites.csv"), MARS_PRESETS)]:
            df = pd.read_csv(target_csv)
            df = df[df["site_id"] != "worked_example"].reset_index(drop=True)
            for weights in presets.values():
                nw = normalize_weights(weights)
                for k in (2, 3):
                    g, _, _ = portfolio(df, nw, k=k)
                    _, _, _, best = best_portfolio(df, nw, k=k)
                    self.assertGreaterEqual(best + 1e-9, portfolio_value(df, nw, g))
        df = pd.DataFrame({"a": [100, 60, 60], "b": [0, 100, 0], "c": [0, 0, 100]})
        w = {"a": 1.0, "b": 1.0, "c": 1.0}
        self.assertEqual(sorted(best_portfolio(df, w, k=2)[0]), [1, 2])

    def test_polar_score_from_latitude(self):
        self.assertEqual(polar_score_from_latitude(0), 0.0)
        self.assertEqual(polar_score_from_latitude(-90), 100.0)
        self.assertGreater(polar_score_from_latitude(-77.5), polar_score_from_latitude(46.6))

    def test_first_place_share(self):
        """A clear leader wins every noisy trial; two equal sites split the wins."""
        w = {"a": 1.0, "b": 1.0}
        clear = pd.DataFrame({"a": [90.0, 50.0], "b": [90.0, 50.0]})
        self.assertEqual(first_place_share(clear, w, error=5.0)[0], 100.0)
        tied = pd.DataFrame({"a": [80.0, 80.0], "b": [80.0, 80.0]})
        share = first_place_share(tied, w, error=5.0)
        self.assertAlmostEqual(share.sum(), 100.0)
        self.assertTrue(30.0 < share[0] < 70.0)

    def test_rank_stability_local_follows_the_weights(self):
        """With all weight on one criterion, the best site on it must stay first."""
        df = pd.DataFrame({"a": [100.0, 10.0, 10.0], "b": [10.0, 100.0, 10.0], "c": [10.0, 10.0, 100.0]})
        rate = rank_stability_local(df, {"a": 1.0, "b": 0.0, "c": 0.0}, top_n=1)
        self.assertGreater(rate[0], 95.0)

    def test_overlap_and_deduplicated_weights(self):
        df = pd.DataFrame({"a": [1.0, 2, 3, 4], "b": [2.0, 4, 6, 8], "c": [4.0, 1, 3, 2], "d": [8.0, 6, 4, 2]})
        pairs = overlapping_pairs(df, ["a", "b", "c", "d"], 0.8)
        self.assertIn(("a", "b"), [(x, y) for x, y, _ in pairs])
        w = deduplicated_weights({"a": 0.25, "b": 0.25, "c": 0.25, "d": 0.25}, pairs)
        self.assertAlmostEqual(sum(w.values()), 1.0)
        self.assertAlmostEqual(w["a"], w["b"])
        self.assertLess(w["a"], w["c"])          # the doubled pair loses weight
        self.assertAlmostEqual(w["c"], w["d"])    # opposites (a/b vs d) are not penalised

    def test_measured_score_functions(self):
        self.assertEqual(cold_score(25.0), 0.0)
        self.assertEqual(cold_score(-70.0), 100.0)
        self.assertEqual(aridity_score(0.0), 100.0)
        self.assertEqual(aridity_score(1000.0), 0.0)
        self.assertGreater(aridity_score(10.0), aridity_score(100.0))
        self.assertEqual(relief_score(0.0), 0.0)
        self.assertGreater(relief_score(400.0), relief_score(40.0))

    def test_distance_based_scores(self):
        self.assertEqual(isolation_score(2.0), 0.0)
        self.assertEqual(isolation_score(1500.0), 100.0)
        self.assertGreater(accessibility_score(10.0, 0.5), accessibility_score(500.0, 50.0))
        self.assertAlmostEqual(accessibility_score(10.0, 0.5), 100.0)
        self.assertAlmostEqual(accessibility_score(3000.0, 500.0), 0.0)
        self.assertEqual(crater_score(0.4, 24.0), 100.0)           # inside a 24 km crater
        self.assertAlmostEqual(crater_score(45.0, 0.0), 50.0)      # 40 km beyond a small one
        self.assertEqual(uv_score(0.0), 0.0)
        self.assertEqual(uv_score(4.0), 100.0)

    def test_every_measured_criterion_has_its_columns(self):
        """Each measured criterion must name a real engine function and columns present in measured.csv."""
        import engine
        from presets import MEASURED_CRITERIA, ACCESS_SPEC, CROSS_CHECK
        measured = pd.read_csv(data_path("measured.csv"), keep_default_na=False)
        specs = [s for t in MEASURED_CRITERIA.values() for s in t.values()] + [ACCESS_SPEC]
        for spec in specs:
            self.assertTrue(callable(getattr(engine, spec["fn"])))
            for col in spec["cols"]:
                self.assertIn(col, measured.columns)
            for _, row in measured.iterrows():
                score = getattr(engine, spec["fn"])(*[row[c] for c in spec["cols"]])
                self.assertTrue(0.0 <= score <= 100.0, (spec["fn"], row["site_id"], score))
        for cols in CROSS_CHECK.values():
            self.assertIn(cols["main"], measured.columns)
            self.assertIn(cols["other"], measured.columns)

    def test_measured_data_covers_every_site(self):
        measured = pd.read_csv(data_path("measured.csv"))
        for f in (data_path("moon_sites.csv"), data_path("mars_sites.csv")):
            ids = set(pd.read_csv(f)["site_id"]) - {"worked_example"}
            self.assertTrue(ids <= set(measured["site_id"]), f)

    def test_mars_keeps_guide_criteria_and_has_accessibility_data(self):
        """Mars is scored on the guide's 8 criteria; accessibility is data only, reported separately."""
        self.assertEqual(len(MARS_CRITERIA_INFO), 8)
        self.assertNotIn("Accessibility for testing", MARS_CRITERIA_INFO)
        self.assertEqual(MARS_PRESETS["Balanced (NASA Baseline)"]["Extreme aridity"], 18.0)
        self.assertIn("Accessibility for testing", pd.read_csv(data_path("mars_sites.csv")).columns)

    def test_calibration_sites_present(self):
        """Verify the 3 calibration sites exist in both datasets."""
        moon_df = pd.read_csv(data_path("moon_sites.csv"))
        mars_df = pd.read_csv(data_path("mars_sites.csv"))
        for s_id in ["mcmurdo", "haughton", "atacama"]:
            self.assertIn(s_id, moon_df["site_id"].values)
            self.assertIn(s_id, mars_df["site_id"].values)


if __name__ == "__main__":
    unittest.main()
