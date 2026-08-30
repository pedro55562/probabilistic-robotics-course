import numpy as np
import matplotlib.pyplot as plt

mu1 = 2.0
sigma1 = 0.5

mu2 = 2.3
sigma2 = 0.3

var1 = sigma1**2
var2 = sigma2**2

# Produto de duas gaussianas
var = 1 / (1 / var1 + 1 / var2)

mu = var * (
    mu1 / var1
    + mu2 / var2
)

sigma = np.sqrt(var)

print("Gaussiana 1:")
print(f"media = {mu1}")
print(f"variancia = {var1}")

print("\nGaussiana 2:")
print(f"media = {mu2}")
print(f"variancia = {var2}")

print("\nProduto:")
print(f"media = {mu:.4f}")
print(f"variancia = {var:.4f}")
print(f"desvio padrao = {sigma:.4f}")


def gaussian(x, mu, sigma):
    return (
        1 / (sigma * np.sqrt(2 * np.pi))
        * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    )


x = np.linspace(0, 4, 1000)

p1 = gaussian(x, mu1, sigma1)
p2 = gaussian(x, mu2, sigma2)
p = gaussian(x, mu, sigma)

plt.plot(x, p1, label="Gaussiana 1")
plt.plot(x, p2, label="Gaussiana 2")
plt.plot(x, p, label="Produto")

plt.xlabel("x")
plt.ylabel("Densidade")
plt.title("Produto de Gaussianas")
plt.grid()
plt.legend()

plt.show()