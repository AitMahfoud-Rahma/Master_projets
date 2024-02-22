import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

# Paramètres de la simulation
grid_size = 50  # Taille de la grille
prob_initial_alive = 0.3  # Probabilité initiale qu'une cellule (bactérie) soit vivante
prob_antibiotic_kill = 0.4  # Probabilité que l'antibiotique tue une bactérie voisine
prob_growth = 0.1  # Probabilité de croissance naturelle
prob_mortality = 0.2  # Probabilité de mortalité naturelle

# Positionnement de l'antibiotique dans des cellules différentes
antibiotic_positions = [(grid_size // 2, grid_size // 2),
                        (grid_size // 2 - 1, grid_size // 2),
                        (grid_size // 2 + 1, grid_size // 2),
                        (grid_size // 2, grid_size // 2 - 1),
                        (grid_size // 2, grid_size // 2 + 1),
                        (grid_size // 2 - 1, grid_size // 2 - 1),
                        (grid_size // 2 + 1, grid_size // 2 + 1)]

# Initialisation de la grille avec des bactéries vivantes de manière aléatoire
grid = np.random.choice([0, 1], size=(grid_size, grid_size), p=[1 - prob_initial_alive, prob_initial_alive])

# Placer l'antibiotique dans les cellules spécifiées
for position in antibiotic_positions:
    i, j = position
    grid[i, j] = 2  # Utiliser une valeur différente (par exemple, 2) pour représenter les cellules avec l'antibiotique

# Liste pour stocker les étapes de la grille
grid_steps = [np.copy(grid)]

# Modèle mathématique simplifié
def update_bacteria(grid):
    # Croissance naturelle et mortalité naturelle
    new_grid = grid + np.random.choice([0, 1], size=(grid_size, grid_size), p=[1 - prob_growth, prob_growth])
    new_grid -= np.random.choice([0, 1], size=(grid_size, grid_size), p=[1 - prob_mortality, prob_mortality])

    # Effet de l'antibiotique
    for position in antibiotic_positions:
        i, j = position
        if grid[i, j] == 1 and np.random.rand() < prob_antibiotic_kill:
            new_grid[i, j] = 0

    return new_grid

# Fonction pour la mise à jour de la grille à chaque étape
def update_grid(frame_num, img, ax):
    global grid
    grid = update_bacteria(grid)
    img.set_array(grid)
    grid_steps.append(np.copy(grid))  # Ajouter l'étape actuelle à la liste
    return [img]

# Initialisation de la figure
fig, ax = plt.subplots()

# Définition des couleurs
purple_color = '#7d4aa2'  # Mauve
beige_color = '#edecdf'   # Beige
blue_color = 'blue'       # Bleu pour l'antibiotique

# Utiliser une colormap personnalisée
cmap_custom = plt.matplotlib.colors.ListedColormap([beige_color, purple_color, blue_color])

img = ax.imshow(grid, cmap=cmap_custom, interpolation='nearest', vmin=0, vmax=2)  # Ajuster vmax pour refléter la nouvelle valeur

# Définition des limites de la figure
ax.set_xlim(0, grid_size)
ax.set_ylim(0, grid_size)

# Ajout du quadrillage
ax.grid(True, which='both', color='red', linewidth=1)

# Fonction d'animation
ani = animation.FuncAnimation(fig, update_grid, fargs=(img, ax), frames=100, interval=200, blit=True)

# Affichage de l'animation dans Google Colab
HTML(ani.to_jshtml())
