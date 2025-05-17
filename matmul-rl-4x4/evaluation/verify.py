"""
verify.py

Exact SymPy checker for candidate 4x4 matrix multiplication algorithms.
"""

import sympy as sp

def verify_triples(triples):
    """
    Verifies that the given list of (U, V, W) factor triples implements
    4x4 matrix multiplication exactly over ℝ/ℂ.

    Returns True on success, False otherwise.
    """
    A = sp.MatrixSymbol('A', 4, 4)
    B = sp.MatrixSymbol('B', 4, 4)
    expr = sum(U * A * V * B * W for (U, V, W) in triples)
    try:
        return sp.simplify(expr - A * B) == 0
    except Exception:
        return False
