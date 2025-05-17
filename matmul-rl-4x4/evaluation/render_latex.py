"""
render_latex.py

Render a LaTeX table from rank45.json factor triples.
"""

import sys
import json

def render_latex(triples):
    # TODO: Implement LaTeX rendering of triples
    return "% LaTeX table for rank-45 factor triples\n"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python render_latex.py rank45.json")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        triples = json.load(f)
    print(render_latex(triples))
