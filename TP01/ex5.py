import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

Sigma = np.array([
    [2.0, 1.2],
    [1.2, 1.0]
])

# Autovalores e autovetores
eigvals, eigvecs = np.linalg.eigh(Sigma)

idx = np.argsort(eigvals)[::-1]
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]

v_max = eigvecs[:, 0]

if v_max[0] < 0:
    v_max = -v_max

angle = np.degrees(np.arctan2(v_max[1], v_max[0]))

print("Autovalores:")
print(eigvals)

print("\nAutovetores:")
print(eigvecs)

print("\nDirecao de maior variancia:")
print(v_max)

print("\nAngulo:")
print(angle)

print("\nCovariancia xy:")
print(Sigma[0, 1])


# Elipse de covariancia
n_std = 2

width = 2 * n_std * np.sqrt(eigvals[0])
height = 2 * n_std * np.sqrt(eigvals[1])

fig, ax = plt.subplots()

ellipse = Ellipse(
    (0, 0),
    width,
    height,
    angle=angle,
    fill=False
)

ax.add_patch(ellipse)

ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.set_aspect("equal")
ax.grid()

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Elipse de covariancia")

plt.show()