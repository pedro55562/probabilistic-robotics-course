import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

mu = np.array([1.0, 2.0])

Sigma = np.array([
    [1.0, 0.5],
    [0.5, 2.0]
])

A = np.array([
    [2.0, 0.0],
    [0.0, 0.5]
])

mu_new = A @ mu
Sigma_new = A @ Sigma @ A.T

eigvals, eigvecs = np.linalg.eigh(Sigma)
eigvals_new, eigvecs_new = np.linalg.eigh(Sigma_new)

print("Media original:")
print(mu)

print("\nNova media:")
print(mu_new)

print("\nCovariancia original:")
print(Sigma)

print("\nNova covariancia:")
print(Sigma_new)

print("\nAutovalores originais:")
print(eigvals)

print("\nAutovalores transformados:")
print(eigvals_new)


def covariance_ellipse(ax, mu, Sigma, label):
    values, vectors = np.linalg.eigh(Sigma)

    idx = np.argsort(values)[::-1]
    values = values[idx]
    vectors = vectors[:, idx]

    v = vectors[:, 0]

    angle = np.degrees(
        np.arctan2(v[1], v[0])
    )

    width = 4 * np.sqrt(values[0])
    height = 4 * np.sqrt(values[1])

    ellipse = Ellipse(
        mu,
        width,
        height,
        angle=angle,
        fill=False,
        linewidth=2,
        label=label
    )

    ax.add_patch(ellipse)


fig, ax = plt.subplots()

covariance_ellipse(
    ax,
    mu,
    Sigma,
    "Original"
)

covariance_ellipse(
    ax,
    mu_new,
    Sigma_new,
    "Transformada"
)

ax.scatter(*mu)
ax.scatter(*mu_new)

ax.set_xlim(-3, 7)
ax.set_ylim(-2, 6)

ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid()
ax.legend()

plt.show()