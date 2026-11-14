"""
Smoke tests for the Streamlit app: the page must render without exceptions
for both targets and every preset (engine tests alone do not catch UI crashes).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit.testing.v1 import AppTest

from presets import MOON_PRESETS, MARS_PRESETS, MOON_TARGET, MARS_TARGET

APP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.py")


class TestStreamlitApp(unittest.TestCase):

    def test_app_renders_all_targets_and_presets(self):
        at = AppTest.from_file(APP_PATH, default_timeout=60)
        at.run()
        self.assertFalse(at.exception, [e.message for e in at.exception])
        self.assertEqual(len(at.tabs), 4)

        for target, presets in [(MOON_TARGET, MOON_PRESETS), (MARS_TARGET, MARS_PRESETS)]:
            at.sidebar.radio[1].set_value(target).run()
            self.assertFalse(at.exception, f"{target}: {[e.message for e in at.exception]}")
            for preset in presets:
                at.sidebar.selectbox[0].set_value(preset).run()
                self.assertFalse(at.exception, f"{target}/{preset}: {[e.message for e in at.exception]}")

            # Hand-estimate mode, overlap correction and both portfolio sizes must also render.
            at.sidebar.radio[2].set_value("Estimates").run()
            self.assertFalse(at.exception, f"{target}/estimates: {[e.message for e in at.exception]}")
            at.sidebar.toggle[0].set_value(True).run()
            self.assertFalse(at.exception, f"{target}/dedupe: {[e.message for e in at.exception]}")
            at.sidebar.radio[3].set_value(3).run()
            self.assertFalse(at.exception, f"{target}/k=3: {[e.message for e in at.exception]}")
            at.sidebar.radio[2].set_value("Measured").run()
            at.sidebar.toggle[0].set_value(False).run()
            at.sidebar.radio[3].set_value(2).run()


if __name__ == "__main__":
    unittest.main()
