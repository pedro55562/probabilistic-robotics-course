import numpy as np
import matplotlib.pyplot as plt

N = 10000

# Ruídos uniformes com média zero
x1 = np.random.uniform(-1, 1, N)

x3 = (
    np.random.uniform(-1, 1, N)
    + np.random.uniform(-1, 1, N)
    + np.random.uniform(-1, 1, N)
)

x10 = sum(np.random.uniform(-1, 1, N) for _ in range(10))


def plot_hist(data, title):
    mu = np.mean(data)
    sigma = np.std(data)

    x = np.linspace(data.min(), data.max(), 500)

    gaussian = (
        1 / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    )

    plt.figure()

    plt.hist(
        data,
        bins=60,
        density=True,
        alpha=0.6,
        label="Amostras"
    )

    plt.plot(
        x,
        gaussian,
        linewidth=2,
        label="Gaussiana ajustada"
    )

    plt.xlabel("Valor")
    plt.ylabel("Densidade")
    plt.title(title)
    plt.grid()
    plt.legend()

    print(f"{title}:")
    print(f"media = {mu:.4f}")
    print(f"desvio padrao = {sigma:.4f}\n")


plot_hist(x1, "1 ruido uniforme")
plot_hist(x3, "Soma de 3 ruidos uniformes")
plot_hist(x10, "Soma de 10 ruidos uniformes")

plt.show()