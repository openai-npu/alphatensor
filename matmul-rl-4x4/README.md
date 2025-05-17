# matmul-rl-4x4

**Discovering a 4×4 matrix multiplication algorithm of rank ≤45 using Reinforcement Learning.**

This project aims to find, using GPU-accelerated RL, a 4×4 matrix multiplication algorithm that uses at most 45 scalar multiplications (rank ≤45), which would be a world first.

## References

- Strassen, V. (1969). Gaussian elimination is not optimal. Numerische Mathematik.
- Waksman, A. (1970). On Winograd's algorithm for multiplication of matrices. Linear Algebra and its Applications.
- Bläser, M. (2003). On the complexity of the multiplication of matrices. Proceedings of the 33rd STOC.
- AlphaTensor (2022). Deep Reinforcement Learning for Tensor Programs. Nature.
- AlphaEvolve (2025). [To appear].

## Usage

```bash
./scripts/run_train.sh --run_id exp1 --max_steps 5000000
```

Track live metrics at http://localhost:8265 and on Weights & Biases.

If `results/rank45.json` appears → 🎉 publish & notify.

## License

MIT
