"""
candidate_utils.py

Simple mutation and crossover helpers for sets of factor triples.

A triple is represented as a tuple of three NumPy arrays (U, V, W) each of
shape (4, 4).  These utilities operate generically on arrays without assuming
special structure – they are *place-holders* so the rest of the RL pipeline can
run.  Replace them with domain-specific mutations later.
"""

from __future__ import annotations

import random
from typing import List, Tuple

import numpy as np

Triple = Tuple[np.ndarray, np.ndarray, np.ndarray]


# --------------------------------------------------------------------------- #
# Mutation                                                                    #
# --------------------------------------------------------------------------- #
def mutate_factor(triples: List[Triple], sigma: float = 0.05) -> List[Triple]:
    """
    Add Gaussian noise (σ) to a random factor matrix within a random triple.

    Parameters
    ----------
    triples : list[Triple]
        Factor triples for a candidate algorithm.
    sigma : float, optional
        Standard deviation for the additive Gaussian noise, by default 0.05.

    Returns
    -------
    list[Triple]
        A *new* list with one mutated factor.
    """
    if not triples:
        return triples

    triples_mut = [tuple(map(np.copy, t)) for t in triples]  # deep copy
    idx = random.randrange(len(triples_mut))
    factor_idx = random.randrange(3)
    noise = np.random.normal(scale=sigma, size=(4, 4))
    triples_mut[idx][factor_idx][:] += noise
    return [tuple(t) for t in triples_mut]


# --------------------------------------------------------------------------- #
# Crossover                                                                   #
# --------------------------------------------------------------------------- #
def crossover(
    triples1: List[Triple], triples2: List[Triple]
) -> List[Triple]:
    """
    One-point crossover: combine prefix of triples1 with suffix of triples2.

    If either list is empty, returns a copy of the other.

    Returns
    -------
    list[Triple]
        Combined candidate.
    """
    if not triples1:
        return [tuple(map(np.copy, t)) for t in triples2]
    if not triples2:
        return [tuple(map(np.copy, t)) for t in triples1]

    cut = random.randrange(1, min(len(triples1), len(triples2)))
    combined = triples1[:cut] + triples2[cut:]
    return [tuple(map(np.copy, t)) for t in combined]
