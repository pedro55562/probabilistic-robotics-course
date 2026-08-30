"""Questao 10 - Simulacao completa de um filtro de Bayes 1D.

Modelo de processo: x_t = x_{t-1} + u + epsilon.
Modelo de medicao:  z_t = x_t + delta.
O belief e representado em uma grade e atualizado por convolucao + Bayes.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_DIR = Path(__file__).resolve().parents[1] / "imagens"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def gaussian(x: np.ndarray, mean: float, std: float) -> np.ndarray:
    return np.exp(-0.5 * ((x - mean) / std) ** 2) / (np.sqrt(2.0 * np.pi) * std)


def normalize_density(p: np.ndarray, dx: float) -> np.ndarray:
    total = np.sum(p) * dx
    if total <= 0.0:
        raise RuntimeError("The density has zero numerical mass.")
    return p / total


def moments(x: np.ndarray, p: np.ndarray, dx: float) -> tuple[float, float]:
    mean = np.sum(x * p) * dx
    var = np.sum((x - mean) ** 2 * p) * dx
    return float(mean), float(np.sqrt(var))


rng = np.random.default_rng(935)

# Simulation parameters.
steps = 30
u = 0.80
sigma_process = 0.45
sigma_measurement = 1.00

# Wide grid so boundary effects are negligible during the simulation.
x_grid = np.linspace(-10.0, 40.0, 2501)
dx = x_grid[1] - x_grid[0]

# Initial belief and true state.
bel = gaussian(x_grid, mean=0.0, std=1.0)
bel = normalize_density(bel, dx)
x_true = 0.30

# Discrete convolution kernel for an increment u + epsilon.
offsets = (np.arange(x_grid.size) - x_grid.size // 2) * dx
motion_kernel = gaussian(offsets, mean=u, std=sigma_process)
motion_kernel = normalize_density(motion_kernel, dx)

true_history = [x_true]
measurement_history = [np.nan]
estimate_history = [moments(x_grid, bel, dx)[0]]
std_history = [moments(x_grid, bel, dx)[1]]

for _ in range(steps):
    # Generate the true process and the noisy measurement.
    x_true = x_true + u + rng.normal(0.0, sigma_process)
    z = x_true + rng.normal(0.0, sigma_measurement)

    # Prediction by convolution with the motion model.
    bel_pred = np.convolve(bel, motion_kernel, mode="same") * dx
    bel_pred = normalize_density(bel_pred, dx)

    # Correction using the measurement likelihood.
    likelihood = gaussian(x_grid, mean=z, std=sigma_measurement)
    bel = normalize_density(likelihood * bel_pred, dx)

    mean, std = moments(x_grid, bel, dx)
    true_history.append(x_true)
    measurement_history.append(z)
    estimate_history.append(mean)
    std_history.append(std)

true_history = np.asarray(true_history)
measurement_history = np.asarray(measurement_history)
estimate_history = np.asarray(estimate_history)
std_history = np.asarray(std_history)
t = np.arange(steps + 1)

rmse = np.sqrt(np.mean((estimate_history - true_history) ** 2))

fig, ax = plt.subplots(figsize=(8.2, 4.8))
ax.plot(t, true_history, linewidth=2.0, label="Estado real")
ax.scatter(t[1:], measurement_history[1:], s=20, alpha=0.65, label="Medicoes")
ax.plot(t, estimate_history, linewidth=2.0, label="Media estimada")
ax.fill_between(
    t,
    estimate_history - 2.0 * std_history,
    estimate_history + 2.0 * std_history,
    alpha=0.18,
    label=r"Faixa $\pm 2\sigma$",
)
ax.set_xlabel("Passo de tempo")
ax.set_ylabel("Estado")
ax.set_title(f"Questao 10 - Filtro de Bayes 1D (RMSE = {rmse:.3f})")
ax.grid(True, alpha=0.25)
ax.legend()
fig.tight_layout()
fig.savefig(OUT_DIR / "questao10_simulacao.pdf", bbox_inches="tight")
fig.savefig(OUT_DIR / "questao10_simulacao.png", dpi=220, bbox_inches="tight")
plt.close(fig)

print(f"RMSE da media estimada: {rmse:.6f}")
print(f"Estado real final:      {true_history[-1]:.6f}")
print(f"Estimativa final:       {estimate_history[-1]:.6f}")
print(f"Desvio posterior final: {std_history[-1]:.6f}")
