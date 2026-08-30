"""Questao 8 - Predicao como convolucao.

Modelo: x_t = x_{t-1} + epsilon, epsilon ~ N(0, sigma^2).
O script plota o belief anterior, o kernel gaussiano e o belief predito.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_DIR = Path(__file__).resolve().parents[1] / "imagens"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def gaussian(x: np.ndarray, mean: float, std: float) -> np.ndarray:
    """Gaussian probability density function."""
    return np.exp(-0.5 * ((x - mean) / std) ** 2) / (np.sqrt(2.0 * np.pi) * std)


def normalize_density(p: np.ndarray, dx: float) -> np.ndarray:
    """Normalize a sampled density so its numerical integral is one."""
    return p / (np.sum(p) * dx)


# Spatial grid.
x = np.linspace(-8.0, 8.0, 1601)
dx = x[1] - x[0]

# A bimodal prior is used only to make the smoothing effect easy to see.
bel_prior = 0.55 * gaussian(x, -2.0, 0.55) + 0.45 * gaussian(x, 1.4, 0.80)
bel_prior = normalize_density(bel_prior, dx)

# Motion-noise kernel: epsilon ~ N(0, sigma^2).
sigma = 0.70
offsets = (np.arange(x.size) - x.size // 2) * dx
kernel = gaussian(offsets, 0.0, sigma)
kernel = normalize_density(kernel, dx)

# Prediction: bel_bar(x_t) = integral p(x_t|x_{t-1}) bel(x_{t-1}) dx_{t-1}.
bel_pred = np.convolve(bel_prior, kernel, mode="same") * dx
bel_pred = normalize_density(bel_pred, dx)

# Plot. The kernel is drawn against displacement, but shares the same horizontal scale.
fig, ax = plt.subplots(figsize=(8.0, 4.8))
ax.plot(x, bel_prior, label="Belief anterior")
ax.plot(offsets, kernel, linestyle="--", label=r"Kernel $\mathcal{N}(0,\sigma^2)$")
ax.plot(x, bel_pred, linewidth=2.0, label="Belief predita")
ax.set_xlabel("Estado / deslocamento")
ax.set_ylabel("Densidade de probabilidade")
ax.set_title("Questao 8 - Predicao como convolucao")
ax.grid(True, alpha=0.25)
ax.legend()
fig.tight_layout()
fig.savefig(OUT_DIR / "questao8_convolucao.pdf", bbox_inches="tight")
fig.savefig(OUT_DIR / "questao8_convolucao.png", dpi=220, bbox_inches="tight")
plt.close(fig)

print(f"Integral prior:    {np.sum(bel_prior) * dx:.6f}")
print(f"Integral kernel:   {np.sum(kernel) * dx:.6f}")
print(f"Integral predicted:{np.sum(bel_pred) * dx:.6f}")
