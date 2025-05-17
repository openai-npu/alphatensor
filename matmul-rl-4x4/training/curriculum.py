"""
curriculum.py

Curriculum learning schedule for target ranks: 49 (10k steps) → 46 → 45.
"""

class Curriculum:
    def __init__(self):
        # TODO: Initialize curriculum state
        self.stages = [
            {"target_rank": 49, "steps": 10000},
            {"target_rank": 46, "steps": None},
            {"target_rank": 45, "steps": None},
        ]
        self.current_stage = 0

    def get_target_rank(self, step):
        # TODO: Return current target rank based on step
        return self.stages[self.current_stage]["target_rank"]

    def advance(self):
        # TODO: Advance to next curriculum stage
        if self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
