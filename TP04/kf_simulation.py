import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from pathlib import Path

np.random.seed(7)

# Parâmetros do sistema
A = np.array([[1.0, 1.0],
              [0.0, 1.0]])
B = np.array([[0.0],
              [1.0]])
C = np.array([[1.0, 0.0]])
R = np.array([[0.01, 0.0],
              [0.0, 0.01]])
Q = np.array([[0.25]])

mu0 = np.array([0.0, 1.0])
Sigma0 = np.array([[0.1, 0.0],
                   [0.0, 0.1]])

# Configuração da simulação
n_steps = 50
u = 0.05
output_dir = Path(__file__).resolve().parent / "figuras"
output_dir.mkdir(exist_ok=True)

true_state = np.zeros((n_steps + 1, 2))
kf_state = np.zeros((n_steps + 1, 2))
dr_state = np.zeros((n_steps + 1, 2))
measurements = np.full(n_steps + 1, np.nan)
covariances = np.zeros((n_steps + 1, 2, 2))
gains = np.zeros((n_steps + 1, 2))

true_state[0] = mu0
kf_state[0] = mu0
dr_state[0] = mu0
covariances[0] = Sigma0

mu = mu0.copy()
Sigma = Sigma0.copy()
I = np.eye(2)

# Simulação e Filtro de Kalman
for k in range(1, n_steps + 1):
    control = np.array([u])
    process_noise = np.random.multivariate_normal(np.zeros(2), R)
    true_state[k] = A @ true_state[k - 1] + (B @ control).ravel() + process_noise

    measurement_noise = np.random.normal(0.0, np.sqrt(Q[0, 0]))
    measurements[k] = (C @ true_state[k])[0] + measurement_noise

    dr_state[k] = A @ dr_state[k - 1] + (B @ control).ravel()

    mu_pred = A @ mu + (B @ control).ravel()
    Sigma_pred = A @ Sigma @ A.T + R

    innovation = measurements[k] - (C @ mu_pred)[0]
    S = C @ Sigma_pred @ C.T + Q
    K = Sigma_pred @ C.T @ np.linalg.inv(S)

    mu = mu_pred + K[:, 0] * innovation
    Sigma = (I - K @ C) @ Sigma_pred @ (I - K @ C).T + K @ Q @ K.T

    kf_state[k] = mu
    covariances[k] = Sigma
    gains[k] = K[:, 0]

time = np.arange(n_steps + 1)

# Gráficos
plt.figure(figsize=(9, 5))
plt.plot(time, true_state[:, 0], label="Posição real", linewidth=2)
plt.scatter(time[1:], measurements[1:], label="Medições", s=18, alpha=0.7)
plt.plot(time, dr_state[:, 0], "--", label="Dead reckoning")
plt.plot(time, kf_state[:, 0], label="Estimativa KF", linewidth=2)
plt.xlabel("Iteração")
plt.ylabel("Posição")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(output_dir / "posicao.pdf", bbox_inches="tight")
plt.close()

plt.figure(figsize=(9, 5))
plt.plot(time, true_state[:, 1], label="Velocidade real", linewidth=2)
plt.plot(time, dr_state[:, 1], "--", label="Dead reckoning")
plt.plot(time, kf_state[:, 1], label="Estimativa KF", linewidth=2)
plt.xlabel("Iteração")
plt.ylabel("Velocidade")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(output_dir / "velocidade.pdf", bbox_inches="tight")
plt.close()

plt.figure(figsize=(9, 5))
plt.plot(time, covariances[:, 0, 0], label=r"$\Sigma_{pp}$")
plt.plot(time, covariances[:, 1, 1], label=r"$\Sigma_{vv}$")
plt.plot(time, np.trace(covariances, axis1=1, axis2=2), "--", label=r"$\mathrm{tr}(\Sigma)$")
plt.xlabel("Iteração")
plt.ylabel("Covariância")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(output_dir / "covariancia.pdf", bbox_inches="tight")
plt.close()

selected = [0, 1, 2, 5, 10, 20]
fig, axes = plt.subplots(2, 3, figsize=(10, 6.5))
chi2_95 = 5.991
for ax, k in zip(axes.ravel(), selected):
    Sigma_k = covariances[k]
    values, vectors = np.linalg.eigh(Sigma_k)
    order = values.argsort()[::-1]
    values = values[order]
    vectors = vectors[:, order]
    angle = np.degrees(np.arctan2(vectors[1, 0], vectors[0, 0]))
    width, height = 2.0 * np.sqrt(chi2_95 * values)
    ellipse = Ellipse(kf_state[k], width, height, angle=angle, fill=False, linewidth=2)
    ax.add_patch(ellipse)
    ax.scatter(kf_state[k, 0], kf_state[k, 1], s=20)
    margin = 0.7 * max(width, height)
    ax.set_xlim(kf_state[k, 0] - margin, kf_state[k, 0] + margin)
    ax.set_ylim(kf_state[k, 1] - margin, kf_state[k, 1] + margin)
    ax.set_title(f"k = {k}")
    ax.set_xlabel("p")
    ax.set_ylabel("v")
    ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(output_dir / "elipses_covariancia.pdf", bbox_inches="tight")
plt.close(fig)

plt.figure(figsize=(9, 5))
plt.plot(time[1:], gains[1:, 0], label=r"$K_p$")
plt.plot(time[1:], gains[1:, 1], label=r"$K_v$")
plt.xlabel("Iteração")
plt.ylabel("Ganho de Kalman")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(output_dir / "ganho_kalman.pdf", bbox_inches="tight")
plt.close()

rmse_dr_p = np.sqrt(np.mean((true_state[:, 0] - dr_state[:, 0]) ** 2))
rmse_kf_p = np.sqrt(np.mean((true_state[:, 0] - kf_state[:, 0]) ** 2))
rmse_dr_v = np.sqrt(np.mean((true_state[:, 1] - dr_state[:, 1]) ** 2))
rmse_kf_v = np.sqrt(np.mean((true_state[:, 1] - kf_state[:, 1]) ** 2))

print(f"RMSE posição - dead reckoning: {rmse_dr_p:.4f}")
print(f"RMSE posição - KF: {rmse_kf_p:.4f}")
print(f"RMSE velocidade - dead reckoning: {rmse_dr_v:.4f}")
print(f"RMSE velocidade - KF: {rmse_kf_v:.4f}")
print(f"Ganho final: {gains[-1]}")
print(f"Covariância final:\n{covariances[-1]}")
