import unittest

from sportlab.models.threshold_frequency import EventFrequency, estimate_threshold


class ThresholdFrequencyTests(unittest.TestCase):
    def test_more_games_are_evidence_not_the_number_of_simulations(self):
        result = estimate_threshold(EventFrequency(50, 70, "MLB team runs >3.5"), EventFrequency(40, 50, "MLB team runs >3.5"),
                                    0.5, simulations=10_000, seed=42)
        self.assertEqual(result["subject"]["observed"], 50 / 70)
        self.assertEqual(result["opponent_allowed"]["observed"], 0.8)
        self.assertEqual(result["simulations"], 10_000)
        self.assertAlmostEqual(result["matchup_estimate"], ((50 + 10) / 90 + (40 + 10) / 70) / 2)
        self.assertLess(abs(result["simulated_frequency"] - result["matchup_estimate"]), 0.02)
        self.assertEqual(result, estimate_threshold(EventFrequency(50, 70, "MLB team runs >3.5"), EventFrequency(40, 50, "MLB team runs >3.5"),
                                                    0.5, simulations=10_000, seed=42))


    def test_stingy_opponent_lowers_estimate_without_a_fixed_percentage_penalty(self):
        subject = EventFrequency(50, 70, "MLB team runs >3.5")
        easy = estimate_threshold(subject, EventFrequency(40, 50, subject.event_key), 0.5, simulations=100)
        difficult = estimate_threshold(subject, EventFrequency(10, 50, subject.event_key), 0.5, simulations=100)
        self.assertLess(difficult["matchup_estimate"], easy["matchup_estimate"])


    def test_invalid_samples_or_priors_fail_instead_of_producing_a_pick(self):
        with self.assertRaises(ValueError):
            EventFrequency(8, 7, "K >5.5")
        with self.assertRaises(ValueError):
            estimate_threshold(EventFrequency(6, 7, "goals >1.5"), EventFrequency(12, 13, "goals >1.5"), 0)
        with self.assertRaises(ValueError):
            estimate_threshold(EventFrequency(6, 7, "goals >1.5"),
                               EventFrequency(12, 13, "goal conceded >0.5"), 0.5)


if __name__ == "__main__":
    unittest.main()
