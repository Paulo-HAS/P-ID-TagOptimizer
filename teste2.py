import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Caminho do arquivo Excel (substitua pelo caminho correto)
excel_path = "C:\comp_evo\resultados.csv"

# Ler dados do Excel (colunas z, x, y)
data = pd.read_csv(excel_path, usecols=[0, 1, 2], names=["z", "x", "y"])

# Extrair os valores das colunas
z = data["z"].values
x = data["x"].values
y = data["y"].values

# Criar uma grade de pontos para interpolação
x_grid = np.linspace(50, 150, 100)
y_grid = np.linspace(50, 150, 100)
X, Y = np.meshgrid(x_grid, y_grid)

# Interpolar os dados para criar uma superfície
Z = griddata((x[1:], y[1:]), z[1:], (X, Y), method='cubic')

# Plotar a função em 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="k")
ax.set_title("Superfície Interpolada em 3D")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
plt.show()

# Gráficos auxiliares em 2D
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Contorno (contour) em 2D
contour = axs[0].contourf(X, Y, Z, cmap="viridis")
axs[0].set_title("Projeção de Contorno (2D)")
axs[0].set_xlabel("X")
axs[0].set_ylabel("Y")
fig.colorbar(contour, ax=axs[0], orientation="vertical")

# Projeção em 2D (heatmap)
heatmap = axs[1].imshow(Z, extent=(50, 150, 50, 150), origin="lower", cmap="viridis", aspect="auto")
axs[1].set_title("Heatmap (2D)")

axs[1].set_xlabel("X")
axs[1].set_ylabel("Y")
fig.colorbar(heatmap, ax=axs[1], orientation="vertical")

plt.tight_layout()
plt.show()