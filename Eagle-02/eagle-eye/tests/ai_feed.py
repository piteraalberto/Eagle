"""TEST ONLY - not part of the real application.

Feeds the AI confidence chart with fake data (a random walk) so the chart can be
checked without the real model. Run from the project root with:  python -m tests.ai_feed

The real application must call model.push(value) with the model's inference value
instead; this folder can then be deleted.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # lets this file run directly too

from main import build_app  # noqa: E402

START_VALUE = 0.5      # first fake inference value
MAX_STEP = 0.06        # maximum change between two consecutive values
INTERVAL_MS = 50       # time between two fake values


def start_random_walk(app, model):
    """Push one random-walk value every INTERVAL_MS using Tk's timer (no threads).

    Values are only generated while the chart is running (START clicked).
    """
    state = {"value": START_VALUE}

    def tick():
        if model.running:
            advance()
        app.root.after(INTERVAL_MS, tick)

    def advance():
        step = random.uniform(-MAX_STEP, MAX_STEP)
        state["value"] = min(1.0, max(0.0, state["value"] + step))
        model.push(state["value"])

    app.root.after(INTERVAL_MS, tick)


if __name__ == "__main__":
    app, model = build_app()
    start_random_walk(app, model)
    app.run()
