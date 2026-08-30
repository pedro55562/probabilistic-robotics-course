"""Questao 9 - Update Bayesiano com likelihood estreita e larga."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_DIR = Path(__file__).resolve().parents[1] / "imagens"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def gaussian(x: np.ndarray, mean: float, std: float) -> np.ndarray:
    return np.exp(-0.5 * ((x - mean) / std) ** 2) / (np.sqrt(2.0 * np.pi) * std)


def normalize_density(p: np.ndarray, dx: float) -> np.ndarray:
    return p / (np.sum(p) * dx)


def moments(x: np.ndarray, p: np.ndarray, dx: float) -> tuple[float, float]:
    mean = np.sum(x * p) * dx
    var = np.sum((x - mean) ** 2 * p) * dx
    return float(mean), float(np.sqrt(var))


x = np.linspace(-6.0, 6.0, 1601)
dx = x[1] - x[0]

# Predicted belief used before the measurement update.
bel_pred = gaussian(x, mean=0.0, std=1.30)
bel_pred = normalize_density(bel_pred, dx)

# Same measurement, two different sensor-noise levels.
z = 1.50
lik_narrow = gaussian(x, mean=z, std=0.45)
lik_wide = gaussian(x, mean=z, std=1.80)

# Bayes update: bel(x_t) = eta p(z_t|x_t) bel_bar(x_t).
post_narrow = normalize_density(lik_narrow * bel_pred, dx)
post_wide = normalize_density(lik_wide * bel_pred, dx)

mean_prior, std_prior = moments(x, bel_pred, dx)
mean_narrow, std_narrow = moments(x, post_narrow, dx)
mean_wide, std_wide = moments(x, post_wide, dx)

fig, ax = plt.subplots(figsize=(8.0, 4.8))
ax.plot(x, bel_pred, label="Belief predita")
ax.plot(x, lik_narrow / np.max(lik_narrow) * np.max(bel_pred), linestyle="--", label="Likelihood estreita (escala visual)")
ax.plot(x, lik_wide / np.max(lik_wide) * np.max(bel_pred), linestyle=":", label="Likelihood larga (escala visual)")
ax.plot(x, post_narrow, linewidth=2.0, label="Posterior - estreita")
ax.plot(x, post_wide, linewidth=2.0, label="Posterior - larga")
ax.axvline(z, linestyle="-.", linewidth=1.0, label=f"Medicao z = {z:.1f}")
ax.set_xlabel("Estado")
ax.set_ylabel("Densidade / escala relativa")
ax.set_title("Questao 9 - Efeito da largura da likelihood")
ax.grid(True, alpha=0.25)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT_DIR / "questao9_update.pdf", bbox_inches="tight")
fig.savefig(OUT_DIR / "questao9_update.png", dpi=220, bbox_inches="tight")
plt.close(fig)

print(f"Prior:             mean={mean_prior:.4f}, std={std_prior:.4f}")
print(f"Posterior estreita: mean={mean_narrow:.4f}, std={std_narrow:.4f}")
print(f"Posterior larga:    mean={mean_wide:.4f}, std={std_wide:.4f}")
