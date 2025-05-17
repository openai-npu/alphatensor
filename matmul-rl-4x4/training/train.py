"""
train.py

Minimal PPO training script for 4×4 matmul rank-search.

Curriculum (stub): fixed starting rank 46 for now.
Hardware         : num_gpus=1 (RTX 5090 assumed), num_workers=8.
Checkpointing    : every 500 episodes.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
import torch  # for GPU check

import sys, os
# Ensure matmul-rl-4x4 directory is on PYTHONPATH so `env` can be imported
_here = os.path.abspath(os.path.dirname(__file__))
_root_dir = os.path.dirname(_here)
sys.path.insert(0, _root_dir)
from env.matmul_env import MatmulEnv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_id", default="exp0", type=str)
    parser.add_argument("--max_steps", default=100_000, type=int)
    parser.add_argument("--num_workers", default=8, type=int)
    return parser.parse_args()


def env_creator(env_config):
    # env_config may carry curriculum later
    return MatmulEnv(starting_rank=46, max_steps=128)


def main() -> None:
    args = parse_args()
    # Check for GPU availability
    print(f"GPU available: {torch.cuda.is_available()}, GPU count: {torch.cuda.device_count()}")

    # Initialise Ray
    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)

    # Register environment with RLlib
    tune.register_env("MatmulEnv-v0", env_creator)

    # Tune run using legacy config dict
    results_dir = Path(__file__).parent.parent / "results" / args.run_id
    results_dir.mkdir(parents=True, exist_ok=True)

    config = {
        "env": "MatmulEnv-v0",
        "framework": "torch",
        "num_gpus": 1,
        "num_workers": args.num_workers,
        "rollout_fragment_length": 128,
        "train_batch_size": 4096,
        "gamma": 0.99,
        "lambda": 0.95,
        "lr": 3e-4,
        "clip_param": 0.2,
        "disable_env_checking": True,
    }

    tune.run(
        "PPO",
        config=config,
        stop={"training_iteration": args.max_steps},
        storage_path=str(results_dir),
        name=args.run_id,
        checkpoint_freq=500,
    )

    ray.shutdown()


if __name__ == "__main__":
    main()
