import matplotlib.pyplot as plt

from cline import Cline

# Create three collinear points (these all lie on the line y = 2x)
z0 = 1 + 2j  # (1,2)
z1 = 2 + 4j  # (2,4)
z2 = 3 + 6j  # (3,6)

# Create a cline passing through these three points
# Because the points are collinear, this will create a line
cline = Cline.from_three_points(z0, z1, z2)

# Create plot with automatic limits
fig, ax = plt.subplots(figsize=(8, 8))
cline.plot(ax=ax, color="orange", label="Line through 3 collinear points", show_points=True)

# Add a grid to visualize the collinearity
ax.grid(True, linestyle="-", alpha=0.3)
plt.legend()
plt.title("Line Through Three Collinear Points")
