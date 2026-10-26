"""Position, label and color of every button.

Button ids are the 1-based positions in BUTTONS: append new buttons at the end
so that the ids of the existing ones do not change.
"""

from frontend.buttons.button import column, make_button
from frontend.theme import RED, YELLOW

# START / PAUSE of the AI chart, driven by AiControls
AI_PAUSE_BUTTON = make_button("PAUSE", x=382, y=722, w=58, inset=6)
AI_START_BUTTON = make_button("START", x=460, y=722, w=58, inset=6)

BUTTONS = (
    # Wide buttons (right panel, top)
    column(2039, 544, 129, 7, ["NEW CLASS", "NEW TRACKER", "START", "PAUSE"])
    + column(2421, 544, 129, 7, ["CLASS 1", "CLASS 2", "CLASS 3", "CLASS 4"])

    # Toggle grid (right panel, bottom)
    + column(2039, 709, 120, 2, ["PATH", "FLAG 1", "FLAG 2", "ARENA", "EAGLE"])
    + column(2169, 709, 120, 2, ["ENEMIES", "ALLIES", "CENTER", "START REC", "PAUSE REC"])
    + column(2300, 709, 120, 2, ["SCOPE", "VEL VECTOR", "BOUNDARIES", "TAPNET", "OVERLAY"])
    + column(2430, 709, 120, 2, ["FPS", "LAT", "INF", "SAVE LOG", "LOAD"])

    # Left panel: robot control
    + [make_button("BOT DETECTION", 12, 92, 175, 8),
       make_button("BOT AVOIDANCE", 12, 128, 175, 8),
       make_button("TRAJECTORY PLANNER", 12, 164, 175, 0)]
    + column(12, 200, 175, 8, ["TEST", "ARM", "AUTO", "MANUAL", "SHUT DOWN", "EMERGENCY"],
             colors={5: RED})

    # Left panel: strategy
    + column(283, 92, 175, 8,
             ["FLAG RECOGNITION", "PROTECT FLAG", "STEAL FLAG", "TURRET AUTO", "TURRET MANUAL",
              "FIRE", "FLIP", "ROCK", "ANTI SUMO"],
             colors={5: YELLOW, 6: YELLOW, 7: YELLOW, 8: YELLOW})

    # EDIT buttons next to each control
    + column(198, 92, 49, 6, ["EDIT"] * 9, colors={8: RED})
    + column(469, 92, 49, 6, ["EDIT"] * 9, colors={5: YELLOW, 6: YELLOW, 7: YELLOW, 8: YELLOW})

    # AI chart controls
    + [AI_PAUSE_BUTTON, AI_START_BUTTON]

    # INPUT panel: EDIT (no function yet)
    + [make_button("EDIT", 2071, 1152, 49, 6)]
)
