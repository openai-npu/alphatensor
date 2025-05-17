"""
matmul_env.py

Minimal runnable Gymnasium environment for 4×4 matrix-multiplication rank search.

This baseline keeps only an integer “current rank” (no factor triples) so that
RLlib PPO can run immediately.  Replace `_apply_action` with real mutation and
verification logic later.

Observation : np.array([current_rank, best_rank], dtype=float32)
Action space: 0 = mutate_factor, 1 = swap_two, 2 = prune_one
Reward      : +0.2  if verify-success and same rank
              +1.0  per rank drop
              +50.0 upon reaching rank 45 (episode terminates)
              −1.0  on invalid action
Episode ends: rank == 45  OR  step budget exhausted
"""

from __future__ import annotations

import random
from typing import Any, Dict, Tuple

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class MatmulEnv(gym.Env):
    """Mock 4×4 matmul environment exposing Gymnasium API."""

    metadata = {"render_modes": ["human"]}

    def __init__(self, *, starting_rank: int = 46, max_steps: int = 128) -> None:
        super().__init__()
        if starting_rank < 45:
            raise ValueError("starting_rank must be ≥ 45")
        self.starting_rank = starting_rank
        self.max_steps = max_steps

        # Observation: [current_rank, best_rank]
        self.observation_space = spaces.Box(
            low=np.array([45.0, 45.0], dtype=np.float32),
            high=np.array([50.0, 50.0], dtype=np.float32),
            dtype=np.float32,
        )

        # Three discrete edit actions
        self.action_space = spaces.Discrete(3)

        self.current_rank: int = starting_rank
        self.best_rank: int = starting_rank
        self.steps: int = 0

    # --------------------------------------------------------------------- #
    # Gymnasium API                                                         #
    # --------------------------------------------------------------------- #

    def reset(
        self,
        *,
        seed: int | None = None,
        options: Dict[str, Any] | None = None,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        super().reset(seed=seed)
        self.current_rank = self.starting_rank
        self.best_rank = self.starting_rank
        self.steps = 0
        return self._get_obs(), {}

    def step(
        self, action: int
    ) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        if not self.action_space.contains(action):
            raise ValueError(f"Invalid action {action}")
        self.steps += 1

        base_reward, valid = self._apply_action(action)

        terminated = self.current_rank == 45
        truncated = self.steps >= self.max_steps

        reward = base_reward + (50.0 if terminated else 0.0)
        if not valid:
            reward = -1.0

        return self._get_obs(), reward, terminated, truncated, {"rank": self.current_rank}

    def render(self) -> None:  # noqa: D401
        print(f"Step {self.steps}: rank={self.current_rank}, best={self.best_rank}")

    # ------------------------------------------------------------------ #
    # Helpers                                                            #
    # ------------------------------------------------------------------ #

    def _get_obs(self) -> np.ndarray:
        return np.array([self.current_rank, self.best_rank], dtype=np.float32)

    def _apply_action(self, action: int) -> Tuple[float, bool]:
        """Mock rank-edit logic used solely for RL loop testing."""
        base_reward = 0.0
        valid = True

        verify_success = random.random() < 0.9  # placeholder success rate

        if action == 0:  # mutate_factor
            if verify_success and self.current_rank > 45:
                if random.random() < 0.3:  # 30 % chance to drop rank by 1
                    self.current_rank -= 1
                    base_reward += 1.0
            else:
                valid = False

        elif action == 1:  # swap_two
            if verify_success:
                base_reward += 0.2
            else:
                valid = False

        elif action == 2:  # prune_one
            if self.current_rank > 45:
                self.current_rank -= 1
                base_reward += 1.0
            else:
                valid = False

        # Update best_rank
        if self.current_rank < self.best_rank:
            self.best_rank = self.current_rank

        return base_reward, valid
